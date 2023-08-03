import React, { useEffect, useState } from 'react';

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
      {substitutes.map(substitute => (
        <div key={substitute.id}>
          <h3>{substitute.name}</h3>
          <p>Email: {substitute.email}</p>
          <p>Location: {substitute.location}</p>
          <p>Phone: {substitute.phone}</p>
          <p>Qualifications: {substitute.qualifications}</p>
          <p>Verification ID: {substitute.verification_id}</p>
        </div>
      ))}
    </div>
  );
};

export default TeacherDashboard;
