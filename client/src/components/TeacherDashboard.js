import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const TeacherDashboard = () => {
  const [substitutes, setSubstitutes] = useState([]);

  useEffect(() => {
    fetchSubstitutes();
  }, []);

  const fetchSubstitutes = async () => {
    try {
      const response = await fetch('/get_substitutes');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setSubstitutes(data.substitutes);
    } catch (error) {
      console.error('Error fetching substitutes:', error);
    }
  };

  return (
    <div>
      <h1>Teacher Dashboard</h1>
      <p>Welcome to Teacher Dashboard!</p>
      <p>Here you can view and request substitutes and add reviews.</p>
      <hr />
      <h2>Available Substitutes:</h2>
      <ul>
        {substitutes.map((substitute) => (
          <li key={substitute.id}>
            <Link to={`/sub-details/${substitute.id}`}>{substitute.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TeacherDashboard;