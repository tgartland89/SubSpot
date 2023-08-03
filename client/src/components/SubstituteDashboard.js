import React, { useEffect, useState } from "react";

const SubstituteDashboard = () => {
  const [incomingRequests, setIncomingRequests] = useState([]);

  useEffect(() => {
    fetchIncomingRequests();
  }, []);

  const fetchIncomingRequests = async () => {
    try {
      const response = await fetch("/get_incoming_requests");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      setIncomingRequests(data.requests);
    } catch (error) {
      console.error("Error fetching incoming requests:", error);
    }
  };

  const handleConfirmRequest = (requestId) => {

  };

  const handleDenyRequest = (requestId) => {

  };

  return (
    <div>
      <h1>Substitute Dashboard</h1>
      <h2>Incoming Requests</h2>
      {incomingRequests.map((request) => (
        <div key={request.id}>
          <h3>From: {request.teacher_name}</h3>
          <p>School: {request.teacher_school}</p>
          <p>Course: {request.course_being_covered}</p>
          <button onClick={() => handleConfirmRequest(request.id)}>Confirm</button>
          <button onClick={() => handleDenyRequest(request.id)}>Deny</button>
        </div>
      ))}
    </div>
  );
};

export default SubstituteDashboard;