import { useState } from "react";

import "./App.css";

import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Auth from "./pages/Auth";

import {
  isAuthenticated,
  logoutUser,
} from "./services/api";


function App() {

  const [authenticated, setAuthenticated] = useState(
    isAuthenticated()
  );

  const handleLogin = () => {
    setAuthenticated(true);
  };

  const handleLogout = () => {
    logoutUser();
    setAuthenticated(false);
  };

  if (!authenticated) {
    return (
      <Auth
        onLogin={handleLogin}
      />
    );
  }

  return (
    <div className="app">
      <Navbar
        onLogout={handleLogout}
      />

      <Home />
    </div>
  );
}

export default App;