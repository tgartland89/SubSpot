import React, { useState } from "react";


function SignUp() {
  const [role, setRole] = useState("Teacher");
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirm_password: "",
    location: "",
    phone: "",
    school_name: "",
    course_name: "",
    qualifications: "",
    verification_id: "",
  });

  const [confirmationMessage, setConfirmationMessage] = useState("")

  const handleRoleChange = (event) => {
    setRole(event.target.value);
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };
  const handleSubmit = (event) => {
    event.preventDefault();
  
    fetch("/auth/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ...formData, role }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message) {
          setConfirmationMessage(data.message);
        } else {
          console.log("Error occurred during signup.");
        }
      })
      .catch((error) => {
        console.error("Error occurred during signup:", error);
      });
  };
  
  return (
    <div>
      <h1>Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <label>Choose Role:</label>
        <select name="role" value={role} onChange={handleRoleChange}>
          <option value="Teacher">Teacher</option>
          <option value="Substitute">Substitute</option>
        </select>
        <br />
        <br />

        <label>Name:</label>
        <input type="text" name="name" value={formData.name} onChange={handleChange} required />
        <br />

        <label>Email:</label>
        <input type="email" name="email" value={formData.email} onChange={handleChange} required />
        <br />

        <label>Password:</label>
        <input type="password" name="password" value={formData.password} onChange={handleChange} required />
        <br />

        <label>Confirm Password:</label>
        <input type="password" name="confirm_password" value={formData.confirm_password} onChange={handleChange} required />
        <br />

        <label>Location:</label>
        <input type="text" name="location" value={formData.location} onChange={handleChange} required />
        <br />

        <label>Phone:</label>
        <input type="text" name="phone" value={formData.phone} onChange={handleChange} required />
        <br />

        {role === "Teacher" && (
          <>
            <label>School Name:</label>
            <input type="text" name="school_name" value={formData.school_name} onChange={handleChange} required />
            <br />

            <label>Course Name:</label>
            <input type="text" name="course_name" value={formData.course_name} onChange={handleChange} required />
            <br />
          </>
        )}

        {role === "Substitute" && (
          <>
            <label>Qualifications:</label>
            <input type="text" name="qualifications" value={formData.qualifications} onChange={handleChange} required />
            <br />

            <label>Verification ID:</label>
            <input type="text" name="verification_id" value={formData.verification_id} onChange={handleChange} required />
            <br />
          </>
        )}

        <input type="submit" value="Sign Up" />
      </form>
      {confirmationMessage && <p>{confirmationMessage}</p>}
    </div>
  );
}

export default SignUp;
