import React, { useEffect, useState } from "react";

const AdminDashboard = () => {
  console.log("Admin Dashboard rendered");
  const [teachers, setTeachers] = useState([]);
  const [substitutes, setSubstitutes] = useState([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const responseTeachers = await fetch("/get_teachers");
      const responseSubstitutes = await fetch("/get_substitutes");

      if (!responseTeachers.ok || !responseSubstitutes.ok) {
        throw new Error("Network response was not ok");
      }

      const dataTeachers = await responseTeachers.json();
      const dataSubstitutes = await responseSubstitutes.json();

      setTeachers(dataTeachers.teachers);
      setSubstitutes(dataSubstitutes.substitutes);
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