import React from "react";
import NavBar from "./NavBar";
import TeacherDashboard from "./TeacherDashboard";
import SubstituteDashboard from "./SubstituteDashboard";
import AdminDashboard from "./AdminDashboard";

const DashboardPage = ({ userRole }) => {
  console.log("userRole in DashboardPage:", userRole);
  return (
    <div>
      <NavBar userRole={userRole} />
      {userRole === "teacher" && <TeacherDashboard />}
      {userRole === "substitute" && <SubstituteDashboard />}
      {userRole === "admin" && <AdminDashboard />}
    </div>
  );
};

export default DashboardPage;