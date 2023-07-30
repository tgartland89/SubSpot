import React, { useState, useEffect } from "react";
import { Switch, Route } from "react-router-dom";
import Home from "./Home";
import LoginComponent from "./Login";
import SignUp from "./SignUp";
import AdminDashboard from "./AdminDashboard";
import AdminNavBar from './AdminNavBar'
import SubstituteDashboard from "./SubstituteDashboard";
import SubNavBar from './SubNavBar';
import TeacherNavBar from './TeacherNavBar';
import TeacherDashboardPage from "./TeacherDashboardPage";
import NotFound from "./NotFound";
import { loginUser } from "./api";

function About() {
  return (
    <div>
      <h1>About SubSpot</h1>
      <p>
        SubSpot is a site built by the son of a fourth-grade teacher who was looking for alternatives to find substitute teachers quickly and efficiently.
      </p>
    </div>
  );
}

function App() {
  const [userRole, setUserRole] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  
  useEffect(() => {
    const urlSearchParams = new URLSearchParams(window.location.search);
    const email = urlSearchParams.get("email");
    const password = urlSearchParams.get("password");

    if (email && password) {
      loginUser(email, password)
        .then((data) => {
          setUserRole(data.role);
        })
        .catch((error) => {
          console.error("Error occurred during login:", error);
        });
    } else {
      setIsLoading(false);
    }
  }, []);
  

  if (isLoading) {
    return <div>Loading...</div>; 
  }

  return (
    <div>
      {userRole === "admin" && <AdminNavBar />}
      {userRole === "teacher" && <TeacherNavBar />} 
      {userRole === "substitute" && <SubNavBar />} 
      {userRole === "teacher" && <TeacherDashboardPage />}

      <Switch>
        <Route exact path="/" component={Home} />   
        <Route path="/login" component={LoginComponent} />
        <Route path="/signup" component={SignUp} />
        <Route path="/about" component={About} />
        <Route component={NotFound} /> 
        <Route path="/substitute-dashboard" component={SubstituteDashboard} />
        <Route path="/admin-dashboard" component={AdminDashboard} />
        <Route path="/teacher-dashboard" component={TeacherDashboardPage} /> 
      </Switch>
    </div>
  );
}

export default App;