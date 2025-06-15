// OAuth2 Configuration
export const AUTH_SERVER = "http://localhost:8000"; // Your OAuth server URL
export const CLIENT_ID = "35dbeee0-7c8c-4c8c-9838-849afd478f9c"; // Your OAuth client ID
export const CLIENT_SECRET = "e76da986-b553-4e14-aee5-cdfa6a105d80"; // Your OAuth client secret
export const REDIRECT_URI = "http://localhost:5173/callback"; // Your app's callback URL

// Helper function to generate random state string
export const generateRandomString = () => {
  const array = new Uint32Array(28);
  window.crypto.getRandomValues(array);
  return Array.from(array, (dec) => ("0" + dec.toString(16)).substr(-2)).join(
    ""
  );
};
