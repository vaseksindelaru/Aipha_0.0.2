"""Tests para Change Evaluator (Fase 2)."""

import pytest
import sys
import os
import tempfile
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.context_sentinel import ContextSentinel
from core.change_proposer import ChangeProposal
from core.change_evaluator import ProposalEvaluator

@pytest.fixture
def setup():
    """Inicializa ContextSentinel y ProposalEvaluator."""
    with tempfile.TemporaryDirectory() as tmpdir:
        sentinel = ContextSentinel(storage_root=Path(tmpdir))
        evaluator = ProposalEvaluator(sentinel)
        yield sentinel, evaluator

class TestChangeEvaluator:
    
    def test_approves_proposal_with_metrics(self, setup):
        """Verifica que aprueba propuestas con métricas."""
        sentinel, evaluator = setup
        
        proposal = ChangeProposal(
            proposal_id="TEST-001",
            title="Ajuste trivial",
            target_component="Trading.barriers",
            impact_justification="Mejora del 10%",
            estimated_difficulty="Baja",
            diff_content="diff",
            test_plan="pytest",
            metrics={"sharpe": 0.12},
            priority="high",
            estimated_complexity="trivial"
        )
        
        metrics = {"win_rate": 0.30, "current_drawdown": 0.05}
        result = evaluator.evaluate(proposal, metrics)
        assert result.approved is True
        # Con WR 30% e Impacto 0.85, más multiplicador x1.10, el score debe ser alto
        assert result.score > 0.80
    
    def test_crisis_multiplier_critical(self, setup):
        """Verifica el efecto del multiplicador de crisis (x1.25)."""
        sentinel, evaluator = setup
        
        proposal = ChangeProposal(
            proposal_id="TEST-CRIT",
            title="Urgente",
            target_component="Risk",
            impact_justification="Crisis",
            estimated_difficulty="Media",
            diff_content="diff",
            test_plan="pytest",
            metrics={},
            priority="critical",
            estimated_complexity="moderate"
        )
        
        metrics = {"win_rate": 0.30, "current_drawdown": 0.20}
        result = evaluator.evaluate(proposal, metrics)
        
        assert "Multiplicador Crisis: x1.25" in result.reasoning
        assert result.score >= 0.70 # Debería ser aprobado por el multiplicador
    
    def test_reasoning_contains_hito3_info(self, setup):
        """Verifica que el razonamiento incluye información del Hito 3."""
        sentinel, evaluator = setup
        
        proposal = ChangeProposal(
            proposal_id="TEST-003",
            title="Test reasoning",
            target_component="Test",
            impact_justification="Test",
            estimated_difficulty="Media",
            diff_content="diff",
            test_plan="pytest",
            metrics={},
            priority="normal",
            estimated_complexity="simple"
        )
        
        result = evaluator.evaluate(proposal, {"win_rate": 0.5})
        assert "Evaluación Hito 3" in result.reasoning
        assert "Impacto (35%)" in result.reasoning
        assert "Multiplicador Crisis" in result.reasoning
