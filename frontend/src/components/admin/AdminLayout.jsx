function AdminLayout({ children }) {
  const now = new Date();
  const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
  const dateStr = now.toLocaleDateString([], { day: '2-digit', month: '2-digit', year: '2-digit' });

  return (
    <div>
      <nav className="admin-navbar">
        <a className="admin-navbar-brand" href="/">
          <span className="brand-icon"><img src="https://png.pngtree.com/png-vector/20230814/ourmid/pngtree-cartoon-italian-chef-logo-for-pizza-restaurant-on-green-background-clipart-vector-png-image_6902779.png" alt="Logo" width="60" height="60" /></span>
          <span className="brand-text">Restaurant / Admin</span>
        </a>

        <div className="admin-navbar-meta">
          <span className="admin-navbar-dot" title="Server online" />
          <span>LIVE</span>
          <span className="nav-divider" />
          <span>{dateStr}</span>
          <span className="nav-divider" />
          <span>{timeStr}</span>
        </div>
      </nav>

      <main className="admin-main">{children}</main>
    </div>
  );
}

export default AdminLayout;
