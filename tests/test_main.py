import pytest
from datetime import timedelta, datetime
from app.auth.token import create_access_token
from app.core.config import settings
import jwt


@pytest.mark.anyio
async def test_check(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }


@pytest.mark.anyio
async def test_create_access_token():
    test_data = {"sub": "test@example.com"}
    token = create_access_token(test_data)
    assert token is not None

    expires_at = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert payload["exp"] == int(expires_at.timestamp())
