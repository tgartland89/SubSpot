export const loginUser = (email, password) => {
  return fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  }).then((response) => response.json());
};