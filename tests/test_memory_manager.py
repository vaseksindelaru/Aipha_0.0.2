"""
Tests para Memory Manager.
Verificar: persistencia, integridad, append-only.
"""

import pytest
import tempfile
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Añadir el directorio raíz al path para importar core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.memory_manager import MemoryManager, ActionEntry

@pytest.fixture
def memory_manager():
    """Crea un MemoryManager con almacenamiento temporal."""
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = MemoryManager(storage_root=Path(tmpdir))
        yield manager

class TestMemoryManager:
    
    def test_record_and_retrieve_action(self, memory_manager):
        """Prueba que se registran y recuperan acciones."""
        hash1 = memory_manager.record_action(
            agent="TestAgent",
            component="TestComponent",
            action="test_action",
            details={"key": "value"}
        )
        
        history = memory_manager.get_action_history()
        assert len(history) == 1
        assert history[0]["agent"] == "TestAgent"
        assert history[0]["entry_hash"] == hash1
    
    def test_append_only_property(self, memory_manager):
        """Verifica que el historial es append-only."""
        # Registrar 3 acciones
        for i in range(3):
            memory_manager.record_action(
                agent="Agent",
                component="Comp",
                action=f"action_{i}",
                details={}
            )
        
        history1 = memory_manager.get_action_history()
        assert len(history1) == 3
        
        # Agregar una más
        memory_manager.record_action(
            agent="Agent",
            component="Comp",
            action="action_3",
            details={}
        )
        
        history2 = memory_manager.get_action_history()
        assert len(history2) == 4
    
    def test_metric_recording(self, memory_manager):
        """Prueba que se registran métricas."""
        memory_manager.record_metric(
            component="Oracle",
            metric_name="win_rate",
            value=0.85,
            metadata={"dataset": "test"}
        )
        
        metrics = memory_manager.get_metrics(component="Oracle")
        assert len(metrics) == 1
        assert metrics[0]["value"] == 0.85
    
    def test_system_state_update(self, memory_manager):
        """Prueba actualización de estado del sistema."""
        memory_manager.update_system_state({
            "phase": 1,
            "status": "running"
        })
        
        state = memory_manager.get_system_state()
        assert state["phase"] == 1
        assert state["status"] == "running"
        assert "last_update" in state
    
    def test_action_entry_hash_integrity(self):
        """Verifica que los hashes son determinísticos."""
        entry1 = ActionEntry(
            timestamp="2025-01-12T10:00:00Z",
            agent="Test",
            component="Comp",
            action="action",
            status="success",
            details={"a": 1}
        )
        
        hash1 = entry1.compute_hash()
        hash2 = entry1.compute_hash()
        assert hash1 == hash2  # Determinístico
