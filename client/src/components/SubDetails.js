import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

const SubDetails = () => {
  const { substituteId } = useParams();
  const [substituteDetails, setSubstituteDetails] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    fetch(`/substitute/${substituteId}`)
      .then((response) => response.json())
      .then((data) => {
        setSubstituteDetails(data);
      })
      .catch((error) => {
        console.error("Error occurred while fetching substitute details:", error);
      });
  }, [substituteId]);

  const sendRequest = () => {
    if (!substituteDetails) {
      console.error("Substitute details not available.");
      return;
    }
  
    const teacherName = prompt("Enter your name:");
    const teacherEmail = prompt("Enter your email:");
  
    if (!teacherName || !teacherEmail) {
      console.error("Invalid name or email.");
      return;
    }
  
    fetch("/make_request", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        substituteUserId: substituteId,  
        teacherName: teacherName,
        teacherEmail: teacherEmail,
      }),
    })
    
      .then((response) => response.json())
      .then((data) => {
        console.log("Request sent successfully:", data);
        setSuccessMessage("Request sent successfully!");
        setErrorMessage("");
      })
      .catch((error) => {
        console.error("Error sending request:", error);
        setErrorMessage("Failed to send the request. Please try again.");
        setSuccessMessage("");
      });
  };
  
  return (
    <div className="sub-details-box">
      {successMessage && <div className="success-message">{successMessage}</div>}
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      {substituteDetails ? (
        <div>
          <h1>Substitute Details</h1>
          <div className="details-box">
            <h2>Name: {substituteDetails.name}</h2>
          </div>
          <div className="details-box">
            <p>Email: {substituteDetails.email}</p>
          </div>
          <div className="details-box">
            <p>Location: {substituteDetails.location}</p>
          </div>
          <div className="details-box">
            <p>Phone: {substituteDetails.phone}</p>
          </div>
          <div className="details-box">
            <p>Qualifications: {substituteDetails.qualifications}</p>
          </div>
          <div className="details-box">
            <p>Verification ID: {substituteDetails.verification_id}</p>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button onClick={sendRequest}>Request</button>
            <button>Review</button>
          </div>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default SubDetails;