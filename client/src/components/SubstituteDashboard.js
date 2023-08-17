import React, { useEffect, useState } from "react";
import { getIncomingRequests, respondToRequest } from "./api"; 

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

  const handleRespondToRequest = (requestId, response, message) => {
    respondToRequest(requestId, response, message)
      .then(() => {
        setIncomingRequests((prevRequests) =>
          prevRequests.map((request) =>
            request.id === requestId ? { ...request, confirmation: response } : request
          )
        );
      })
      .catch((error) => console.error("Error responding to request:", error));
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
              <button onClick={() => handleRespondToRequest(request.id, "Accept", "Accepted the request.")}>Accept</button>
              <button onClick={() => handleRespondToRequest(request.id, "Decline", "Declined the request.")}>Decline</button>
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
