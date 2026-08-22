import "./Navbar.css";

function Navbar() {
    return (
        <nav className="navbar">
            <div className="nav-container">
                <div className="logo">
                    <span className="logo-mark">◈</span>
                    <span className="logo-text">ForgeIQ</span>
                </div>

                <div className="nav-links">
                    <a href="#home">Home</a>
                    <a href="#analyze">Analyze</a>
                    <a href="#about">About</a>
                </div>

                <button className="nav-button">Analyze Project</button>
            </div>
        </nav>
    );
}

export default Navbar;