"""
Change Proposer - Sugiere mejoras automáticamente basadas en métricas.
Usa análisis de tendencias para proponer cambios cuantitativos.
"""
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import uuid

logger = logging.getLogger(__name__)

@dataclass
class ChangeProposal:
    """Propuesta de cambio al sistema."""
    id: str
    timestamp: str
    title: str
    component: str
    current_value: Any
    proposed_value: Any
    justification: str  # DEBE incluir datos cuantitativos
    impact_metrics: Dict[str, float]  # {"metric_name": change_value}
    priority: str  # "low", "medium", "high", "critical"
    estimated_complexity: str  # "trivial", "simple", "moderate", "complex"

    def to_dict(self) -> Dict[str, Any]:
        """Serializa a diccionario."""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "title": self.title,
            "component": self.component,
            "current_value": str(self.current_value),
            "proposed_value": str(self.proposed_value),
            "justification": self.justification,
            "impact_metrics": self.impact_metrics,
            "priority": self.priority,
            "estimated_complexity": self.estimated_complexity
        }

class ChangeProposer:
    """
    Agente que sugiere cambios basado en análisis de métricas históricas.
    """
    def __init__(self, memory_manager):
        """
        Args:
            memory_manager: Instancia de MemoryManager para acceder a métricas
        """
        self.memory = memory_manager
        logger.info("ChangeProposer inicializado")

    def propose_changes(self, lookback_days: int = 7) -> List[ChangeProposal]:
        """
        Propone cambios basados en tendencias recientes.
        
        Args:
            lookback_days: Período de análisis (ej: últimos 7 días)
            
        Returns:
            Lista de propuestas de cambio ordenadas por prioridad
        """
        proposals = []
        
        # Analizar cada componente con métricas
        components_metrics = {
            "Oracle": ["win_rate", "accuracy"],
            "Trading": ["sharpe_ratio", "max_drawdown"],
            "Barriers": ["tp_factor", "sl_factor"]
        }
        
        for component, metrics in components_metrics.items():
            for metric_name in metrics:
                metric_data = self.memory.get_metrics(
                    component=component,
                    metric_name=metric_name,
                    limit=100  # Últimas 100 métricas
                )
                
                if len(metric_data) < 10:
                    continue  # Insuficientes datos
                
                # Análisis de tendencia
                recent_values = [m["value"] for m in metric_data[-14:]]
                older_values = [m["value"] for m in metric_data[-28:-14]]
                
                if not older_values:
                    continue
                
                recent_avg = sum(recent_values) / len(recent_values)
                older_avg = sum(older_values) / len(older_values)
                
                # Detectar degradación
                if older_avg > 0 and recent_avg < older_avg * 0.95:  # Bajó 5%
                    proposal = self._create_degradation_proposal(
                        component, metric_name, recent_avg, older_avg
                    )
                    if proposal:
                        proposals.append(proposal)
                
                # Detectar mejora consistente
                if recent_avg > older_avg * 1.05:  # Subió 5%
                    proposal = self._create_improvement_proposal(
                        component, metric_name, recent_avg, older_avg
                    )
                    if proposal:
                        proposals.append(proposal)
        
        # Ordenar por prioridad
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        proposals.sort(key=lambda p: priority_order.get(p.priority, 4))
        
        logger.info(f"Generated {len(proposals)} proposals")
        return proposals

    def _create_degradation_proposal(self, component: str, metric: str,
                                   recent_avg: float, older_avg: float) -> Optional[ChangeProposal]:
        """Propone cambio para recuperar métrica degradada."""
        
        # Mapping de degradaciones a cambios sugeridos
        if component == "Oracle" and metric == "win_rate":
            # La tasa de ganancia bajó → revisar features del modelo
            return ChangeProposal(
                id=f"AIPHA-{uuid.uuid4().hex[:6].upper()}",
                timestamp=datetime.utcnow().isoformat() + "Z",
                title="Mejorar Oracle: Win Rate degradado",
                component="Oracle.model",
                current_value="random_forest_v1",
                proposed_value="random_forest_v2_tuned",
                justification=f"Win Rate bajó de {older_avg:.2%} → {recent_avg:.2%} (últimos 14 días). "
                            f"Degradación: {(1 - recent_avg/older_avg)*100:.1f}%. "
                            f"Propuesta: Aumentar n_estimators de 100 → 200.",
                impact_metrics={"win_rate": +0.05},
                priority="high",
                estimated_complexity="moderate"
            )
        
        elif component == "Trading" and metric == "sharpe_ratio":
            # Sharpe bajó → ajustar barreras ATR
            return ChangeProposal(
                id=f"AIPHA-{uuid.uuid4().hex[:6].upper()}",
                timestamp=datetime.utcnow().isoformat() + "Z",
                title="Ajustar Barreras ATR: Sharpe degradado",
                component="Trading.barriers",
                current_value="tp_factor=2.0, sl_factor=1.0",
                proposed_value="tp_factor=2.5, sl_factor=1.2",
                justification=f"Sharpe bajó de {older_avg:.2f} → {recent_avg:.2f}. "
                            f"Mercado más volátil: aumentar tolerancia de barreras.",
                impact_metrics={"sharpe_ratio": +0.2},
                priority="medium",
                estimated_complexity="trivial"
            )
        
        return None

    def _create_improvement_proposal(self, component: str, metric: str,
                                   recent_avg: float, older_avg: float) -> Optional[ChangeProposal]:
        """Propone cambio para consolidar mejora observada."""
        
        if component == "Oracle" and metric == "accuracy":
            # Accuracy mejoró → incrementar confianza en decisiones
            return ChangeProposal(
                id=f"AIPHA-{uuid.uuid4().hex[:6].upper()}",
                timestamp=datetime.utcnow().isoformat() + "Z",
                title="Incrementar confianza en Oracle",
                component="Orchestrator.confidence_threshold",
                current_value=0.7,
                proposed_value=0.75,
                justification=f"Accuracy mejoró consistentemente: {older_avg:.2%} → {recent_avg:.2%}. "
                            f"Mejora: +{(recent_avg/older_avg - 1)*100:.1f}%. "
                            f"Aumentar threshold de aprobación automática.",
                impact_metrics={"automatic_approvals": +0.1},
                priority="low",
                estimated_complexity="trivial"
            )
        
        return None
