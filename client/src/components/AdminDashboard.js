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
  const handleDeleteUser = async (userId) => {
    try {
      const response = await fetch(`/delete_user/${userId}`, {
        method: "DELETE",
      });
      if (response.ok) {
        fetchUsers();
      } else {
        throw new Error("Failed to delete user.");
      }
    } catch (error) {
      console.error("Error deleting user:", error);
    }
  };
  

  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard</h1>
      <div className="teacher-section">
        <h2>Teachers</h2>
        {teachers.map((teacher) => (
          <div className="teacher-card" key={teacher.id}>
            <h3>{teacher.name}</h3>
            <p>Email: {teacher.email}</p>
            <p>Location: {teacher.location}</p>
            <p>Phone: {teacher.phone}</p>
            <button
              className="delete-button"
              onClick={() => handleDeleteUser(teacher.id)}
            >
              Delete
            </button>
          </div>
        ))}
      </div>
      <div className="substitute-section">
        <h2>Substitutes</h2>
        {substitutes.map((substitute) => (
          <div className="substitute-card" key={substitute.id}>
            <h3>{substitute.name}</h3>
            <p>Email: {substitute.email}</p>
            <p>Location: {substitute.location}</p>
            <p>Phone: {substitute.phone}</p>
            <p>Qualifications: {substitute.qualifications}</p>
            <p>Verification ID: {substitute.verification_id}</p>
            <button
              className="delete-button"
              onClick={() => handleDeleteUser(substitute.id)}
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminDashboard;