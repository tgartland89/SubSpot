import React from "react";
import NavBar from "./NavBar";
import Dashboard from "./Dashboard";

const DashboardPage = ({ userRole }) => {
  return (
    <div>
      <NavBar userRole={userRole} />
      <Dashboard userRole={userRole} />
    </div>
  );
};

export default DashboardPage;
