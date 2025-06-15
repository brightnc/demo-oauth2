// OAuth2 Configuration
export const AUTH_SERVER = "http://localhost:8000"; // Your OAuth server URL
export const CLIENT_ID = ""; // Your OAuth client ID
export const CLIENT_SECRET = ""; // Your OAuth client secret
export const REDIRECT_URI = "http://localhost:5173/callback"; // Your app's callback URL

// Helper function to generate random state string
export const generateRandomString = () => {
  const array = new Uint32Array(28);
  window.crypto.getRandomValues(array);
  return Array.from(array, (dec) => ("0" + dec.toString(16)).substr(-2)).join(
    ""
  );
};
