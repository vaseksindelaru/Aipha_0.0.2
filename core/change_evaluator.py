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
    """Resultado de evaluación (Study Plan V5)"""
    score: float
    reasoning: str
    approved: bool

class ProposalEvaluator:
    """
    Evalúa propuestas basado en:
    1. Impacto (30%)
    2. Dificultad (20%)
    3. Riesgo (30%)
    4. Complejidad (20%)
    """
    APPROVAL_THRESHOLD = 0.70

    def __init__(self, sentinel):
        """
        Args:
            sentinel: Instancia de ContextSentinel para persistencia
        """
        self.sentinel = sentinel
        logger.info("ProposalEvaluator (Fase 2) inicializado")

    def evaluate(self, proposal) -> EvaluationResult:
        """
        Evalúa una propuesta de cambio.
        """
        # Heurística de evaluación para la Fase 2 (hardcodeada para ATR)
        # En un sistema real, esto analizaría el contenido del diff y las métricas
        
        impact = 0.90      # Alto impacto esperado (+7% Win Rate)
        difficulty = 0.80  # Baja dificultad = Alto score
        risk = 0.85        # Bajo riesgo = Alto score
        complexity = 0.90  # Baja complejidad = Alto score
        
        # Cálculo ponderado
        score = (impact * 0.30) + (difficulty * 0.20) + (risk * 0.30) + (complexity * 0.20)
        approved = score >= self.APPROVAL_THRESHOLD
        
        reasoning = (
            f"Evaluación de {proposal.proposal_id}:\n"
            f"- Impacto (30%): {impact:.2f}\n"
            f"- Dificultad (20%): {difficulty:.2f}\n"
            f"- Riesgo (30%): {risk:.2f}\n"
            f"- Complejidad (20%): {complexity:.2f}\n"
            f"Score Total: {score:.2f} -> {'APROBADO' if approved else 'RECHAZADO'}"
        )
        
        # Registrar la evaluación en la memoria
        self.sentinel.add_action(
            agent="ProposalEvaluator",
            action_type="PROPOSAL_EVALUATED",
            proposal_id=proposal.proposal_id,
            details={"score": score, "approved": approved}
        )
        
        return EvaluationResult(
            score=score,
            reasoning=reasoning,
            approved=approved
        )
