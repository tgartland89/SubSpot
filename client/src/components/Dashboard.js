import React, { useState, useEffect } from "react";
import { getSubstitutes } from './api';

function Dashboard({ userRole }) { 
  console.log('Dashboard role:', userRole); 
  const [substitutes, setSubstitutes] = useState([]);

  useEffect(() => {
    getSubstitutes()
      .then(response => setSubstitutes(response.substitutes))
      .catch(error => console.error(error));
  }, []);

  switch (userRole) {
    case "admin":
      return (
        <div>
          <h1>Welcome to Admin Dashboard</h1>
          <p>Here you can manage teachers and substitutes.</p>
          <p>You have the authority to add, delete, and update users for both tabs.</p>
        </div>
      );
    case "teacher":
      return (
        <div>
          <h1>Welcome to Teacher Dashboard!</h1>
          <p>Here you can view and request substitutes and add reviews.</p>
  <ul>
    {substitutes.map(sub => 
      <li key={sub.id}>
        <a href={`/substitute/${sub.id}`}>{sub.name}</a>
      </li>
    )}
  </ul>
</div>
      );
    case "substitute":
      return (
        <div>
          <h1>Welcome to Substitute Dashboard</h1>
          <p>Here you can manage your substitute-related activities.</p>
          <p>You can view incoming requests and respond to them.</p>
        </div>
      );
    default:
      return <div>User role not recognized.</div>;
  }
};

export default Dashboard;