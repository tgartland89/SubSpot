import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../AuthContext';

const NavBar = ({ onLogout }) => {
  const { user, logout } = useContext(AuthContext); 
  console.log("User: ", user);
  
  const handleLogout = () => {
    fetch("/logout", { method: "DELETE" })
      .then(() => {
        logout();
        window.location.href = '/'; 
      })
      .catch((error) => {
        console.error("Error occurred during logout:", error);
      });
  };

  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/about">About</Link>
        </li>
        {user && user.role === "teacher" && (
          <li>
            <Link to="/teacher-dashboard">Teacher Dashboard</Link>
          </li>
        )}
        {user && user.role === "substitute" && (
          <li>
            <Link to="/substitute-dashboard">Substitute Dashboard</Link>
          </li>
        )}
        {user && user.role === "admin" && (
          <li>
            <Link to="/admin-dashboard">Admin Dashboard</Link>
          </li>
        )}
        {user && (
          <li>
            <button onClick={handleLogout}>Log Out</button>
          </li>
        )}
      </ul>
    </nav>
  );
};

export default NavBar;