import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../AuthContext";

function NavBar() {
  const { user, logout } = useContext(AuthContext);

  const handleLogout = () => {
    logout(); // Clear the user session and redirect to the home page
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
        {user && (
          <li>
            {user.role === "Teacher" && (
              <Link to="/teacher-dashboard">Teacher Dashboard</Link>
            )}
            {user.role === "Substitute" && (
              <Link to="/substitute-dashboard">Substitute Dashboard</Link>
            )}
            {user.role === "Admin" && (
              <Link to="/admin-dashboard">Admin Dashboard</Link>
            )}
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
}

export default NavBar;
