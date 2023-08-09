import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div>
      <h1>Welcome to SubSpot!</h1>
      <p>Find substitutes quickly for your teaching needs.</p>
      <div className="login-container">
        <div className="login-box left-box">
          <h2>Log In</h2>
          <form>
            <label>Email:</label>
            <input type="email" name="email" required /><br />

            <label>Password:</label>
            <input type="password" name="password" required /><br />

            <input type="submit" value="Log In" />
          </form>
        </div>
        <div className="signup-about-box right-box"> 
          <div>
            <h2>Sign Up</h2>
            <Link to="/signup" className="dark-purple-link">Sign Up</Link>
          </div>
          <div>
            <h2>About</h2>
            <Link to="/about" className="dark-purple-link">About</Link>
          </div>
        </div>
      </div>
    </div>
  );
}
export default Home;