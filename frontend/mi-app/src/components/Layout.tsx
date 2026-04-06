import { type ReactNode, useState, useEffect } from 'react';
import Topbar from './Topbar';
import Sidebar from './Sidebar';
import './layout.css';

interface LayoutProps {
  children: ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [sidebarMini, setSidebarMini] = useState(true);

  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 768) {
        setSidebarOpen(false);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const toggleSidebar = () => {
    const isMobile = window.innerWidth <= 768;
    if (isMobile) {
      setSidebarOpen(!sidebarOpen);
    } else {
      setSidebarMini(!sidebarMini);
    }
  };

  return (
    <div className="layout-container">
      <Topbar onMenuClick={toggleSidebar} />
      <div className="main-wrapper">
        <Sidebar isOpen={sidebarOpen} isMini={sidebarMini} />
        <main className="content-area">{children}</main>
      </div>
    </div>
  );
}
