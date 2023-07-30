import React, { useState } from "react";
import { useHistory } from "react-router-dom";

function LoginComponent() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const history = useHistory();

  const handleLogin = (event) => {
    event.preventDefault();

    // Perform login logic and API call here using the email and password state variables.
    // You may use fetch or Axios to make an API call to your Flask backend.
    // Upon successful login, redirect to the home page.
    // Example using fetch:

    fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    })
      .then((response) => {
        if (response.ok) {
          history.push("/"); // Redirect to the home page upon successful login.
        } else {
          // Handle invalid login here.
          console.log("Invalid email or password. Please try again.");
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
