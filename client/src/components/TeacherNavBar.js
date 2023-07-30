import React from 'react';
import { Link } from 'react-router-dom';

const TeacherNavBar = () => {
  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/teacher-dashboard">Teacher Dashboard</Link></li>
        <li><Link to="/reviews">Reviews</Link></li>
        <li><Link to="/logout">Log Out</Link></li>
      </ul>
    </nav>
  );
};

export default TeacherNavBar;
