import { useEffect, useRef, useState } from "react";
import "./App.css";
import Auth from "./pages/Auth";
import Home from "./pages/Home";
import { getTokenExpiration, isAuthenticated, logoutUser } from "./services/api";

function App() {
  const [authenticated,setAuthenticated]=useState(isAuthenticated());
  const timer=useRef(null);
  useEffect(()=>{
    const schedule=()=>{ if(timer.current) clearTimeout(timer.current); if(!isAuthenticated()){setAuthenticated(false);return;} const exp=getTokenExpiration(); if(!exp){setAuthenticated(false);return;} timer.current=setTimeout(()=>{logoutUser();setAuthenticated(false)},Math.max(0,exp-Date.now())); };
    schedule();
    const onLogout=()=>{if(timer.current)clearTimeout(timer.current);setAuthenticated(false)};
    const onStorage=()=>{const ok=isAuthenticated();setAuthenticated(ok);if(ok)schedule()};
    window.addEventListener("forgeiq:logout",onLogout); window.addEventListener("storage",onStorage);
    return()=>{if(timer.current)clearTimeout(timer.current);window.removeEventListener("forgeiq:logout",onLogout);window.removeEventListener("storage",onStorage)};
  },[]);
  if(!authenticated) return <Auth onLogin={()=>setAuthenticated(true)} />;
  return <div className="app"><Home onLogout={()=>{logoutUser();setAuthenticated(false)}} /></div>;
}
export default App;
