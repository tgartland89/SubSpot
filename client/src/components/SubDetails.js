import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

const SubDetails = () => {
  const { substituteId } = useParams();
  const [substituteDetails, setSubstituteDetails] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [teacherUserId, setTeacherUserId] = useState(null); 

  useEffect(() => {
    fetch(`/substitute/${substituteId}`)
      .then((response) => response.json())
      .then((data) => {
        setSubstituteDetails(data);
      })
      .catch((error) => {
        console.error("Error occurred while fetching substitute details:", error);
      });

   
    fetch('/get_teacher_user_id')
      .then((response) => response.json())
      .then((data) => {
        setTeacherUserId(data.teacher_user_id);
      })
      .catch((error) => {
        console.error("Error occurred while fetching teacher user ID:", error);
      });
  }, [substituteId]);

  const sendRequest = async () => {
    if (!substituteDetails || !teacherUserId) {
      console.error("Substitute details or teacher's user ID not available.");
      return;
    }

    const teacherName = prompt("Enter your name:");
    const teacherEmail = prompt("Enter your email:");

    if (!teacherName || !teacherEmail) {
      console.error("Invalid name or email.");
      return;
    }

    try {
      const response = await fetch('/make_request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          substitute_id: substituteDetails.user_id,
          teacherName: teacherName,
          teacherEmail: teacherEmail,
          teacherUserId: teacherUserId, 
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Request sent successfully:', data);
        setSuccessMessage("Request sent successfully!");
        setErrorMessage("");
      } else {
        console.error('Error sending request:', response.statusText);
        setErrorMessage("Failed to send the request. Please try again.");
        setSuccessMessage("");
      }
    } catch (error) {
      console.error('Network error:', error);
      setErrorMessage("Failed to send the request. Please try again.");
      setSuccessMessage("");
    }
  };
  
  
  return (
    <div className="sub-details-box light-blue-bg">
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