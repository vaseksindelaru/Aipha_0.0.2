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
    
    def test_approves_proposal(self, setup):
        """
        Verifica que aprueba propuestas.
        NOTA: En Fase 2, la lógica de evaluación está hardcodeada para aprobar
        siempre con un score alto (basado en el caso de uso ATR).
        """
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
        
        result = evaluator.evaluate(proposal)
        assert result.approved is True
        assert result.score > 0.70
    
    def test_reasoning_contains_key_metrics(self, setup):
        """Verifica que el razonamiento incluye los scores."""
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
            priority="medium",
            estimated_complexity="simple"
        )
        
        result = evaluator.evaluate(proposal)
        # Verificar palabras clave en español como están en change_evaluator.py
        assert "Impacto" in result.reasoning
        assert "Dificultad" in result.reasoning
        assert "Riesgo" in result.reasoning
        assert "Complejidad" in result.reasoning
