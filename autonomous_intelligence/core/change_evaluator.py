"""
Change Evaluator - Puntúa propuestas antes de aplicarlas.
Usa criterios de factibilidad, impacto y riesgo.
"""
import logging
from typing import Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class EvaluationResult:
    """Resultado de evaluación de una propuesta."""
    proposal_id: str
    feasibility_score: float  # 0.0 - 1.0
    impact_score: float       # 0.0 - 1.0
    risk_score: float         # 0.0 - 1.0 (menor es mejor)
    overall_score: float      # 0.0 - 1.0
    approved: bool            # overall_score >= 0.70
    reasoning: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "feasibility": self.feasibility_score,
            "impact": self.impact_score,
            "risk": self.risk_score,
            "overall": self.overall_score,
            "approved": self.approved,
            "reasoning": self.reasoning
        }

class ChangeEvaluator:
    """
    Evalúa propuestas de cambio usando tres criterios ponderados:
    - Factibilidad (30%): ¿Se puede hacer sin romper nada?
    - Impacto (40%): ¿Mejora las métricas?
    - Riesgo (30%): ¿Qué puede salir mal?
    """
    APPROVAL_THRESHOLD = 0.70

    def __init__(self, memory_manager):
        self.memory = memory_manager
        logger.info("ChangeEvaluator inicializado")

    def evaluate(self, proposal) -> EvaluationResult:
        """
        Puntúa una propuesta de cambio.
        
        Args:
            proposal: ChangeProposal a evaluar
            
        Returns:
            EvaluationResult con scores y decisión
        """
        
        # 1. Evaluar Factibilidad (30%)
        feasibility = self._evaluate_feasibility(proposal)
        
        # 2. Evaluar Impacto (40%)
        impact = self._evaluate_impact(proposal)
        
        # 3. Evaluar Riesgo (30%)
        risk = self._evaluate_risk(proposal)
        
        # Combinar con pesos
        # overall = (factibilidad * 0.30) + (impacto * 0.40) + ((1 - riesgo) * 0.30)
        overall = (feasibility * 0.30) + (impact * 0.40) + ((1 - risk) * 0.30)
        
        approved = overall >= self.APPROVAL_THRESHOLD
        
        reasoning = self._build_reasoning(proposal, feasibility, impact, risk, overall)
        
        result = EvaluationResult(
            proposal_id=proposal.id,
            feasibility_score=feasibility,
            impact_score=impact,
            risk_score=risk,
            overall_score=overall,
            approved=approved,
            reasoning=reasoning
        )
        
        logger.info(f"Evaluated {proposal.id}: {result.overall_score:.2f} → {'APPROVED' if approved else 'REJECTED'}")
        
        return result

    def _evaluate_feasibility(self, proposal) -> float:
        """
        ¿Se puede implementar sin romper cosas?
        
        - Trivial: 0.95 (cambios de parámetros)
        - Simple: 0.80 (cambios de código aislado)
        - Moderate: 0.60 (cambios con dependencias)
        - Complex: 0.30 (cambios en core)
        """
        complexity_scores = {
            "trivial": 0.95,
            "simple": 0.80,
            "moderate": 0.60,
            "complex": 0.30
        }
        base_score = complexity_scores.get(proposal.estimated_complexity, 0.5)
        
        # Ajustar por dependencias (heurístico)
        if "model" in proposal.component.lower():
            # Cambios de modelo son arriesgados
            base_score *= 0.85
        
        if "barrier" in proposal.component.lower():
            # Cambios de barreras son más seguros
            base_score *= 1.05
        
        return min(1.0, base_score)

    def _evaluate_impact(self, proposal) -> float:
        """
        ¿Qué tan bueno es el impacto esperado?
        
        - Sin impact: 0.0
        - Pequeño (+1-5%): 0.4
        - Moderado (+5-10%): 0.7
        - Significativo (+10%+): 0.95
        """
        if not proposal.impact_metrics:
            return 0.3  # Por defecto, bajo
        
        # Tomar el promedio de impactos
        impacts = list(proposal.impact_metrics.values())
        avg_impact = sum(impacts) / len(impacts)
        
        if avg_impact > 0.10:
            return 0.95
        elif avg_impact > 0.05:
            return 0.70
        elif avg_impact > 0.01:
            return 0.40
        else:
            return 0.20

    def _evaluate_risk(self, proposal) -> float:
        """
        ¿Qué puede salir mal?
        
        - Bajo (0.1): cambios probados, con rollback
        - Moderado (0.5): cambios con cierto riesgo
        - Alto (0.8): cambios muy invasivos
        """
        risk_score = 0.2  # Base: bajo riesgo
        
        # Aumentar riesgo por complejidad
        if proposal.estimated_complexity == "complex":
            risk_score += 0.4
        elif proposal.estimated_complexity == "moderate":
            risk_score += 0.2
        
        # Reducir riesgo si impacto es mínimo
        max_impact = max(proposal.impact_metrics.values()) if proposal.impact_metrics else 0
        if max_impact < 0.02:
            risk_score *= 0.5
        
        # Prioridad alta = más riesgo aceptable
        if proposal.priority == "critical":
            risk_score *= 0.8
        
        return min(1.0, risk_score)

    def _build_reasoning(self, proposal, feasibility, impact, risk, overall) -> str:
        """Construye justificación de la evaluación."""
        lines = [
            f"Propuesta: {proposal.title}",
            f"Factibilidad: {feasibility:.2f} ({proposal.estimated_complexity})",
            f"Impacto esperado: {impact:.2f}",
            f"Riesgo: {risk:.2f}",
            f"Score final: {overall:.2f}/1.00"
        ]
        
        if overall >= self.APPROVAL_THRESHOLD:
            lines.append(f"✅ APROBADO (score >= {self.APPROVAL_THRESHOLD})")
        else:
            lines.append(f"❌ RECHAZADO (score < {self.APPROVAL_THRESHOLD})")
            lines.append(f"  Déficit: {(self.APPROVAL_THRESHOLD - overall):.2f} puntos")
        
        return "\n".join(lines)
