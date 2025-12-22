"""Tests para Change Evaluator."""

import pytest
import sys
import os
import tempfile
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from autonomous_intelligence.core.memory_manager import MemoryManager
from autonomous_intelligence.core.change_proposer import ChangeProposal
from autonomous_intelligence.core.change_evaluator import ChangeEvaluator

@pytest.fixture
def setup():
    """Inicializa MemoryManager y ChangeEvaluator."""
    with tempfile.TemporaryDirectory() as tmpdir:
        memory = MemoryManager(storage_root=Path(tmpdir))
        evaluator = ChangeEvaluator(memory)
        yield memory, evaluator

class TestChangeEvaluator:
    
    def test_approves_trivial_high_impact_proposal(self, setup):
        """Verifica que aprueba propuestas sencillas de alto impacto."""
        memory, evaluator = setup
        
        proposal = ChangeProposal(
            id="TEST-001",
            timestamp="2025-01-12T10:00:00Z",
            title="Ajuste trivial",
            component="Trading.barriers",
            current_value=2.0,
            proposed_value=2.5,
            justification="Mejora del 10%",
            impact_metrics={"sharpe": 0.12},
            priority="high",
            estimated_complexity="trivial"
        )
        
        result = evaluator.evaluate(proposal)
        assert result.approved is True
        assert result.overall_score > 0.80
    
    def test_rejects_complex_low_impact_proposal(self, setup):
        """Verifica que rechaza propuestas complejas de bajo impacto."""
        memory, evaluator = setup
        
        proposal = ChangeProposal(
            id="TEST-002",
            timestamp="2025-01-12T10:00:00Z",
            title="Cambio complejo",
            component="Oracle.model",
            current_value="v1",
            proposed_value="v2",
            justification="Mejora mínima",
            impact_metrics={"accuracy": 0.005},
            priority="low",
            estimated_complexity="complex"
        )
        
        result = evaluator.evaluate(proposal)
        assert result.approved is False
        assert result.overall_score < 0.50
    
    def test_reasoning_contains_key_metrics(self, setup):
        """Verifica que el razonamiento incluye los scores."""
        memory, evaluator = setup
        
        proposal = ChangeProposal(
            id="TEST-003",
            timestamp="2025-01-12T10:00:00Z",
            title="Test reasoning",
            component="Test",
            current_value=0,
            proposed_value=1,
            justification="Test",
            impact_metrics={},
            priority="medium",
            estimated_complexity="simple"
        )
        
        result = evaluator.evaluate(proposal)
        assert "Factibilidad" in result.reasoning
        assert "Impacto" in result.reasoning
        assert "Riesgo" in result.reasoning
        assert "Score final" in result.reasoning
