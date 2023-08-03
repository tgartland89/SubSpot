import React from "react";
import NavBar from "./NavBar";
import Dashboard from "./Dashboard";
import TeacherDashboard from './TeacherDashboard';

const DashboardPage = ({ userRole }) => {
  return (
    <div>
      <NavBar userRole={userRole} />
      <Dashboard userRole={userRole} />
      {userRole === 'teacher' && <TeacherDashboard />}
    </div>
  );
};

export default DashboardPage;