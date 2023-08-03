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

export function getSubstitutes() {
  return fetch('/get_substitutes', {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Failed to fetch substitutes.');
    }
    return response.json();
  })
  .catch(error => {
    console.error('Network error:', error);
    throw error;
  });
}

