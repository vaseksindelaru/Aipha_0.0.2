"""Tests para Change Proposer."""

import pytest
import sys
import os
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.memory_manager import MemoryManager
from core.change_proposer import ChangeProposer

@pytest.fixture
def setup():
    """Inicializa MemoryManager y ChangeProposer."""
    with tempfile.TemporaryDirectory() as tmpdir:
        memory = MemoryManager(storage_root=Path(tmpdir))
        proposer = ChangeProposer(memory)
        yield memory, proposer

class TestChangeProposer:
    
    def test_detects_degradation(self, setup):
        """Propone cambio si métrica degrada."""
        memory, proposer = setup
        
        # Registrar 20 métricas: primero altas, luego bajas
        for i in range(14):
            memory.record_metric("Oracle", "win_rate", 0.85)
        for i in range(14):
            memory.record_metric("Oracle", "win_rate", 0.80)  # Bajó ~6%
        
        proposals = proposer.propose_changes()
        
        # Debe detectar degradación
        assert any("degradado" in p.title.lower() for p in proposals)
    
    def test_proposal_has_quantitative_justification(self, setup):
        """Verifica que justificación incluye datos cuantitativos."""
        memory, proposer = setup
        
        # Registrar degradación
        for i in range(14):
            memory.record_metric("Oracle", "win_rate", 0.90)
        for i in range(14):
            memory.record_metric("Oracle", "win_rate", 0.85)
        
        proposals = proposer.propose_changes()
        
        for proposal in proposals:
            # Justificación debe incluir números o porcentajes
            assert "%" in proposal.justification or "." in proposal.justification
    
    def test_detects_improvement(self, setup):
        """Propone cambio si métrica mejora."""
        memory, proposer = setup
        
        # Registrar mejora
        for i in range(14):
            memory.record_metric("Oracle", "accuracy", 0.80)
        for i in range(14):
            memory.record_metric("Oracle", "accuracy", 0.85) # Subió ~6%
            
        proposals = proposer.propose_changes()
        
        assert any("incrementar confianza" in p.title.lower() for p in proposals)
