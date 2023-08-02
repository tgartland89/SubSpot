import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import { loginUser } from "./api"; 

function LoginComponent() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
   // eslint-disable-next-line 
  const [userRole, setUserRole] = useState(""); 
  const history = useHistory();

  const handleLogin = (event) => {
    event.preventDefault();
    loginUser(email, password)
      .then((data) => {
        setUserRole(data.role);
        if (data.role === "teacher") {
          history.push("/teacher-dashboard");
        } else if (data.role === "admin") {
          history.push("/admin-dashboard");
        } else if (data.role === "substitute") {
          history.push("/substitute-dashboard");
        }
      })
      .catch((error) => {
        console.error("Error occurred during login:", error);
      });
  };

  return (
    <div>
      <h2>Log in</h2>
      <form onSubmit={handleLogin}>
        <label>Email:</label>
        <input type="email" name="email" required onChange={(e) => setEmail(e.target.value)} /><br />
        <label>Password:</label>
        <input type="password" name="password" required onChange={(e) => setPassword(e.target.value)} /><br />
        <input type="submit" value="Log In" />
      </form>
    </div>
  );
}

export default LoginComponent;