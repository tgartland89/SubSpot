import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { makeRequest } from './api'; 

const TeacherDashboard = () => {
  const [substitutes, setSubstitutes] = useState([]);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

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

  const handleRequest = (substituteId, substituteName) => {
    const teacherName = ''; 
    const teacherEmail = ''; 

    makeRequest(substituteId, teacherName, teacherEmail)
      .then((data) => {
        console.log('Request sent successfully:', data);
        setSuccessMessage("Request sent successfully!");
        setErrorMessage("");
      })
      .catch((error) => {
        console.error('Error sending request:', error);
        setErrorMessage("Failed to send the request. Please try again.");
        setSuccessMessage("");
      });
  };

  return (
    <div>
      {successMessage && <div className="success-message">{successMessage}</div>}
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      <h1>Teacher Dashboard</h1>
      <p>Here you can view and request substitutes and add reviews.</p>
      <hr />
      <h2>Available Substitutes:</h2>
      <ul>
        {substitutes.map((substitute) => (
          <li key={substitute.id}>
            <Link to={`/sub-details/${substitute.id}`} className="dark-purple-link mr-2">{substitute.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TeacherDashboard;