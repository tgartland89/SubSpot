import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { makeRequest } from './api'; 

const TeacherDashboard = ({ userName, userEmail, teacherId, teacherUserId }) => { 
  console.log("Teacher ID in TeacherDashboard:", teacherId); 

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

  // eslint-disable-next-line
  const handleRequest = (substituteId, substituteName) => {
    const teacherName = userName;
    const teacherEmail = userEmail;

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
      <div className="substitutes-box"> {/* New container */}
        <ul>
          {substitutes.map((substitute) => (
            <li key={substitute.user_id}>
              <Link to={`/sub-details/${substitute.user_id}`} className="dark-purple-link mr-2">
                {substitute.name}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default TeacherDashboard;