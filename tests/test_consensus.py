"""
Tests for Consensus Voting module

Tests N-of-M voting, weighted consensus, and decision logic.
"""

import pytest
from jarvis_agent_auth import (
    AuthManager,
    AgentIdentity,
    ConsensusVoter
)


class TestConsensusVoter:
    """ConsensusVoter test suite"""

    @pytest.fixture
    def auth_manager(self):
        """Create AuthManager with mock mode"""
        return AuthManager(
            domain="test.auth0.com",
            client_id="test_client",
            client_secret="test_secret",
            api_audience="https://test-api",
            mock_mode=True
        )

    @pytest.fixture
    def agents(self):
        """Create test agents"""
        return [
            AgentIdentity(
                agent_id=f"agent-{i}",
                name=f"Agent {i}",
                model_type="test-model",
                scopes=["agents:read", "agents:vote"]
            )
            for i in range(5)
        ]

    @pytest.fixture
    def voter(self, auth_manager, agents):
        """Create consensus voter"""
        return ConsensusVoter(
            agents=agents,
            auth_manager=auth_manager,
            required_votes=3,
            weights={agent.agent_id: 1.0 for agent in agents}
        )

    def test_voter_initialization(self, voter, agents):
        """Test voter initialization"""
        assert len(voter.agents) == 5
        assert voter.required_votes == 3
        assert voter.min_consensus_threshold == 0.6

    def test_vote_and_decide(self, voter):
        """Test consensus voting"""
        result = voter.vote_and_decide(
            decision_query="Test query"
        )
        assert result.decision in ["agree", "disagree", "inconclusive"]
        assert 0 <= result.consensus_score <= 1
        assert result.total_votes >= voter.required_votes

    def test_weighted_voting(self, auth_manager, agents):
        """Test weighted voting calculation"""
        weights = {
            agents[0].agent_id: 2.0,  # Double weight
            agents[1].agent_id: 1.0,
            agents[2].agent_id: 1.0,
            agents[3].agent_id: 1.0,
            agents[4].agent_id: 1.0,
        }

        voter = ConsensusVoter(
            agents=agents,
            auth_manager=auth_manager,
            required_votes=3,
            weights=weights
        )

        result = voter.vote_and_decide("Test query")
        assert result.weighted_score is not None

    def test_decision_history(self, voter):
        """Test decision history tracking"""
        assert len(voter.get_decision_history()) == 0

        voter.vote_and_decide("Query 1")
        assert len(voter.get_decision_history()) == 1

        voter.vote_and_decide("Query 2")
        assert len(voter.get_decision_history()) == 2

    def test_agent_voting_stats(self, voter, agents):
        """Test agent voting statistics"""
        voter.vote_and_decide("Test query")

        stats = voter.get_agent_voting_stats(agents[0].agent_id)
        assert stats["agent_id"] == agents[0].agent_id
        assert stats["total_votes"] >= 1

    def test_insufficient_votes(self, auth_manager, agents):
        """Test error when insufficient votes"""
        voter = ConsensusVoter(
            agents=agents[:1],  # Only 1 agent
            auth_manager=auth_manager,
            required_votes=3  # But need 3
        )

        with pytest.raises(ValueError):
            voter.vote_and_decide("Test query")

    def test_step_up_authentication(self, voter):
        """Test step-up authentication"""
        result = voter.vote_and_decide(
            decision_query="High stakes decision",
            step_up_auth_required=True
        )
        assert result.step_up_auth_used is True

    def test_clear_history(self, voter):
        """Test clearing history"""
        voter.vote_and_decide("Query 1")
        voter.vote_and_decide("Query 2")
        assert len(voter.get_decision_history()) == 2

        voter.clear_history()
        assert len(voter.get_decision_history()) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])