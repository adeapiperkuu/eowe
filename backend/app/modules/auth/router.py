from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.rate_limit import limiter
from app.core.security import InvalidTokenError
from app.db.session import get_db
from app.modules.auth import service
from app.modules.auth.models import User
from app.modules.auth.schemas import LoginRequest, TokenResponse, UserRead

router = APIRouter()

REFRESH_COOKIE_NAME = "refresh_token"
REFRESH_COOKIE_PATH = "/api/v1/auth"


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def _set_refresh_cookie(response: Response, refresh_token: str, max_age_seconds: int) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        # Secure requires TLS; local dev/test run over plain http://localhost,
        # where browsers/test clients (unlike some special-cased fetch APIs)
        # will not resend a Secure cookie. Production terminates TLS at the
        # proxy (SECURITY_STANDARDS §6) so this is safe there.
        secure=settings.environment == "production",
        samesite="lax",
        max_age=max_age_seconds,
        path=REFRESH_COOKIE_PATH,
    )


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login(
    request: Request,
    body: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> TokenResponse:
    # PUBLIC: unauthenticated login endpoint (SECURITY_STANDARDS §0.2).
    try:
        access_token, refresh_token, _user = service.login(
            db, body.email, body.password, _client_ip(request)
        )
    except service.InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        ) from exc

    _set_refresh_cookie(response, refresh_token, settings.refresh_token_expire_days * 24 * 60 * 60)
    return TokenResponse(access_token=access_token)


@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("10/minute")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)) -> TokenResponse:
    # PUBLIC: the access token is presumed expired; auth is the refresh cookie.
    raw_refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if not raw_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
        )
    try:
        access_token, new_refresh_token = service.refresh(
            db, raw_refresh_token, _client_ip(request)
        )
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials"
        ) from exc

    _set_refresh_cookie(
        response, new_refresh_token, settings.refresh_token_expire_days * 24 * 60 * 60
    )
    return TokenResponse(access_token=access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(request: Request, response: Response, db: Session = Depends(get_db)) -> None:
    # PUBLIC: intentionally works without a valid access token so logout
    # succeeds even after the access token has already expired; the
    # credential actually checked is the httpOnly refresh cookie (revoked
    # server-side by service.logout if present and still valid).
    raw_refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    service.logout(db, raw_refresh_token, _client_ip(request))
    response.delete_cookie(key=REFRESH_COOKIE_NAME, path=REFRESH_COOKIE_PATH)


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user
