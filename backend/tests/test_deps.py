import pytest
from fastapi import HTTPException

from app.api.deps import require_roles


class _FakeRole:
    def __init__(self, code: str) -> None:
        self.code = code


class _FakeUser:
    def __init__(self, code: str) -> None:
        self.role = _FakeRole(code)


def test_require_roles_allows_matching_role():
    checker = require_roles("admin", "management")
    user = checker(_FakeUser("admin"))
    assert user.role.code == "admin"


def test_require_roles_rejects_wrong_role():
    checker = require_roles("admin", "management")
    with pytest.raises(HTTPException) as exc_info:
        checker(_FakeUser("readonly"))
    assert exc_info.value.status_code == 403
