"""Shared test fixtures.

Test DB strategy: run against the same dev Postgres, wrapping each test in
an outer transaction + SAVEPOINT so code under test can call `session.commit()`
freely while everything is rolled back afterward (SQLAlchemy's standard
"join a session into an external transaction" recipe). This is a pragmatic
simplification (no separate test database yet) — see DEVELOPMENT_GUIDE.
"""

import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.orm import Session

from app.core.rate_limit import limiter
from app.core.security import hash_password
from app.db.session import engine, get_db
from app.main import app
from app.modules.auth import service as auth_service
from app.modules.auth.models import Role, User
from app.modules.tenants.models import Tenant

TEST_PASSWORD = "Test-Password-123!"


@pytest.fixture(autouse=True)
def _disable_rate_limiting_and_reset_state():
    # Deterministic tests: don't let slowapi's per-IP bucket (all TestClient
    # requests share one fake client address) or the per-account failed-
    # attempt tracker leak state between tests / trip on a shared address.
    limiter.enabled = False
    auth_service._failed_attempts.clear()
    yield
    auth_service._failed_attempts.clear()


@pytest.fixture
def db_session():
    connection = engine.connect()
    trans = connection.begin()
    session = Session(bind=connection)
    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def _restart_savepoint(sess, transaction):
        if transaction.nested and not transaction._parent.nested:
            sess.begin_nested()

    yield session

    session.close()
    trans.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_tenant(db_session):
    tenant = Tenant(name="Test Tenant", slug=f"test-{uuid.uuid4().hex[:8]}")
    db_session.add(tenant)
    db_session.flush()
    return tenant


@pytest.fixture
def admin_role(db_session):
    role = db_session.query(Role).filter_by(code="admin").first()
    assert role is not None, "roles must be seeded first: python -m app.db.seed"
    return role


@pytest.fixture
def readonly_role(db_session):
    role = db_session.query(Role).filter_by(code="readonly").first()
    assert role is not None, "roles must be seeded first: python -m app.db.seed"
    return role


@pytest.fixture
def test_user(db_session, test_tenant, admin_role):
    user = User(
        tenant_id=test_tenant.id,
        email=f"test+{uuid.uuid4().hex[:8]}@example.com",
        password_hash=hash_password(TEST_PASSWORD),
        full_name="Test User",
        role_id=admin_role.id,
        is_active=True,
    )
    db_session.add(user)
    db_session.flush()
    return user
