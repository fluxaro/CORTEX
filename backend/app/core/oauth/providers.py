"""OAuth provider integrations for GitHub, GitLab, and Bitbucket."""

from typing import Any


class BaseOAuthProvider:
    """Abstract base OAuth provider."""

    @property
    def provider_name(self) -> str:
        raise NotImplementedError

    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        raise NotImplementedError

    async def exchange_code_for_user(
        self, code: str, redirect_uri: str
    ) -> dict[str, Any]:
        raise NotImplementedError


class GitHubOAuthProvider(BaseOAuthProvider):
    """GitHub OAuth provider."""

    @property
    def provider_name(self) -> str:
        return "GITHUB"

    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        client_id = "mock_github_client_id"
        return (
            f"https://github.com/login/oauth/authorize?"
            f"client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope=user:email,repo"
        )

    async def exchange_code_for_user(
        self, code: str, redirect_uri: str
    ) -> dict[str, Any]:
        return {
            "provider": "GITHUB",
            "external_id": "gh-12345",
            "email": "user@github.com",
            "name": "GitHub User",
            "avatar_url": "https://github.com/identicons/user.png",
        }


class GitLabOAuthProvider(BaseOAuthProvider):
    """GitLab OAuth provider."""

    @property
    def provider_name(self) -> str:
        return "GITLAB"

    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        client_id = "mock_gitlab_client_id"
        return (
            f"https://gitlab.com/oauth/authorize?"
            f"client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&state={state}&scope=read_user+api"
        )

    async def exchange_code_for_user(
        self, code: str, redirect_uri: str
    ) -> dict[str, Any]:
        return {
            "provider": "GITLAB",
            "external_id": "gl-67890",
            "email": "user@gitlab.com",
            "name": "GitLab User",
            "avatar_url": "https://gitlab.com/identicons/user.png",
        }


class BitbucketOAuthProvider(BaseOAuthProvider):
    """Bitbucket OAuth provider."""

    @property
    def provider_name(self) -> str:
        return "BITBUCKET"

    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        client_id = "mock_bitbucket_client_id"
        return (
            f"https://bitbucket.org/site/oauth2/authorize?"
            f"client_id={client_id}&response_type=code&state={state}"
        )

    async def exchange_code_for_user(
        self, code: str, redirect_uri: str
    ) -> dict[str, Any]:
        return {
            "provider": "BITBUCKET",
            "external_id": "bb-54321",
            "email": "user@bitbucket.org",
            "name": "Bitbucket User",
            "avatar_url": "https://bitbucket.org/identicons/user.png",
        }


class OAuthProviderFactory:
    """Factory to retrieve configured OAuth provider."""

    _providers = {
        "GITHUB": GitHubOAuthProvider(),
        "GITLAB": GitLabOAuthProvider(),
        "BITBUCKET": BitbucketOAuthProvider(),
    }

    @classmethod
    def get_provider(cls, provider: str) -> BaseOAuthProvider:
        prov = cls._providers.get(provider.upper())
        if not prov:
            raise ValueError(f"Unsupported OAuth provider: {provider}")
        return prov
