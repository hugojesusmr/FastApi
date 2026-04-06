import { Home, BarChart2, Mail, Bell, Settings, Power } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import './sidebar.css';

interface SidebarProps {
  isOpen: boolean;
  isMini: boolean;
}

export default function Sidebar({ isOpen, isMini }: SidebarProps) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
    navigate('/login');
  };

  const sidebarClass = `sidebar card-hybrid ${!isMini ? 'mini' : ''} ${isOpen ? 'active' : ''}`;

  return (
    <aside className={sidebarClass} id="sidebar">
      <nav>
        <a href="#" className="nav-item">
          <Home size={20} />
          <span>Dashboard</span>
        </a>
        <a href="#" className="nav-item">
          <BarChart2 size={20} />
          <span>Analíticas</span>
        </a>
        <a href="#" className="nav-item">
          <Mail size={20} />
          <span>Mensajes</span>
        </a>
        <a href="#" className="nav-item">
          <Bell size={20} />
          <span>Notificaciones</span>
        </a>
        <a href="#" className="nav-item">
          <Settings size={20} />
          <span>Ajustes</span>
        </a>
      </nav>
      <div className="sidebar-footer">
        <button className="nav-item logout-link" onClick={handleLogout}>
          <Power size={20} />
          <span>Cerrar Sesión</span>
        </button>
      </div>
    </aside>
  );
}
