"""Tests para Central Orchestrator."""

import pytest
import sys
import os
import tempfile
from pathlib import Path
from datetime import datetime

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from autonomous_intelligence.core.orchestrator import CentralOrchestrator

@pytest.fixture
def orchestrator():
    """Crea un CentralOrchestrator con almacenamiento temporal."""
    with tempfile.TemporaryDirectory() as tmpdir:
        orch = CentralOrchestrator(storage_root=Path(tmpdir))
        yield orch

class TestCentralOrchestrator:
    
    def test_run_cycle_with_no_data(self, orchestrator):
        """Verifica que el ciclo corre incluso sin datos (cero propuestas)."""
        result = orchestrator.run_improvement_cycle()
        
        assert result["proposals_generated"] == 0
        assert result["changes_applied"] == 0
        assert "timestamp" in result
    
    def test_run_cycle_with_mock_degradation(self, orchestrator):
        """Verifica el ciclo completo cuando hay una degradación detectable."""
        # Inyectar métricas de degradación en la memoria
        for i in range(14):
            orchestrator.memory.record_metric("Trading", "sharpe_ratio", 2.0)
        for i in range(14):
            orchestrator.memory.record_metric("Trading", "sharpe_ratio", 1.5) # Degradación 25%
            
        result = orchestrator.run_improvement_cycle()
        
        # Debería haber generado al menos una propuesta para Trading.sharpe_ratio
        assert result["proposals_generated"] > 0
        # Dado que es una degradación de Sharpe (trivial complexity), 
        # el Evaluator debería aprobarla.
        assert result["proposals_approved"] > 0
        assert result["changes_applied"] > 0
        
        # Verificar que se registró en el estado del sistema
        state = orchestrator.memory.get_system_state()
        assert "last_improvement_cycle" in state
        assert state["last_cycle_applied"] > 0
    
    def test_get_status(self, orchestrator):
        """Verifica que get_status devuelve información coherente."""
        orchestrator.run_improvement_cycle()
        status = orchestrator.get_status()
        
        assert "system_state" in status
        assert "recent_actions" in status
        assert len(status["recent_actions"]) > 0 # Al menos el fin del ciclo
