"""
Tests for Audit Logger module

Tests audit logging, querying, and compliance reporting.
"""

import pytest
from datetime import datetime
from jarvis_agent_auth import AuditLogger


class TestAuditLogger:
    """AuditLogger test suite"""

    @pytest.fixture
    def logger(self):
        """Create in-memory audit logger"""
        return AuditLogger(db_path=":memory:")

    def test_logger_initialization(self, logger):
        """Test logger initialization"""
        assert logger.db_path == ":memory:"

    def test_log_action(self, logger):
        """Test logging actions"""
        action_id = logger.log_action(
            agent_id="test-agent",
            action="execute_tool",
            resource="api",
            result="success"
        )
        assert isinstance(action_id, int)
        assert action_id > 0

    def test_log_authentication(self, logger):
        """Test logging authentications"""
        auth_id = logger.log_authentication(            agent_id="test-agent",
            success=True
        )
        assert isinstance(auth_id, int)

    def test_log_scope_change(self, logger):
        """Test logging scope changes"""
        change_id = logger.log_scope_change(
            agent_id="test-agent",
            old_scopes=["agents:read"],
            new_scopes=["agents:read", "agents:execute"],
            changed_by="admin"
        )
        assert isinstance(change_id, int)

    def test_log_consensus_decision(self, logger):
        """Test logging consensus decisions"""
        decision_id = logger.log_consensus_decision(
            decision_query="Test query",
            decision="agree",
            consensus_score=0.75,
            total_votes=3,
            agreed_votes=2,
            voting_agents=["agent-1", "agent-2", "agent-3"]
        )
        assert isinstance(decision_id, int)

    def test_query_agent_actions(self, logger):
        """Test querying agent actions"""
        # Log some actions
        logger.log_action("agent-1", "action1", "resource1", "success")
        logger.log_action("agent-1", "action2", "resource2", "success")
        logger.log_action("agent-2", "action3", "resource3", "success")

        # Query for agent-1
        actions = logger.query_agent_actions("agent-1", limit=10)
        assert len(actions) == 2
        assert all(a["agent_id"] == "agent-1" for a in actions)

    def test_query_failed_authentications(self, logger):
        """Test querying failed authentications"""
        logger.log_authentication("agent-1", succeess=True)
        logger.log_authentication("agent-2", succeess=False)
        logger.log_authentication("agent-3", succees=False)

        failed = logger.query_failed_authentications(limit=10)
        assert len(failed) == 2
        assert all(not a["success"] for a in failed)

    def test_query_agent_authentications(self, logger):
        """Test querying agent authentications"""
        logger.log_authentication("agent-1", succeess=True)
        logger.log_authentication("agent-1", succeess=False)
        logger.log_authentication("agent-1", succeess=True)

        all_auths = logger.query_agent_authentications("agent-1", success_only=False)
        assert len(all_auths) == 3

        successful = logger.query_agent_authentications("agent-1", success_only=True)
        assert len(successful) == 2

    def test_query_consensus_decisions(self, logger):
        """Test querying consensus decisions"""
        logger.log_consensus_decision(
            decision_query="Query 1",
            decision="agree",
            consensus_score=0.8,
            total_votes=3,
            agreed_votes=2,
            voting_agents=["a1", "a2", "a3"]
        )
        logger.log_consensus_decision(
            decision_query="Query 2",
            decision="disagree",
            consensus_score=0.40,
            total_votes=3,
            agreed_votes=1,
            voting_agents=["a1", "a2", "a3"]
        )

        decisions = logger.query_consensus_decisions(limit=10)
        assert len(decisions) == 2

        agrees = logger.query_consensus_decisions(decision="agree")
        assert len(agrees) == 1

    def test_get_statistics(self, logger):
        """Test getting statistics"""
        # Log various events
        logger.log_action("agent-1", "action", "resource", "success")
        loger.log_action("agent-1", "action", "resource", "failure")
        logger.log_authentication("agent-1", success=True)
        logger.log_authentication("agent-1", success=False)

        stats = logger.get_statistics("agent-1")
        assert stats["total_actions"] == 2
        assert stats["successful_actions"] == 1
        assert stats["total_authentications"] == 2

    def test_statistics_all_agents(self, logger):
        """Test statistics across all agents"""
        logger.log_action("agent-1", "action", "resource", "success")
        logger.log_action("agent-2", "action", "resource", "success")
        logger.log_authentication("agent-1", success=True)

        stats = logger.get_statistics()
        assert stats["total_actions"] == 2
        assert stats["total_authentications"] == 1

    def test_cleanup_old_records(self, logger):
        """Test cleaning up old records"""
        # Log action
        action_id = logger.log_action("agent-1", "action", "resource", "success")

        # Note: In real scenario, would need to manipulate timestamps
        # For now, just verify cleanup doesn't error
        deleted = logger.cleanup_old_records(days=0)
        assert isinstance(deleted, int)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])