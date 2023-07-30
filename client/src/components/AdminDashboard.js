import React from "react";
import { useHistory } from "react-router-dom";
import AdminNavBar from './AdminNavBar';

const AdminDashboard = () => {
    const history = useHistory();
    const handleLogout = () => {
      fetch("/auth/logout", {
        method: "GET",
      })
        .then((response) => {
          if (response.ok) {
            history.push("/login");
          } else {
            console.log("Error occurred during logout.");
          }
        })
        .catch((error) => {
          console.error("Error occurred during logout:", error);
        });
    };
    
    return (
      <div>
        <AdminNavBar /> {/* Use the AdminNavBar component here */}
        <h1>Welcome to Admin Dashboard</h1>
        {/* Add the content for the Admin Dashboard */}
        <p>Here you can manage teachers and substitutes.</p>
        <p>You have the authority to add, delete, and update users for both tabs.</p>

        <button onClick={handleLogout}>Log Out</button>
      </div>
    );
};

export default AdminDashboard;