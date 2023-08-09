import React, { useState } from "react";



function SignUp() {
  const [role, setRole] = useState("Teacher");
  const [error, setError] = useState("");
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirm_password: "",
    location: "",
    phone: "",
    // Fields specific to Teacher
    school_name: "",
    course_name: "",
    // Fields specific to Substitute
    qualifications: "",
    verification_id: "",
  });

  const [confirmationMessage, setConfirmationMessage] = useState("");

  const handleRoleChange = (event) => {
    setRole(event.target.value);
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData({ ...formData, [name]: value });
  };
  const handleSubmit = (event) => {
    event.preventDefault();
  
    if (formData.password !== formData.confirm_password) {
      setError("Passwords do not match.");
      return;
    }
  
    if (!isStrongPassword(formData.password)) {
      setError(
        "Password is not strong enough. Please include an uppercase and lowercase letter, a digit, a special character, and a length between 8 and 20 characters."
      );
      return;
    }
  
    formData.role = role;
    const apiEndpoint =
      role === "Teacher" ? "/auth/signup-teacher" : "/auth/signup-substitute";
  
    fetch(apiEndpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message) {
          setConfirmationMessage(data.message);
        } else if (data.error) {
          setError(data.error);
        } else {
          console.log("Error occurred during signup.");
        }
      })
      .catch((error) => {
        console.error("Error occurred during signup:", error);
      });
  };

  

// Helper function to check password complexity
const isStrongPassword = (password) => {
  // Define your complexity rules here
  const minLength = 8;
  const maxLength = 20; // New requirement: Maximum length of 20 characters
  const hasUppercase = /[A-Z]/.test(password);
  const hasLowercase = /[a-z]/.test(password);
  const hasDigit = /\d/.test(password);
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

  // Check all complexity rules
  if (
    password.length >= minLength &&
    password.length <= maxLength &&
    hasUppercase &&
    hasLowercase &&
    hasDigit &&
    hasSpecialChar
  ) {
    return true;
  } else {
    return false;
  }
};
  
  return (
    <div className="container">
      <h1>Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Choose Role:</label>
          <select
            className="form-control"
            name="role"
            value={role}
            onChange={handleRoleChange}
          >
            <option value="Teacher">Teacher</option>
            <option value="Substitute">Substitute</option>
          </select>
        </div>
        <br />
        <br />

        <label>Name:</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <br />

        <label>Email:</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <br />

        <label>Password:</label>
        <input
        type="password"
        name="password"
        value={formData.password}
        onChange={handleChange}
   required
/>

{formData.password && (
  <div className="password-validation">
    {isStrongPassword(formData.password) ? (
      <span className="valid">Password is strong!</span>
    ) : (
      <span className="invalid">
        Password is not strong enough. Please include an uppercase and lowercase letter, a digit, a special character, and a length between 8 and 20 characters.
      </span>
    )}
  </div>
)}
<br />

        <label>Confirm Password:</label>
        <input
          type="password"
          name="confirm_password"
          value={formData.confirm_password}
          onChange={handleChange}
          required
        />
        <br />

        {formData.password !== formData.confirm_password && (
          <span style={{ color: "red" }}>Passwords do not match.</span>
        )}
        <br />

        <label>Location:</label>
        <input
          type="text"
          name="location"
          value={formData.location}
          onChange={handleChange}
          required
        />
        <br />

        <label>Phone:</label>
        <input
          type="text"
          name="phone"
          value={formData.phone}
          onChange={handleChange}
          required
        />
        <br />

        {role === "Teacher" && (
  <>
    <label>School Name:</label>
    <input
      type="text"
      name="school_name"
      value={formData.school_name}
      onChange={handleChange}
      required
    />
    <br />

    <label>School Location:</label>
    <input
      type="text"
      name="school_location"
      value={formData.school_location}
      onChange={handleChange}
      required
    />
    <br />

    <label>Course Name:</label>
    <input
      type="text"
      name="course_name"
      value={formData.course_name}
      onChange={handleChange}
      required
    />
    <br />
  </>
)}
        {role === "Substitute" && (
          <>
            <label>Qualifications:</label>
            <input
              type="text"
              name="qualifications"
              value={formData.qualifications}
              onChange={handleChange}
              required
            />
            <br />

            <label>Verification ID:</label>
            <input
              type="text"
              name="verification_id"
              value={formData.verification_id}
              onChange={handleChange}
              required
            />
            <br />
          </>
        )}

        <input type="submit" className="btn btn-primary" value="Sign Up" />
      </form>
      {confirmationMessage && <p>{confirmationMessage}</p>}
      {error && <p className="text-danger">{error}</p>}
    </div>
  );
}

export default SignUp;