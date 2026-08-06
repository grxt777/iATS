import React from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import './Layout.css';

const Layout: React.FC = () => {
  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="logo">
          <h1>🚛 AI Logistics</h1>
          <p>E-Logistika Platform</p>
        </div>
        
        <nav className="nav-menu">
          <NavLink to="/" end className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
            <span className="icon">📊</span>
            <span>Dashboard</span>
          </NavLink>
          
          <NavLink to="/orders" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
            <span className="icon">📦</span>
            <span>Orders</span>
          </NavLink>
          
          <NavLink to="/vehicles" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
            <span className="icon">🚛</span>
            <span>Vehicles</span>
          </NavLink>
          
          <NavLink to="/matching" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
            <span className="icon">🤖</span>
            <span>AI Matching</span>
          </NavLink>
          
          <NavLink to="/safety" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
            <span className="icon">🛡️</span>
            <span>Safety Check</span>
          </NavLink>
          
          <NavLink to="/routing" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
            <span className="icon">️</span>
            <span>Route Planner</span>
          </NavLink>
          
          <NavLink to="/documents" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
            <span className="icon">📄</span>
            <span>Documents</span>
          </NavLink>
          
          <NavLink to="/permits" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
            <span className="icon">📜</span>
            <span>Permits</span>
          </NavLink>
          
          <NavLink to="/analytics" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
            <span className="icon">📈</span>
            <span>Analytics</span>
          </NavLink>
        </nav>
        
        <div className="sidebar-footer">
          <p>Hackathon 2026</p>
          <p className="version">v1.0.0</p>
        </div>
      </aside>
      
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
