import time

import jwt

_JWT_SECRET = "test-secret-key-at-least-32-bytes-long"
_JWT_ALGORITHM = "HS256"


def make_auth_header(*permissions: str) -> dict[str, str]:
    """Build an Authorization header with a valid JWT containing the given permissions."""
    payload = {
        "sub": "user-1",
        "username": "testuser",
        "permissions": list(permissions),
        "exp": int(time.time()) + 3600,
    }
    token = jwt.encode(payload, _JWT_SECRET, algorithm=_JWT_ALGORITHM)
    return {"Authorization": f"Bearer {token}"}
