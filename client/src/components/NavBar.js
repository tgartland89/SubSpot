import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = ({ userRole }) => {
  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        {userRole === 'admin' && <li><Link to="/admin-dashboard">Admin Dashboard</Link></li>}
        {userRole === 'teacher' && <li><Link to="/teacher-dashboard">Teacher Dashboard</Link></li>}
        {userRole === 'substitute' && <li><Link to="/substitute-dashboard">Substitute Dashboard</Link></li>}
        <li><Link to="/about">About</Link></li>
        <li><Link to="/logout">Log Out</Link></li>
      </ul>
    </nav>
  );
};

export default NavBar;
