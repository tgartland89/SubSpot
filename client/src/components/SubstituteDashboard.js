import React from "react";
import { useHistory } from "react-router-dom";

const SubstituteDashboard = () => {
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
        <h1>Welcome to Substitute Dashboard</h1>
        {/* Add the content for the Substitute Dashboard */}
        <p>Here you can manage your substitute-related activities.</p>
        <p>You can view incoming requests and respond to them.</p>
        <button onClick={handleLogout}>Log Out</button>
      </div>
    );
  };
  
export default SubstituteDashboard;