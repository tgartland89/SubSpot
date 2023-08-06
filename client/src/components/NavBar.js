import React, { useContext } from "react";
import { Link, useHistory } from "react-router-dom";
import { AuthContext } from "../AuthContext";

function NavBar() {
  const { user, logout } = useContext(AuthContext);
  const history = useHistory();

  const handleLogout = () => {
    logout();
    history.push("/");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light golden-rod-bg"> 
      <ul className="navbar-nav mr-auto">
        <li className="nav-item">
          <Link to="/" className="nav-link">
            Home
          </Link>
        </li>
        <li className="nav-item">
          <Link to="/about" className="nav-link">
            About
          </Link>
        </li>
        {user && (
          <li className="nav-item">
            {user.role === "Teacher" && (
              <Link to="/teacher-dashboard" className="nav-link">
                Teacher Dashboard
              </Link>
            )}
            {user.role === "Substitute" && (
              <Link to="/substitute-dashboard" className="nav-link">
                Substitute Dashboard
              </Link>
            )}
            {user.role === "SiteAdmin" && (
              <Link to="/admin-dashboard" className="nav-link">
                Admin Dashboard
              </Link>
            )}
          </li>
        )}
      </ul>
      {user && (
        <button
          className="btn btn-outline-primary my-2 my-sm-0"
          onClick={handleLogout}
        >
          Log Out
        </button>
      )}
    </nav>
  );
}

export default NavBar;