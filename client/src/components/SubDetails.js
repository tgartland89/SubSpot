import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

const SubsDetails = () => {
  const { substituteId } = useParams();
  const [substituteDetails, setSubstituteDetails] = useState(null);

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

  if (!substituteDetails) {

    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Substitute Details</h1>
      <h2>Name: {substituteDetails.name}</h2>
      <p>Email: {substituteDetails.email}</p>
      <p>Location: {substituteDetails.location}</p>
      <p>Phone: {substituteDetails.phone}</p>
      <p>Qualifications: {substituteDetails.qualifications}</p>
      <p>Verification ID: {substituteDetails.verification_id}</p>
      <button>Request</button>
      <button>Review</button>
    </div>
  );
};

export default SubsDetails;