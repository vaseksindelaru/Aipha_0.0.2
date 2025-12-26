"""Tests para Change Proposer (Fase 2)."""

import pytest
import sys
import os
import tempfile
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from core.context_sentinel import ContextSentinel
from core.change_proposer import ChangeProposer

@pytest.fixture
def setup():
    """Inicializa ContextSentinel y ChangeProposer."""
    with tempfile.TemporaryDirectory() as tmpdir:
        sentinel = ContextSentinel(storage_root=Path(tmpdir))
        proposer = ChangeProposer(sentinel)
        yield sentinel, proposer

class TestChangeProposer:
    
    def test_generate_atr_proposal(self, setup):
        """Verifica que genera la propuesta ATR hardcodeada de Fase 2."""
        sentinel, proposer = setup
        
        proposals = proposer.propose_changes()
        
        assert len(proposals) == 1
        proposal = proposals[0]
        assert proposal.proposal_id == "AIPHA-ATR-001"
        assert "ATR" in proposal.title
        assert proposal.target_component == "trading_manager.building_blocks.labelers.potential_capture_engine"
        
        # Verificar que se registró en memoria
        history = sentinel.get_action_history()
        assert any(h["action_type"] == "PROPOSAL_GENERATED" for h in history)
