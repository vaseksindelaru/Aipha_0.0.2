"""Tests para Central Orchestrator."""

import pytest
import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.orchestrator import CentralOrchestrator
from core.change_proposer import ChangeProposal

@pytest.fixture
def orchestrator():
    """Crea un CentralOrchestrator con almacenamiento temporal."""
    with tempfile.TemporaryDirectory() as tmpdir:
        orch = CentralOrchestrator(storage_root=Path(tmpdir))
        yield orch

class TestCentralOrchestrator:
    
    def test_run_cycle_with_no_data(self, orchestrator, monkeypatch):
        """Verifica que el ciclo corre incluso sin datos (cero propuestas)."""
        # Mockear ChangeProposer para devolver lista vacía
        monkeypatch.setattr(orchestrator.proposer, "propose_changes", lambda lookback_days=7: [])
        
        result = orchestrator.run_improvement_cycle()
        
        assert result["proposals_generated"] == 0
        assert result["changes_applied"] == 0
        assert "timestamp" in result
    
    def test_run_cycle_with_mock_proposal(self, orchestrator, monkeypatch):
        """Verifica el ciclo completo cuando hay una propuesta válida."""
        # Mockear ChangeProposer para devolver una propuesta válida
        proposal = ChangeProposal(
            proposal_id="TEST-ORCH-001",
            title="Test Proposal",
            target_component="core.dummy",
            impact_justification="Test",
            estimated_difficulty="Baja",
            diff_content="diff",
            test_plan="pytest",
            metrics={},
            priority="high",
            estimated_complexity="trivial"
        )
        monkeypatch.setattr(orchestrator.proposer, "propose_changes", lambda lookback_days=7: [proposal])
        
        # Mockear AtomicUpdateSystem para evitar ejecución real
        orchestrator.atomic_system.execute = MagicMock(return_value=(True, "Mock Success"))
        
        result = orchestrator.run_improvement_cycle()
        
        assert result["proposals_generated"] == 1
        assert result["proposals_approved"] == 1
        assert result["changes_applied"] == 1
        
        # Verificar que se registró en el estado del sistema usando ContextSentinel
        state = orchestrator.sentinel.query_memory("system_state")
        assert "last_improvement_cycle" in state
        assert state["last_cycle_applied"] == 1
    
    def test_get_status(self, orchestrator):
        """Verifica que get_status devuelve información coherente."""
        # Ejecutar un ciclo vacío para generar algo de historia
        orchestrator.run_improvement_cycle()
        
        status = orchestrator.get_status()
        
        assert "system_state" in status
        assert "recent_actions" in status
        assert len(status["recent_actions"]) > 0 # Al menos el fin del ciclo
