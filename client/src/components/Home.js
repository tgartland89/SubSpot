import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div>
      <h1>Welcome to SubSpot!</h1>
      <p>Find substitutes quickly for your teaching needs.</p>
      <div>
        <h2>Log In</h2>
        <form>
          <label>Email:</label>
          <input type="email" name="email" required /><br />

          <label>Password:</label>
          <input type="password" name="password" required /><br />

          <input type="submit" value="Log In" />
        </form>
      </div>
      <div>
        <h2>Sign Up</h2>
        <Link to="/signup">Sign Up</Link>
      </div>
    </div>
  );
}

export default Home;
