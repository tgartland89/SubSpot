import React, { useState, useEffect } from "react";
import { Switch, Route } from "react-router-dom";
import Home from "./Home";
import LoginComponent from "./Login";
import SignUp from "./SignUp";
import DashboardPage from "./DashboardPage";
import NavBar from "./NavBar";
import NotFound from "./NotFound";
import SubsDetails from "./SubDetails";
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
  // eslint-disable-next-line
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const urlSearchParams = new URLSearchParams(window.location.search);
    const email = urlSearchParams.get("email");
    const password = urlSearchParams.get("password");

    if (email && password) {
      loginUser(email, password)
        .then((data) => {
          setUserRole(data.role);
          console.log("User role after login:", data.role); 
    
          window.history.replaceState({}, document.title, window.location.pathname);
        })
        .catch((error) => {
          console.error("Error occurred during login:", error);
        });
    } else {
      setIsLoading(false);
    }
  }, []);
  
  const handleLogout = () => {
    fetch("/logout", { method: "DELETE" })
      .then(() => {
        setUserRole(null);
        window.location.href = '/'; 
      })
      .catch((error) => {
        console.error("Error occurred during logout:", error);
      });
  };
  
  return (
    <div>
      <NavBar userRole={userRole} onLogout={handleLogout} />
      <Switch>
        <Route exact path="/" component={Home} />   
        <Route path="/login" component={LoginComponent} />
        <Route path="/signup" component={SignUp} />
        <Route path="/about" component={About} />
        <Route component={NotFound} /> 
        <Route path="/teacher-dashboard" render={() => <DashboardPage userRole="teacher" />} />
        <Route path="/sub-details/:substituteId" component={SubsDetails}/>
        <Route path="/admin-dashboard" render={() => <DashboardPage userRole="admin" />} />
        <Route path="/substitute-dashboard" render={() => <DashboardPage userRole="substitute" />} />
      </Switch>
    </div>
  );
}

export default App;