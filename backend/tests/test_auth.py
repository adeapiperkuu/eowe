from datetime import datetime, timezone

from tests.conftest import TEST_PASSWORD


def test_login_success_issues_access_token_and_refresh_cookie(client, test_user):
    r = client.post(
        "/api/v1/auth/login", json={"email": test_user.email, "password": TEST_PASSWORD}
    )
    assert r.status_code == 200
    body = r.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert "refresh_token" in r.cookies


def test_login_wrong_password_uniform_error(client, test_user):
    r = client.post("/api/v1/auth/login", json={"email": test_user.email, "password": "wrong"})
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid email or password"


def test_login_unknown_email_uniform_error(client):
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "nobody-xyz@example.com", "password": "whatever12345"},
    )
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid email or password"


def test_login_inactive_user_rejected(client, db_session, test_user):
    test_user.is_active = False
    db_session.flush()
    r = client.post(
        "/api/v1/auth/login", json={"email": test_user.email, "password": TEST_PASSWORD}
    )
    assert r.status_code == 401


def test_login_soft_deleted_user_rejected(client, db_session, test_user):
    test_user.deleted_at = datetime.now(timezone.utc)
    db_session.flush()
    r = client.post(
        "/api/v1/auth/login", json={"email": test_user.email, "password": TEST_PASSWORD}
    )
    assert r.status_code == 401


def test_login_rejects_extra_fields(client, test_user):
    r = client.post(
        "/api/v1/auth/login",
        json={"email": test_user.email, "password": TEST_PASSWORD, "role": "admin"},
    )
    assert r.status_code == 422  # extra="forbid"


def test_me_requires_token(client):
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 401


def test_me_rejects_garbage_token(client):
    r = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer garbage.token.value"})
    assert r.status_code == 401


def test_me_with_valid_token_returns_user(client, test_user):
    login = client.post(
        "/api/v1/auth/login", json={"email": test_user.email, "password": TEST_PASSWORD}
    )
    token = login.json()["access_token"]
    r = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    body = r.json()
    assert body["email"] == test_user.email
    assert body["role"]["code"] == "admin"


def test_refresh_without_cookie_rejected(client):
    r = client.post("/api/v1/auth/refresh")
    assert r.status_code == 401


def test_refresh_rotates_and_issues_new_access_token(client, test_user):
    client.post("/api/v1/auth/login", json={"email": test_user.email, "password": TEST_PASSWORD})
    r = client.post("/api/v1/auth/refresh")
    assert r.status_code == 200
    assert r.json()["access_token"]


def test_refresh_reuse_of_rotated_out_token_rejected(client, test_user):
    login = client.post(
        "/api/v1/auth/login", json={"email": test_user.email, "password": TEST_PASSWORD}
    )
    old_refresh_cookie = login.cookies.get("refresh_token")

    client.post("/api/v1/auth/refresh")  # rotates: old cookie is now revoked

    r = client.post("/api/v1/auth/refresh", cookies={"refresh_token": old_refresh_cookie})
    assert r.status_code == 401


def test_logout_revokes_refresh_and_clears_cookie(client, test_user):
    client.post("/api/v1/auth/login", json={"email": test_user.email, "password": TEST_PASSWORD})

    r = client.post("/api/v1/auth/logout")
    assert r.status_code == 204

    r2 = client.post("/api/v1/auth/refresh")
    assert r2.status_code == 401


def test_logout_without_cookie_is_idempotent(client):
    r = client.post("/api/v1/auth/logout")
    assert r.status_code == 204
