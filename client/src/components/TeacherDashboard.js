import React, { useState, useEffect } from "react";
import SubsDetails from "./SubDetails";

const TeacherDashboard = () => {
  const [substitutes, setSubstitutes] = useState([]);

  useEffect(() => {
    // Fetch the list of substitutes when the component mounts
    fetch("/teacher-dashboard")
      .then((response) => response.json())
      .then((data) => {
        if (data.substitutes) {
          setSubstitutes(data.substitutes);
        }
      })
      .catch((error) => {
        console.error("Error occurred while fetching substitutes:", error);
      });
  }, []);

  const handleRequest = (substituteId) => {
    // Implement the logic to make a request to the selected substitute
    // You can send a request to the backend here to create a new request for the substitute
    console.log("Request sent to substitute with ID:", substituteId);
  };

  return (
    <div>
      <h1>Welcome to Teacher Dashboard</h1>
      <p>Here you can view and request substitutes and add reviews.</p>
      {substitutes.map((substitute) => (
        <div key={substitute.id}>
          <h2>{substitute.name}</h2>
          <p>Email: {substitute.email}</p>
          <p>Location: {substitute.location}</p>
          <p>Phone: {substitute.phone}</p>
          <p>Qualifications: {substitute.qualifications}</p>
          <p>Verification ID: {substitute.verification_id}</p>
          <button onClick={() => handleRequest(substitute.id)}>Request</button>
          <button>Review</button>
        </div>
      ))}
    </div>
  );
};

export default TeacherDashboard;
