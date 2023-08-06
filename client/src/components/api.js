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

export function getIncomingRequests() {
  return fetch('/get_incoming_requests', {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Failed to fetch incoming requests.');
    }
    return response.json();
  })
  .catch(error => {
    console.error('Network error:', error);
    throw error;
  });
}

export function confirmRequest(requestId) {
  return fetch(`/confirm_request/${requestId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
  .then((response) => {
    if (!response.ok) {
      throw new Error("Failed to confirm request.");
    }
    return response.json();
  })
  .catch(error => {
    console.error('Network error:', error);
    throw error;
  });
}

export function denyRequest(requestId) {
  return fetch(`/deny_request/${requestId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
  .then((response) => {
    if (!response.ok) {
      throw new Error("Failed to deny request.");
    }
    return response.json();
  })
  .catch(error => {
    console.error('Network error:', error);
    throw error;
  });
}
export function makeRequest(substituteId, teacherName, teacherEmail) {
  return fetch('/make_request', {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      substituteId,
      teacherName,
      teacherEmail,
    }),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Failed to make a request.');
    }
    return response.json();
  })
  .catch(error => {
    console.error('Network error:', error);
    throw error;
  });
}