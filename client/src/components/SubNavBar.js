import React from 'react';
import { Link } from 'react-router-dom'; 

const SubNavBar = () => {
  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/logout">Log Out</Link></li>
      </ul>
    </nav>
  );
};

export default SubNavBar;
