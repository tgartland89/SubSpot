import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import teacherImage from "../assets/teacher_computer_class.jpg";
import substituteImage from "../assets/substitute_1.jpg";
import appleImage from "../assets/green_apple.jpg";

function Home() {
  useEffect(() => {
    const options = {
      root: null,
      rootMargin: "0px",
      threshold: 0.5,
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("fade-in");
          observer.unobserve(entry.target);
        }
      });
    }, options);

    const teacherImageElement = document.querySelector(".teacher-image");
    const substituteImageElement = document.querySelector(".substitute-image");

    if (teacherImageElement && !localStorage.getItem("teacherImageAnimated")) {
      observer.observe(teacherImageElement);
    }
    if (substituteImageElement && !localStorage.getItem("substituteImageAnimated")) {
      observer.observe(substituteImageElement);
    }

    return () => {
      observer.disconnect();
    };
  }, []);

  return (
    <div>
      <h1>Welcome to SubSpot!</h1>
      <p>Find substitutes quickly for your teaching needs.</p>
      <div className="login-container">
        <div className="login-box left-box">
          <h2 className="underlined-heading">Log In</h2>
          <form>
          <label className="bold-label">Email:</label>
            <input type="email" name="email" required /><br />

            <label className="bold-label">Password:</label>
            <input type="password" name="password" required /><br />

            <input type="submit" value="Log In" />
          </form>
        </div>
        <div className="signup-about-box right-box">
          <div>
            <h2 className="underlined-heading">Sign Up</h2>
            <p>
            <img src={appleImage} alt="Apple Bullet" className="apple-bullet" />Join us and create an account!</p>
            <Link to="/signup" className="dark-purple-link">
              Sign Up
            </Link>
          </div>
          <div>
            <h2 className="underlined-heading">About</h2>
            <p>
            <img src={appleImage} alt="Apple Bullet" className="apple-bullet" />Learn more about SubSpot.</p>
            <Link to="/about" className="dark-purple-link">
              About
            </Link>
          </div>
        </div>
        <div className="image-container">
          <img src={teacherImage} alt="Teacher" className="teacher-image" />
          <img src={substituteImage} alt="Substitute" className="substitute-image" />
        </div>
      </div>
    </div>
  );
}

export default Home;