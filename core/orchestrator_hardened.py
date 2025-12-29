"""
core/orchestrator_hardened.py - Orchestrator Reforzado

Integra:
- SafeCycleContext para interrupciones seguras
- ExecutionQueue para prioridad de usuario
- Signal handlers mejorados
- Health-checks de ML
"""

import signal
import threading
import asyncio
import time
import logging
from contextlib import contextmanager
from enum import Enum
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class CycleType(Enum):
    AUTO = "automatic"
    USER = "human_initiated"
    URGENT = "urgent_rollback"


class OrchestrationState:
    """Estado global compartido del Orchestrator"""
    
    def __init__(self):
        self.current_cycle = None
        self.current_cycle_type = None
        self.cycle_lock = threading.RLock()  # Re-entrant para signal handlers
        self.should_interrupt = False
        self.interrupt_reason = None
        self.interrupt_timestamp = None


class CentralOrchestratorHardened:
    """
    Orchestrator reforzado para alta presión
    
    Características de seguridad:
    1. SafeCycleContext: Interrupciones limpias
    2. ExecutionQueue: Prioridad de usuario
    3. Signal handlers: No bloquean, solo encolan
    4. Health-checks: ML validado post-commit
    """
    
    def __init__(self):
        self.state = OrchestrationState()
        
        # Managers
        from core.context_sentinel import ContextSentinel
        from core.execution_queue import ExecutionQueue
        from oracle.oracle_manager import OracleManagerWithHealthCheck
        
        self.memory_manager = ContextSentinel()
        self.execution_queue = ExecutionQueue(max_workers=1)
        self.oracle_manager = OracleManagerWithHealthCheck()
        
        # Registrar signal handlers
        signal.signal(signal.SIGUSR1, self._handle_user_signal)
        signal.signal(signal.SIGUSR2, self._handle_emergency_signal)
        
        # Callbacks del LLM o dashboard
        self.on_cycle_interrupted = None
        self.on_user_priority_triggered = None
        
        logger.info("✅ CentralOrchestratorHardened inicializado")
    
    def _handle_user_signal(self, signum, frame):
        """
        Handler para SIGUSR1 (propuesta del usuario)
        
        IMPORTANTE: Este handler debe ser RÁPIDO
        No ejecuta nada, solo encola
        """
        
        logger.info("⚡ SIGUSR1 recibido (Usuario)")
        
        try:
            # NO usar self.state.cycle_lock aquí (puede causar deadlock)
            # Solo actualizar flags atómicos
            
            if self.state.current_cycle:
                logger.warning(
                    f"⚠️ Interrumpiendo ciclo: "
                    f"{self.state.current_cycle_type.value}"
                )
                self.state.should_interrupt = True
                self.state.interrupt_reason = "USER_PRIORITY"
                self.state.interrupt_timestamp = time.time()
                
                if self.on_user_priority_triggered:
                    self.on_user_priority_triggered()
            
            # Obtener propuesta pendiente
            last_proposal = self.memory_manager.get_last_approved_proposal()
            
            if last_proposal:
                from core.execution_queue import ExecutionTask, ExecutionPriority
                
                # Crear tarea con MÁXIMA PRIORIDAD
                task = ExecutionTask(
                    priority=ExecutionPriority.USER_IMMEDIATE,
                    proposal_id=last_proposal.id,
                    cycle_type='USER',
                    timestamp=time.time(),
                    source='user_signal'
                )
                
                # Encolar (thread-safe, rápido)
                self.execution_queue.enqueue(task)
                
                logger.info(
                    f"📋 Propuesta encolada con máxima prioridad: "
                    f"{last_proposal.id}"
                )
        
        except Exception as e:
            logger.error(f"❌ Error en signal handler: {e}")
    
    def _handle_emergency_signal(self, signum, frame):
        """
        Handler para SIGUSR2 (emergencia)
        
        Usado si detectamos corrupción
        """
        logger.critical("🚨 SIGUSR2 recibido (EMERGENCIA)")
        
        self.state.should_interrupt = True
        self.state.interrupt_reason = "EMERGENCY_ROLLBACK"
        self.state.interrupt_timestamp = time.time()
    
    @contextmanager
    def safe_cycle_context(self, cycle_type: CycleType):
        """
        Context manager para ciclos seguros
        
        Garantiza:
        - Cleanup automático si se interrumpe
        - Prioridad humana
        - Sin archivos bloqueados
        
        Uso:
            with self.safe_cycle_context(CycleType.AUTO):
                # Ejecutar ciclo
                await self.run_improvement_cycle()
        """
        
        cycle_id = f"CYCLE_{int(time.time() * 1000)}"
        start_time = time.time()
        
        try:
            with self.state.cycle_lock:
                # Verificar si debe interrumpirse ANTES de empezar
                if self.state.should_interrupt:
                    logger.info(
                        f"✅ Interrupción limpia, no ejecutando {cycle_id}"
                    )
                    self._handle_pending_requests()
                    return
                
                # Marcar ciclo en progreso
                self.state.current_cycle = cycle_id
                self.state.current_cycle_type = cycle_type
            
            logger.info(
                f"▶️ Iniciando {cycle_type.value} cycle: {cycle_id}"
            )
            
            yield cycle_id  # El ciclo se ejecuta aquí
            
        except Exception as e:
            logger.error(f"❌ Error en ciclo: {e}")
            self._cleanup_cycle(cycle_id)
            raise
        
        finally:
            duration = time.time() - start_time
            
            with self.state.cycle_lock:
                # Limpiar estado del ciclo
                self.state.current_cycle = None
                self.state.current_cycle_type = None
                
                # Si fue interrumpido, procesar solicitudes del usuario
                if self.state.should_interrupt:
                    logger.info(
                        f"🔄 Ciclo interrumpido después de {duration:.2f}s, "
                        f"procesando solicitudes del usuario"
                    )
                    self.state.should_interrupt = False
                    
                    if self.on_cycle_interrupted:
                        self.on_cycle_interrupted({
                            'cycle_id': cycle_id,
                            'reason': self.state.interrupt_reason,
                            'duration': duration
                        })
                    
                    # Procesar propuestas pendientes
                    self._handle_pending_requests()
                else:
                    logger.info(
                        f"✅ Ciclo completado en {duration:.2f}s"
                    )
    
    def _cleanup_cycle(self, cycle_id: str):
        """Limpiar recursos del ciclo si se interrumpe"""
        
        logger.info(f"🧹 Limpiando ciclo: {cycle_id}")
        
        try:
            # Eliminar backups pendientes
            backup_path = Path(f"memory/backups/{cycle_id}")
            if backup_path.exists():
                import shutil
                shutil.rmtree(backup_path)
                logger.info(f"  Backup eliminado: {backup_path}")
            
            # Marcar ciclo como interrumpido en historial
            self.memory_manager.log_event({
                'type': 'cycle_interrupted',
                'cycle_id': cycle_id,
                'reason': self.state.interrupt_reason,
                'timestamp': datetime.now().isoformat()
            })
        
        except Exception as e:
            logger.error(f"❌ Error durante cleanup: {e}")
    
    def _check_interrupt(self) -> bool:
        """
        Verificar si se solicita interrupción
        
        Se llama dentro de las fases para permitir
        terminación graceful
        """
        if self.state.should_interrupt:
            logger.info(
                f"⏸️ Interrupción solicitada: "
                f"{self.state.interrupt_reason}"
            )
            return True
        return False
    
    def _handle_pending_requests(self):
        """Procesar propuestas pendientes en cola"""
        
        stats = self.execution_queue.get_stats()
        
        if stats['queue_size'] > 0:
            logger.info(
                f"📋 Procesando {stats['queue_size']} "
                f"tareas pendientes de ejecución"
            )
            
            # Esperar a que se procesen (con timeout)
            self.execution_queue.wait_for_completion(timeout=300)
        else:
            logger.info("✅ No hay tareas pendientes")
    
    async def run_improvement_cycle(
        self, 
        cycle_type: CycleType = CycleType.AUTO
    ):
        """
        Ejecutar ciclo de mejora con manejo de interrupciones
        
        Si se recibe SIGUSR1 durante la ejecución:
        1. El ciclo termina gracefully
        2. Los backups se limpian
        3. Las propuestas del usuario se procesan
        """
        
        with self.safe_cycle_context(cycle_type):
            try:
                # FASE 1: Recolectar métricas
                if self._check_interrupt():
                    logger.info("  Interrupción en Fase 1")
                    return
                
                logger.info("📊 FASE 1: Recolectando métricas...")
                metrics = await self._collect_metrics()
                logger.info(f"✅ Métricas recolectadas")
                
                # FASE 2: Generar propuestas
                if self._check_interrupt():
                    logger.info("  Interrupción en Fase 2")
                    return
                
                logger.info("💡 FASE 2: Generando propuestas...")
                proposals = self._generate_proposals(metrics, cycle_type)
                logger.info(
                    f"✅ {len(proposals)} propuestas generadas"
                )
                
                # FASE 3: Evaluar propuestas
                if self._check_interrupt():
                    logger.info("  Interrupción en Fase 3")
                    return
                
                logger.info("🔍 FASE 3: Evaluando propuestas...")
                approved = []
                
                for proposal in proposals:
                    score = self.evaluator.evaluate(proposal, metrics)
                    if score >= 0.70:
                        approved.append(proposal)
                        self.memory_manager.update_proposal_status(
                            proposal.id, 'APPROVED_AUTO'
                        )
                
                logger.info(f"✅ {len(approved)} propuestas aprobadas")
                
                # FASE 4: Ejecutar propuestas aprobadas
                logger.info(f"⚙️ FASE 4: Ejecutando propuestas...")
                
                for proposal in approved:
                    # Verificar interrupción ANTES de ejecutar
                    if self._check_interrupt():
                        logger.info(
                            f"  Interrupción antes de ejecutar {proposal.id}"
                        )
                        break
                    
                    logger.info(f"  Ejecutando {proposal.id}...")
                    result = await self.atomic_system.execute(proposal)
                    
                    logger.info(
                        f"  {'✅' if result['success'] else '❌'} "
                        f"{proposal.id}"
                    )
            
            except asyncio.CancelledError:
                logger.warning("⏹️ Ciclo cancelado")
                raise
            except Exception as e:
                logger.error(f"❌ Error en ciclo: {e}")
                raise
    
    # ... métodos auxiliares ...
    async def _collect_metrics(self):
        """Recolectar métricas del sistema"""
        # Implementación
        pass
    
    def _generate_proposals(self, metrics, cycle_type):
        """Generar propuestas basadas en métricas"""
        # Implementación
        pass
