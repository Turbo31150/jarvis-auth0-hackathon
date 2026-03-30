"""
JARVIS AgentAuth - Secure Multi-Agent Orchestrator using Auth0 Token Vault

A production-ready framework for orchestrating multiple AI agents with
enterprise-grade security, authentication, and consensus voting.
"""

__version__ = "1.0.0"
__author__ = "JARVIS AgentAuth Team"
__all__ = [
    "AuthManager",
    "AgentIdentity",
    "ConsensusVoter",
    "MCPMiddleware",
    "AuditLogger",
    "TokenVaultError",
    "AuthenticationError",
    "AuthorizationError",
    "ConsensusError",
]

from .auth_manager import AuthManager
from .agent_identity import AgentIdentity
from .consensus_auth import ConsensusVoter
from .mcp_middleware import MCPMiddleware
from .audit_logger import AuditLogger

# Custom Exceptions
class TokenVaultError(Exception):
    """Raised when Token Vault operation fails"""
    pass


class AuthenticationError(Exception):
    """Raised when agent authentication fails"""
    pass


class AuthorizationError(Exception):
    """Raised when agent lacks required scopes"""
    pass


class ConsensusError(Exception):
    """Raised when consensus voting fails"""
    pass
