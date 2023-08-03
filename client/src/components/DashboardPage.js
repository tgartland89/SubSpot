import React from "react";
import NavBar from "./NavBar";
import Dashboard from "./Dashboard";
import TeacherDashboard from './TeacherDashboard';
import SubstituteDashboard from './SubstituteDashboard';
import AdminDashboard from './AdminDashboard';

const DashboardPage = ({ userRole }) => {
  return (
    <div>
      <NavBar />
      <Dashboard userRole={userRole} />
      {userRole === 'teacher' && <TeacherDashboard />}
      {userRole === 'substitute' && <SubstituteDashboard />}
      {userRole === 'admin' && <AdminDashboard />}
  </div>
);
};

export default DashboardPage;