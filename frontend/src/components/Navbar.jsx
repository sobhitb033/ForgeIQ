function Navbar({ onLogout }) {
    return (
        <nav className="navbar">
            <div className="nav-container">
                <div className="logo">
                    <div className="logo-icon">⚡</div>

                    <div className="logo-text">
                        ForgeIQ
                    </div>
                </div>

                <div className="nav-right">
                    <span className="status-dot"></span>

                    <span>AI Project Analyzer</span>

                    <button
                        className="logout-button"
                        onClick={onLogout}
                    >
                        Logout
                    </button>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;