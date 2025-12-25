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
    """Propuesta inmutable de cambio (Study Plan V5)"""
    proposal_id: str
    title: str
    target_component: str
    impact_justification: str
    estimated_difficulty: str
    diff_content: str
    test_plan: str
    metrics: Dict[str, Any]

class ChangeProposer:
    """
    Genera propuestas de cambio.
    FASE 2: Solo hardcodeado (ATR).
    """
    def __init__(self, sentinel):
        """
        Args:
            sentinel: Instancia de ContextSentinel para persistencia
        """
        self.sentinel = sentinel
        logger.info("ChangeProposer (Fase 2) inicializado")

    def generate_atr_proposal(self) -> ChangeProposal:
        """
        Genera la propuesta hardcodeada de ATR para la Fase 2.
        """
        proposal = ChangeProposal(
            proposal_id="AIPHA-ATR-001",
            title="Optimización de ATR en PotentialCaptureEngine",
            target_component="trading_manager.building_blocks.labelers.potential_capture_engine",
            impact_justification="El Win Rate actual es del 15%. Se propone usar ATR dinámico para mejorar el filtrado de volatilidad.",
            estimated_difficulty="Baja",
            diff_content="+ self.atr = ATR(period=14)\n- self.fixed_threshold = 0.02",
            test_plan="Ejecutar tests/test_potential_capture_engine.py con datos de alta volatilidad.",
            metrics={"expected_win_rate_improvement": 0.07}
        )
        
        # Registrar la generación en la memoria
        self.sentinel.add_action(
            agent="ChangeProposer",
            action_type="PROPOSAL_GENERATED",
            proposal_id=proposal.proposal_id,
            details={"title": proposal.title}
        )
        
        return proposal

    def propose_changes(self) -> List[ChangeProposal]:
        """Legacy method for compatibility, returns the ATR proposal in Phase 2."""
        return [self.generate_atr_proposal()]
