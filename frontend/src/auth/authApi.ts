// Plain fetch, no router/data-layer dependency: F-06/F-07 (React Query, API
// client) aren't built yet. This is intentionally minimal — just enough to
// wire the existing login page to the real backend.

export interface AuthRole {
  code: string;
  name: string;
}

export interface AuthUser {
  id: string;
  email: string;
  full_name: string;
  role: AuthRole;
}

export class LoginError extends Error {}

// Falls back to the standard local backend port so `npm run dev` works
// without requiring a frontend .env file; docker-compose sets VITE_API_URL
// explicitly and takes precedence.
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function fetchCurrentUser(accessToken: string): Promise<AuthUser> {
  const res = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
    headers: { Authorization: `Bearer ${accessToken}` },
    credentials: 'include',
  });
  if (!res.ok) {
    throw new LoginError('Could not load the signed-in user.');
  }
  return (await res.json()) as AuthUser;
}

export async function login(
  email: string,
  password: string,
): Promise<{ accessToken: string; user: AuthUser }> {
  const res = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    // Sends/receives the httpOnly refresh-token cookie; the access token
    // itself only ever lives in memory (component state), never storage.
    credentials: 'include',
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    throw new LoginError('Invalid email or password');
  }
  const { access_token: accessToken } = (await res.json()) as { access_token: string };
  const user = await fetchCurrentUser(accessToken);
  return { accessToken, user };
}

export async function logout(): Promise<void> {
  await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  });
}
