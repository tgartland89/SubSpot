import React, { useEffect, useState } from "react";

const AdminDashboard = () => {
  const [teachers, setTeachers] = useState([]);
  const [substitutes, setSubstitutes] = useState([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch("/get_users");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      setTeachers(data.teachers);
      setSubstitutes(data.substitutes);
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };

  const handleDeleteUser = (userId) => {

  };

  return (
    <div>
      <h1>Admin Dashboard</h1>
      <div>
        <h2>Teachers</h2>
        {teachers.map((teacher) => (
          <div key={teacher.id}>
            <h3>{teacher.name}</h3>
            <p>Email: {teacher.email}</p>
            <p>Location: {teacher.location}</p>
            <p>Phone: {teacher.phone}</p>
            <button onClick={() => handleDeleteUser(teacher.id)}>Delete</button>
          </div>
        ))}
      </div>
      <div>
        <h2>Substitutes</h2>
        {substitutes.map((substitute) => (
          <div key={substitute.id}>
            <h3>{substitute.name}</h3>
            <p>Email: {substitute.email}</p>
            <p>Location: {substitute.location}</p>
            <p>Phone: {substitute.phone}</p>
            <p>Qualifications: {substitute.qualifications}</p>
            <p>Verification ID: {substitute.verification_id}</p>
            <button onClick={() => handleDeleteUser(substitute.id)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminDashboard;