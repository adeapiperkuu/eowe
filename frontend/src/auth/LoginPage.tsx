import { useState } from 'react';

import { login, logout, LoginError, type AuthUser } from './authApi';
import BrandPanel from './BrandPanel';
import { useLoginForm } from './useLoginForm';
import type { LoginData } from './validation';
import styles from './LoginPage.module.css';

function LoginPage() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  // Access token lives only in component state (in memory) — never
  // localStorage/sessionStorage (SECURITY_STANDARDS §2.2).
  const [authUser, setAuthUser] = useState<AuthUser | null>(null);

  function onSubmit(data: LoginData) {
    setIsSubmitting(true);
    setSubmitError(null);
    login(data.email, data.password)
      .then(({ user }) => {
        setAuthUser(user);
      })
      .catch((err: unknown) => {
        setSubmitError(
          err instanceof LoginError ? err.message : 'Something went wrong. Please try again.',
        );
      })
      .finally(() => {
        setIsSubmitting(false);
      });
  }

  function handleLogout() {
    setAuthUser(null);
    void logout();
  }

  const { email, password, errors, setEmail, setPassword, handleSubmit } = useLoginForm(onSubmit);

  if (authUser) {
    return (
      <div className={styles.page}>
        <BrandPanel />
        <div className={styles.formPanel}>
          <div className={styles.card}>
            <div className={styles.header}>
              <div className={styles.logoMark} aria-hidden="true" />
              <h1 className={styles.title}>Logged in as {authUser.full_name}</h1>
              <p className={styles.subtitle}>
                {authUser.role.name} &middot; {authUser.email}
              </p>
            </div>
            <button type="button" className={styles.button} onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <BrandPanel />

      <div className={styles.formPanel}>
        <div className={styles.card}>
          <div className={styles.header}>
            <div className={styles.logoMark} aria-hidden="true" />
            <h1 className={styles.title}>Sign in to your events dashboard</h1>
            <p className={styles.subtitle}>Welcome back. Please enter your details.</p>
          </div>

          <form onSubmit={handleSubmit} noValidate className={styles.form}>
            <div className={styles.field}>
              <label htmlFor="email" className={styles.label}>
                Email
              </label>
              <input
                id="email"
                type="email"
                autoComplete="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={`${styles.input} ${errors.email ? styles.invalid : ''}`}
                aria-invalid={Boolean(errors.email)}
                aria-describedby={errors.email ? 'email-error' : undefined}
              />
              {errors.email && (
                <span id="email-error" className={styles.error}>
                  {errors.email}
                </span>
              )}
            </div>

            <div className={styles.field}>
              <label htmlFor="password" className={styles.label}>
                Password
              </label>
              <input
                id="password"
                type="password"
                autoComplete="current-password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className={`${styles.input} ${errors.password ? styles.invalid : ''}`}
                aria-invalid={Boolean(errors.password)}
                aria-describedby={errors.password ? 'password-error' : undefined}
              />
              {errors.password && (
                <span id="password-error" className={styles.error}>
                  {errors.password}
                </span>
              )}
              <a href="#" className={styles.forgot}>
                Forgot your password?
              </a>
            </div>

            {submitError && (
              <span role="alert" className={styles.error}>
                {submitError}
              </span>
            )}

            <button type="submit" className={styles.button} disabled={isSubmitting}>
              {isSubmitting ? 'Signing in…' : 'Sign In'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
