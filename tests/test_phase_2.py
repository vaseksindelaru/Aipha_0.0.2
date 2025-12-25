import pytest
import tempfile
from pathlib import Path
from core.context_sentinel import ContextSentinel
from core.change_proposer import ChangeProposer, ChangeProposal
from core.change_evaluator import ProposalEvaluator, EvaluationResult

class TestPhase2:
    @pytest.fixture
    def sentinel(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield ContextSentinel(Path(tmpdir))

    def test_change_proposer_atr_proposal(self, sentinel):
        proposer = ChangeProposer(sentinel)
        proposal = proposer.generate_atr_proposal()
        
        assert isinstance(proposal, ChangeProposal)
        assert proposal.proposal_id == "AIPHA-ATR-001"
        assert "ATR" in proposal.title
        assert proposal.metrics["expected_win_rate_improvement"] == 0.07
        
        # Verificar que se registró la acción
        history = sentinel.get_action_history()
        assert len(history) == 1
        assert history[0]["action_type"] == "PROPOSAL_GENERATED"
        assert history[0]["proposal_id"] == "AIPHA-ATR-001"

    def test_proposal_evaluator_scoring(self, sentinel):
        proposer = ChangeProposer(sentinel)
        evaluator = ProposalEvaluator(sentinel)
        
        proposal = proposer.generate_atr_proposal()
        result = evaluator.evaluate(proposal)
        
        assert isinstance(result, EvaluationResult)
        assert result.score >= 0.70
        assert result.approved is True
        assert "Score Total" in result.reasoning
        
        # Verificar que se registró la acción
        history = sentinel.get_action_history()
        # 1 de la propuesta + 1 de la evaluación
        assert len(history) == 2
        assert history[1]["action_type"] == "PROPOSAL_EVALUATED"
        assert history[1]["details"]["approved"] is True

    def test_propose_changes_legacy_compatibility(self, sentinel):
        proposer = ChangeProposer(sentinel)
        proposals = proposer.propose_changes()
        assert len(proposals) == 1
        assert proposals[0].proposal_id == "AIPHA-ATR-001"
