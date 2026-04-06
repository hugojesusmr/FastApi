import { Menu, User } from 'lucide-react';
import './topbar.css';

interface TopbarProps {
  onMenuClick: () => void;
}

export default function Topbar({ onMenuClick }: TopbarProps) {
  return (
    <header className="topbar card-hybrid">
      <div className="content-topbar">
        <button className="btn-menu" onClick={onMenuClick}>
          <Menu size={24} />
        </button>
        <div className="topbar-titulo">IT Support</div>
      </div>

      <div className="topbar-usuario">
        <span>Usuario</span>
        <div className="circle-user">
          <User size={24} />
        </div>
      </div>
    </header>
  );
}
