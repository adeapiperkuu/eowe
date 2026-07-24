import styles from './LoginPage.module.css';

function BrandPanel() {
  return (
    <aside className={styles.brandPanel}>
      <div className={styles.brandOverlay} aria-hidden="true" />

      <div className={styles.brandContent}>
        <div className={styles.brandLogo}>EOWE</div>
        <h2 className={styles.brandTagline}>Manage your open-water events, all in one place.</h2>
        <p className={styles.brandSubtext}>
          Registrations, participants, and event storefront — from one dashboard.
        </p>
      </div>

      <p className={styles.brandFooter}>European Open Water Events</p>
    </aside>
  );
}

export default BrandPanel;
