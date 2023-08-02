import React from "react";
import { Link } from "react-router-dom";

const NavBar = ({ userRole, onLogout }) => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/about">About</Link>
        </li>
        {userRole === "Teacher" && (
          <li>
            <Link to="/teacher-dashboard">Teacher Dashboard</Link>
          </li>
        )}
        {userRole === "Substitute" && (
          <li>
            <Link to="/substitute-dashboard">Substitute Dashboard</Link>
          </li>
        )}
        {userRole === "SiteAdmin" && (
          <li>
            <Link to="/admin-dashboard">Admin Dashboard</Link>
          </li>
        )}
        {userRole && (
          <li>
            <button onClick={onLogout}>Log Out</button>
          </li>
        )}
      </ul>
    </nav>
  );
};

export default NavBar;