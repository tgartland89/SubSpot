import React from "react";
import TeacherNavBar from "./TeacherNavBar";
import TeacherDashboard from "./TeacherDashboard"; 

const TeacherDashboardPage = () => {
  return (
    <div>
      <TeacherNavBar /> 
      <div>
        <h1>Welcome to Teacher Dashboard</h1>
        <p>Here you can manage your teaching-related activities and view reviews.</p>
        <TeacherDashboard /> 
      </div>
    </div>
  );
};

export default TeacherDashboardPage;
