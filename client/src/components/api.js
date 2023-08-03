export const loginUser = (email, password) => {
  return fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  }).then((response) => {
    if (!response.ok) {
      throw new Error("Failed to log in. Please check your credentials and try again.");
    }
    return response.json();
  });
};