import React, { useState, useContext } from 'react';
import { useHistory } from 'react-router-dom';
import { loginUser } from './api';
import { AuthContext } from '../AuthContext';

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const { login } = useContext(AuthContext);
  const history = useHistory();

  const handleLogin = (event) => {
    event.preventDefault();

    loginUser(email, password)
    .then((data) => {
      login(data);
      if (data.role === "Teacher") {
        history.push(`/teacher-dashboard/${data.user_id}`); 
      } else if (data.role === "Substitute") {
        history.push(`/substitute-dashboard/${data.user_id}`); 
      } else if (data.role === "Admin") {
        history.push("/admin-dashboard");
      }
    })
    .catch((error) => {
      console.error("Error occurred during login:", error);
      setErrorMessage("Invalid email or password. Please try again.");
    });
  };

  return (
    <div>
      <h1>Welcome to SubSpot!</h1>
      <p>Find substitutes quickly for your teaching needs.</p>
      <form onSubmit={handleLogin}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Log In</button>
        {errorMessage && <p>{errorMessage}</p>}
      </form>
    </div>
  );
}

export default Login;