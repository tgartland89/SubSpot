import React, { useState, useEffect } from "react";
import { Switch, Route, } from "react-router-dom";
import Home from "./Home";
import LoginComponent from "./Login";
import SignUp from "./SignUp";
import DashboardPage from "./DashboardPage";
import NavBar from "./NavBar";
import NotFound from "./NotFound";
import SubsDetails from "./SubDetails";
import { loginUser } from "./api";
import { useAuth } from "../AuthContext";
import TeacherDashboard from "./TeacherDashboard";
import SubstituteDashboard from "./SubstituteDashboard";
import AdminDashboard from "./AdminDashboard";

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
  const { user, login } = useAuth();
  // eslint-disable-next-line
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const urlSearchParams = new URLSearchParams(window.location.search);
    const email = urlSearchParams.get("email");
    const password = urlSearchParams.get("password");

    if (email && password) {
      loginUser(email, password)
        .then((data) => {
          login(data);
          console.log("User role after login:", data.role);

          window.history.replaceState({}, document.title, window.location.pathname);
        })
        .catch((error) => {
          console.error("Error occurred during login:", error);
        });
    } else {
      setIsLoading(false);
    }
  }, [login]);

  console.log("User Role:", user?.role);

  return (
    <div>
      <NavBar />
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/login" component={LoginComponent} />
        <Route path="/signup" component={SignUp} />
        <Route path="/about" component={About} />
        <Route path="/dashboard" render={() => <DashboardPage userRole={user?.role} />} />

        {/* Teacher Dashboard */}
        <Route path="/teacher-dashboard" component={TeacherDashboard} />

        {/* Substitute Dashboard */}
        <Route path="/substitute-dashboard" component={SubstituteDashboard} />

        {/* Admin Dashboard */}
        <Route path="/admin-dashboard" component={AdminDashboard} />

        <Route path="/sub-details/:substituteId" component={SubsDetails} />
        <Route component={NotFound} />
      </Switch>
    </div>
  );
}

export default App;
