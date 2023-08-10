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
    school_name: "",
    course_name: "",
    qualifications: "",
    verification_id: "",
  });

  const [confirmationMessage, setConfirmationMessage] = useState("");

  const handleRoleChange = (event) => {
    const newRole = event.target.value;
    setRole(newRole);

    setFormData({
      name: "",
      email: "",
      password: "",
      confirm_password: "",
      location: "",
      phone: "",
      school_name: "",
      school_location: "", 
      course_name: "",
      qualifications: "",
      verification_id: "",
    });
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

const isStrongPassword = (password) => {

  const minLength = 8;
  const maxLength = 20; 
  const hasUppercase = /[A-Z]/.test(password);
  const hasLowercase = /[a-z]/.test(password);
  const hasDigit = /\d/.test(password);
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

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
        <label className="form-label">Choose Role:</label>
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

      <div className="form-group">
        <label className="form-label">Name:</label>
        <div>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="form-control"
          />
          <small className="form-text text-muted">First and Last Name</small>
        </div>
      </div>

      <div className="form-group">
        <label className="form-label">Email:</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
          className="form-control"
        />
      </div>

      <div className="form-group">
        <label className="form-label">Password:</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
          className="form-control"
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
      </div>

      <div className="form-group">
        <label className="form-label">Confirm Password:</label>
        <input
          type="password"
          name="confirm_password"
          value={formData.confirm_password}
          onChange={handleChange}
          required
          className="form-control"
        />
        {formData.password !== formData.confirm_password && (
          <span className="invalid">Passwords do not match.</span>
        )}
      </div>

      <div className="form-group">
        <label className="form-label">Location:</label>
        <div>
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            required
            className="form-control"
          />
          <small className="form-text text-muted">City, State, Zip code</small>
        </div>
      </div>

      <div className="form-group">
        <label className="form-label">Phone:</label>
        <input
          type="text"
          name="phone"
          value={formData.phone}
          onChange={handleChange}
          required
          className="form-control"
        />
      </div>
      <br />

  {role === "Teacher" && (
        <>
          <div className="form-group">
            <label className="form-label">School Name:</label>
            <input
              type="text"
              name="school_name"
              value={formData.school_name}
              onChange={handleChange}
              required
              className="form-control"
            />
          </div>

          <div className="form-group">
            <label className="form-label">School Address:</label>
            <input
              type="text"
              name="school_location"
              value={formData.school_location}
              onChange={handleChange}
              required
              className="form-control"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Course Name:</label>
            <input
              type="text"
              name="course_name"
              value={formData.course_name}
              onChange={handleChange}
              required
              className="form-control"
            />
          </div>
        </>
      )}

      {role === "Substitute" && (
        <>
          <div className="form-group">
            <label className="form-label">Qualifications:</label>
            <input
              type="text"
              name="qualifications"
              value={formData.qualifications}
              onChange={handleChange}
              required
              className="form-control"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Verification ID:</label>
            <input
              type="text"
              name="verification_id"
              value={formData.verification_id}
              onChange={handleChange}
              required
              className="form-control"
            />
          </div>
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