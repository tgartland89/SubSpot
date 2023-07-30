import React from "react";
import { useHistory } from "react-router-dom";

const TeacherDashboard = () => {
  const history = useHistory();

  const handleLogout = () => {
    fetch("/logout", {
      method: "GET",
    })
      .then((response) => {
        if (response.ok) {
          history.push("/login"); // Use useHistory to navigate to "/login" after logout
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
      <h1>Welcome to Teacher Dashboard</h1>
      {/* Add the content for the Teacher Dashboard */}
      <p>Here you can manage your teaching-related activities and view reviews.</p>

      <button onClick={handleLogout}>Log Out</button>
    </div>
  );
};

export default TeacherDashboard;
