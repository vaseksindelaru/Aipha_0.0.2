"""
Central Orchestrator - Dirige el ciclo de automejora de Aipha.
Orquesta: MemoryManager → ChangeProposer → ChangeEvaluator → Acción
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import time

from core.context_sentinel import ContextSentinel
from core.change_proposer import ChangeProposer
from core.change_evaluator import ProposalEvaluator
from core.atomic_update_system import AtomicUpdateSystem
from core.config_manager import ConfigManager
from core.alerts import AlertsSystem

logger = logging.getLogger(__name__)

class CentralOrchestrator:
    """
    Núcleo autónomo de Aipha.
    Ejecuta el ciclo: Recolectar → Proponer → Evaluar → Decidir → Registrar
    """
    
    def __init__(self, storage_root: Path = Path("memory"), use_llm: bool = False):
        self.storage_root = Path(storage_root)
        self.use_llm = use_llm
        
        # Inicializar componentes
        self.sentinel = ContextSentinel(storage_root=self.storage_root)
        self.config = ConfigManager(config_path=self.storage_root / "aipha_config.json")
        
        # Seleccionar proposer según configuración
        if use_llm:
            try:
                from core.llm_proposer import LLMProposer
                self.proposer = LLMProposer(self.sentinel)
                logger.info("🧠 Usando LLMProposer")
            except Exception as e:
                logger.warning(f"No se pudo cargar LLMProposer ({e}), usando heurísticas")
                self.proposer = ChangeProposer(self.sentinel)
        else:
            self.proposer = ChangeProposer(self.sentinel)
        
        self.evaluator = ProposalEvaluator(self.sentinel)
        self.atomic_system = AtomicUpdateSystem(self.sentinel)
        self.alerts = AlertsSystem(memory_manager=self.sentinel)
        
        # Inicializar información del sistema
        self.sentinel.add_memory("system_info", {
            "version": "0.0.2",
            "mode": "AUTONOMOUS_LLM" if use_llm else "AUTONOMOUS",
            "last_boot": datetime.utcnow().isoformat() + "Z"
        })
        
        logger.info("🤖 CentralOrchestrator inicializado")
    
    def run_improvement_cycle(self, lookback_days: int = 7) -> Dict[str, Any]:
        """
        Ejecuta un ciclo completo de automejora.
        
        Args:
            lookback_days: Período de análisis de métricas
            
        Returns:
            Resumen del ciclo (propuestas, aprobaciones, acciones)
        """
        logger.info("═" * 60)
        logger.info("🔄 INICIANDO CICLO DE AUTOMEJORA")
        logger.info("═" * 60)
        
        cycle_start = datetime.utcnow()
        
        # PASO 1: Recolectar métricas (Simulado por ahora)
        logger.info("\n[PASO 1] Recolectando métricas...")
        metrics_summary = self._collect_metrics()
        
        # PASO 2: Proponer cambios
        logger.info("\n[PASO 2] Generando propuestas de cambio...")
        proposals = self.proposer.propose_changes(lookback_days=lookback_days)
        logger.info(f"  → {len(proposals)} propuestas generadas")
        
        # PASO 3: Evaluar propuestas
        logger.info("\n[PASO 3] Evaluando propuestas...")
        evaluations = []
        for proposal in proposals:
            evaluation = self.evaluator.evaluate(proposal)
            evaluations.append(evaluation)
            logger.info(f"  → {proposal.proposal_id}: {evaluation.score:.2f} → {'✅' if evaluation.approved else '❌'}")
        
        # PASO 4: Decidir e implementar
        logger.info("\n[PASO 4] Implementando cambios aprobados...")
        approved_proposals = [p for p, e in zip(proposals, evaluations) if e.approved]
        
        if not approved_proposals and proposals:
            self.alerts.warning("Ciclo sin cambios", "Se generaron propuestas pero ninguna fue aprobada por el Evaluador.")
        
        actions_taken = 0
        for proposal in approved_proposals:
            success, message = self.atomic_system.execute(proposal)
            if success:
                actions_taken += 1
                self.alerts.info("Cambio Aplicado", f"Se aplicó el cambio {proposal.proposal_id} en {proposal.target_component}")
                logger.info(f"  ✅ Aplicado: {proposal.proposal_id} - {message}")
            else:
                self.alerts.critical("Fallo en Aplicación", f"No se pudo aplicar el cambio {proposal.proposal_id}")
                logger.warning(f"  ❌ Fallo: {proposal.proposal_id} - {message}")
        
        # PASO 5: Registrar ciclo
        logger.info("\n[PASO 5] Registrando ciclo...")
        cycle_duration = (datetime.utcnow() - cycle_start).total_seconds()
        
        self.sentinel.add_memory("system_state", {
            "last_improvement_cycle": cycle_start.isoformat() + "Z",
            "last_cycle_proposals": len(proposals),
            "last_cycle_approved": len(approved_proposals),
            "last_cycle_applied": actions_taken,
            "last_cycle_duration_seconds": cycle_duration
        })
        
        self.sentinel.add_action(
            agent="CentralOrchestrator",
            action_type="improvement_cycle_completed",
            details={
                "proposals_generated": len(proposals),
                "proposals_approved": len(approved_proposals),
                "changes_applied": actions_taken,
                "duration_seconds": cycle_duration
            }
        )
        
        # Resumen final
        logger.info("\n" + "═" * 60)
        logger.info("📊 RESUMEN DEL CICLO")
        logger.info("═" * 60)
        logger.info(f"⏱️  Duración: {cycle_duration:.1f}s")
        logger.info(f"📝 Propuestas generadas: {len(proposals)}")
        logger.info(f"✅ Propuestas aprobadas: {len(approved_proposals)}")
        logger.info(f"🔧 Cambios aplicados: {actions_taken}")
        logger.info("═" * 60 + "\n")
        
        return {
            "timestamp": cycle_start.isoformat() + "Z",
            "proposals_generated": len(proposals),
            "proposals_approved": len(approved_proposals),
            "changes_applied": actions_taken,
            "duration_seconds": cycle_duration
        }
    
    def _collect_metrics(self) -> Dict[str, Any]:
        """
        Simulación de recolección de métricas desde Capas 2-5.
        En producción, esto consultaría las APIs de cada capa.
        """
        state = self.sentinel.query_memory("system_state") or {}
        return {
            "oracle_metrics_collected": True,
            "trading_metrics_collected": True,
            "system_state": state
        }
    
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene estado actual del sistema."""
        state = self.sentinel.query_memory("system_state")
        history = self.sentinel.get_action_history()
        
        return {
            "system_state": state,
            "recent_actions": history[-10:] if history else []
        }

if __name__ == "__main__":
    # Configurar logging para ejecución directa
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    
    orchestrator = CentralOrchestrator()
    orchestrator.run_improvement_cycle()
