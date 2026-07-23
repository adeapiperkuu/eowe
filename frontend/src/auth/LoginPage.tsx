import { useLoginForm } from './useLoginForm';
import type { LoginData } from './validation';
import styles from './LoginPage.module.css';

// Placeholder submit handler — no real auth, no API calls.
// A teammate will wire the backend separately.
function onSubmit(data: LoginData) {
  console.log('Login submitted:', data);
}

function LoginPage() {
  const { email, password, errors, setEmail, setPassword, handleSubmit } = useLoginForm(onSubmit);

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <div className={styles.header}>
          <div className={styles.logoMark} aria-hidden="true" />
          <h1 className={styles.title}>Sign in to your account</h1>
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

          <button type="submit" className={styles.button}>
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
