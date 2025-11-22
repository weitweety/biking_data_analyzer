import { Link, useLocation } from 'react-router-dom';
import './NavigationBar.css';

const NavigationBar = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="navigation-bar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          <h1>Biking Data Analyzer</h1>
        </Link>
        <div className="nav-links">
          <Link 
            to="/trip-duration" 
            className={`nav-link ${isActive('/trip-duration') ? 'active' : ''}`}
          >
            Trip Duration
          </Link>
          <Link 
            to="/hour-range" 
            className={`nav-link ${isActive('/hour-range') ? 'active' : ''}`}
          >
            Hour Range
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default NavigationBar;

