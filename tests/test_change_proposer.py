"""Tests para Change Proposer (Fase 7 - Dinámico)."""

import pytest
import sys
import os
import tempfile
from pathlib import Path

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
    
    def test_propose_changes_with_low_trades(self, setup):
        """Verifica que genera propuesta Loosen Entry cuando no hay trades."""
        sentinel, proposer = setup
        
        # Simular estado sin trades
        sentinel.add_memory("trading_metrics", {
            "win_rate": 0.0,
            "total_trades": 0,
            "current_drawdown": 0.0
        })
        
        proposals = proposer.propose_changes()
        
        # Debería generar propuesta Loosen Entry
        assert len(proposals) == 1
        proposal = proposals[0]
        assert "AIPHA-DYN" in proposal.proposal_id
        assert "Sensibilidad" in proposal.title or "Entrada" in proposal.title
    
    def test_propose_changes_with_poor_performance(self, setup):
        """Verifica que genera propuesta Tighten Risk cuando hay bajo rendimiento."""
        sentinel, proposer = setup
        
        sentinel.add_memory("trading_metrics", {
            "win_rate": 0.25,
            "total_trades": 50,
            "current_drawdown": 0.2
        })
        
        proposals = proposer.propose_changes()
        
        assert len(proposals) == 1
        proposal = proposals[0]
        assert "Protección" in proposal.title or "Capital" in proposal.title
    
    def test_no_proposal_on_normal_metrics(self, setup):
        """Verifica que no genera propuestas cuando las métricas están en rango normal."""
        sentinel, proposer = setup
        
        sentinel.add_memory("trading_metrics", {
            "win_rate": 0.5,  # Normal
            "total_trades": 50,
            "current_drawdown": 0.05
        })
        
        proposals = proposer.propose_changes()
        
        # No debería generar propuestas en rango normal
        assert len(proposals) == 0
