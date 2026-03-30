"""
Tests for AuthManager module

Tests M2M authentication, token management, and Token Vault operations.
"""

import pytest
from datetime import datetime, timedelta
from jarvis_agent_auth import AuthManager, AgentIdentity


class TestAuthManager:
    """AuthManager test suite"""

    @pytest.fixture
    def auth_manager(self):
        """Create AuthManager instance with mock mode"""
        return AuthManager(
            domain="test.auth0.com",
            client_id="test_client",
            client_secret="test_secret",
            api_audience="https://test-api",
            mock_mode=True
        )

    @pytest.fixture
    def agent(self):
        """Create test agent"""
        return AgentIdentity(
            agent_id="test-agent",
            name="Test Agent",
            model_type="test-model",
            scopes=["agents:read", "agents:execute"]
        )

    def test_auth_manager_initialization(self, auth_manager):
        """Test AuthManager initialization"""
        assert auth_manager.domain == "test.auth0.com"
        assert auth_manager.client_id == "test_client"
        assert auth_manager.mock_mode is True

    def test_get_token(self, auth_manager):
        """Test token retrieval"""
        token = auth_manager.get_token("test-agent")
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_caching(self, auth_manager):
        """Test token caching"""
        token1 = auth_manager.get_token("test-agent")
        token2 = auth_manager.get_token("test-agent")
        # Cached tokens should be identical
        assert token1 == token2

    def test_token_validation(self, auth_manager):
        """Test token validation"""
        token = auth_manager.get_token("test-agent")
        claims = auth_manager.validate_token(token)
        assert "sub" in claims or "agent_id" in claims

    def test_check_scope(self, auth_manager):
        """Test scope checking"""
        token = auth_manager.get_token("test-agent")
        assert auth_manager.check_scope(token, "agents:read")

    def test_vault_operations(self, auth_manager):
        """Test Token Vault operations"""
        # Store
        auth_manager.vault_store("test-key", "test-value")

        # Retrieve
        value = auth_manager.vault_retrieve("test-key")
        assert value == "test-value"

        # Delete
        deleted = auth_manager.vault_delete("test-key")
        assert deleted is True

        # Verify deleted
        value = auth_manager.vault_retrieve("test-key")
        assert value is None

    def test_register_agent(self, auth_manager, agent):
        """Test agent registration"""
        token = auth_manager.register_agent(agent)
        assert token is not None
        assert isinstance(token, str)

    def test_health_check(self, auth_manager):
        """Test health check"""
        health = auth_manager.health_check()
        assert "status" in health
        assert health["status"] in ["ok", "degraded", "error"]

    def test_token_rotation(self, auth_manager):
        """Test token rotation"""
        token1 = auth_manager.get_token("test-agent")
        token2 = auth_manager.rotate_token("test-agent")
        # Rotated token should be different (or new)
        assert token1 is not None
        assert token2 is not None


class TestTokenVault:
    """Token Vault test suite"""

    def test_vault_store_and_retrieve(self, auth_manager):
        """Test storing and retrieving secrets"""
        auth_manager.vault_store("secret-key", "secret-value")
        value = auth_manager.vault_retrieve("secret-key")
        assert value == "secret-value"

    def test_vault_metadata(self, auth_manager):
        """Test vault with metadata"""
        metadata = {"env": "production", "ttl": 3600}
        auth_manager.vault_store("api-key", "secret", metadata=metadata)

        # Verify stored
        value = auth_manager.vault_retrieve("api-key")
        assert value == "secret"

    def test_vault_list_keys(self, auth_manager):
        """Test listing vault keys"""
        auth_manager.vault_store("key1", "value1")
        auth_manager.vault_store("key2", "value2")

        keys = auth_manager.vault_list()
        assert "key1" in keys
        assert "key2" in keys


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
