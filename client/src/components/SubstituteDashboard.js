import React, { useEffect, useState } from "react";
import { getIncomingRequests, confirmRequest, denyRequest } from './api';

const SubstituteDashboard = () => {
  const [incomingRequests, setIncomingRequests] = useState([]);

  useEffect(() => {
    fetchIncomingRequests();
  }, []);

  const fetchIncomingRequests = async () => {
    try {
      const response = await getIncomingRequests();
      setIncomingRequests(response.incoming_requests);
    } catch (error) {
      console.error("Error fetching incoming requests:", error);
    }
  };

  const handleConfirmRequest = (requestId) => {
    confirmRequest(requestId)
      .then(() => {
        const updatedRequests = incomingRequests.map((request) =>
          request.id === requestId ? { ...request, confirmation: "Accept" } : request
        );
        setIncomingRequests(updatedRequests);
      })
      .catch((error) => console.error("Error confirming request:", error));
  };

  const handleDenyRequest = (requestId) => {
    denyRequest(requestId)
      .then(() => {
        const updatedRequests = incomingRequests.map((request) =>
          request.id === requestId ? { ...request, confirmation: "Decline" } : request
        );
        setIncomingRequests(updatedRequests);
      })
      .catch((error) => console.error("Error denying request:", error));
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
          {request.confirmation === null ? (
            <div>
              <button onClick={() => handleConfirmRequest(request.id)}>Confirm</button>
              <button onClick={() => handleDenyRequest(request.id)}>Deny</button>
            </div>
          ) : (
            <p>Confirmation: {request.confirmation}</p>
          )}
        </div>
      ))}
    </div>
  );
};

export default SubstituteDashboard;