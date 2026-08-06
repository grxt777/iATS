import React from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Button,
  Badge,
  Avatar,
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  Tooltip,
  Chip
} from '@heroui/react';

const navItems = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/orders', label: 'Orders', icon: '' },
  { path: '/vehicles', label: 'Vehicles', icon: '🚛' },
  { path: '/matching', label: 'AI Matching', icon: '🤖' },
  { path: '/safety', label: 'Safety', icon: '🛡️' },
  { path: '/routing', label: 'Routes', icon: '🗺️' },
  { path: '/documents', label: 'Documents', icon: '📄' },
  { path: '/permits', label: 'Permits', icon: '📜' },
  { path: '/analytics', label: 'Analytics', icon: '' },
];

const Layout: React.FC = () => {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <div className="min-h-screen bg-background">
      {/* HeroUI Navbar */}
      <Navbar
        maxWidth="full"
        className="glass border-b border-white/10"
        classNames={{
          wrapper: 'px-6'
        }}
      >
        <NavbarBrand>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center text-xl neon-glow">
              🚛
            </div>
            <div>
              <h1 className="text-lg font-bold text-foreground">AI Logistics</h1>
              <p className="text-xs text-muted">E-Logistika Platform</p>
            </div>
          </div>
        </NavbarBrand>

        <NavbarContent className="hidden md:flex gap-1" justify="center">
          {navItems.slice(0, 5).map((item) => (
            <NavbarItem key={item.path}>
              <NavLink
                to={item.path}
                end={item.path === '/'}
                className={({ isActive }) =>
                  `px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-primary/20 text-primary'
                      : 'text-muted hover:text-foreground hover:bg-white/5'
                  }`
                }
              >
                <span className="mr-2">{item.icon}</span>
                {item.label}
              </NavLink>
            </NavbarItem>
          ))}
        </NavbarContent>

        <NavbarContent justify="end">
          <NavbarItem>
            <Tooltip content="Notifications">
              <Button isIconOnly variant="light" className="text-muted hover:text-foreground">
                <Badge content="3" color="danger" size="sm">
                  🔔
                </Badge>
              </Button>
            </Tooltip>
          </NavbarItem>

          <NavbarItem>
            <Chip
              startContent={<span className="text-success">●</span>}
              variant="flat"
              color="success"
              size="sm"
            >
              Online
            </Chip>
          </NavbarItem>

          <NavbarItem>
            <Dropdown>
              <DropdownTrigger>
                <Button
                  variant="flat"
                  className="bg-surface hover:bg-white/10"
                >
                  <Avatar
                    isBordered
                    color="primary"
                    name="Admin"
                    size="sm"
                  />
                  <span className="ml-2 text-sm">Admin</span>
                </Button>
              </DropdownTrigger>
              <DropdownMenu aria-label="User actions">
                <DropdownItem key="profile">Profile</DropdownItem>
                <DropdownItem key="settings">Settings</DropdownItem>
                <DropdownItem key="logout" color="danger">Logout</DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </NavbarItem>
        </NavbarContent>
      </Navbar>

      {/* Main Content */}
      <div className="flex">
        {/* Sidebar */}
        <aside className="hidden lg:block w-64 min-h-screen glass border-r border-white/10 p-4 sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto">
          <nav className="space-y-1">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === '/'}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                    isActive
                      ? 'gradient-primary text-white shadow-lg'
                      : 'text-muted hover:text-foreground hover:bg-white/5'
                  }`
                }
              >
                <span className="text-xl">{item.icon}</span>
                <span className="text-sm font-medium">{item.label}</span>
              </NavLink>
            ))}
          </nav>

          <div className="mt-8 p-4 rounded-xl bg-gradient-to-br from-primary/10 to-secondary/10 border border-primary/20">
            <h3 className="text-sm font-bold text-foreground mb-2">System Status</h3>
            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-muted">API</span>
                <span className="text-success">● Online</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-muted">ML Models</span>
                <span className="text-success">● Active</span>
              </div>
              <div className="flex justify-between text-xs">
                <span className="text-muted">Database</span>
                <span className="text-success">● Connected</span>
              </div>
            </div>
          </div>

          <div className="mt-4 text-center">
            <p className="text-xs text-muted">Hackathon 2026</p>
            <p className="text-xs text-muted">v1.0.0</p>
          </div>
        </aside>

        {/* Page Content */}
        <main className="flex-1 p-6 animate-fade-in">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
