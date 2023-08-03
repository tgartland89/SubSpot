import React, { useContext } from "react";
import { Link, useHistory } from "react-router-dom";
import { AuthContext } from "../AuthContext";

function NavBar() {
  const { user, logout } = useContext(AuthContext);
  const history = useHistory();

  const handleLogout = () => {
    logout(); // Clear the user session
    history.push("/"); // Redirect to the home page
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
            {user.role === "SiteAdmin" && (
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
