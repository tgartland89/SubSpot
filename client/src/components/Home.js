import React from "react";
import { Link } from "react-router-dom";
import teacherImage from "../assets/teacher_computer_class.jpg";
import substituteImage from "../assets/substitute_1.jpg";

function Home() {
  return (
    <div>
      <h1>Welcome to SubSpot!</h1>
      <p>Find substitutes quickly for your teaching needs.</p>
      <div className="login-container">
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
        <div className="image-container">
          <img src={teacherImage} alt="Teacher" className="teacher-image" />
          <img src={substituteImage} alt="Substitute" className="substitute-image" />
        </div>
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
      </div>
    </div>
  );
}

export default Home;