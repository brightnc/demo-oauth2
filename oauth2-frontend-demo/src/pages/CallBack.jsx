import React, { useEffect, useState, useCallback, useRef } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { AUTH_SERVER, CLIENT_ID, REDIRECT_URI, CLIENT_SECRET } from "../config";

const Callback = () => {
  const [error, setError] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const hasProcessed = useRef(false);

  const exchangeCodeForToken = useCallback(
    async (code) => {
      try {
        // สร้าง Basic Auth header
        const credentials = btoa(`${CLIENT_ID}:${CLIENT_SECRET}`);
        console.log("Client ID:", CLIENT_ID);
        console.log("Client Secret:", CLIENT_SECRET);
        console.log("Basic Auth:", credentials);

        // Create FormData
        const formData = new FormData();
        formData.append("code", code);
        formData.append("grant_type", "authorization_code");
        formData.append("redirect_uri", REDIRECT_URI);

        // Exchange code for access token
        const response = await fetch(`${AUTH_SERVER}/api/v1/auth/token`, {
          method: "POST",
          headers: {
            Authorization: `Basic ${credentials}`,
          },
          body: formData,
        });

        if (!response.ok) {
          const errorData = await response.json();
          console.error("Token Error:", errorData);
          throw new Error(errorData.detail || "Failed to get access token");
        }

        const data = await response.json();
        console.log("Token Response:", data);

        // Store the access token
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);

        // Clear the state
        localStorage.removeItem("oauth_state");

        // Redirect to home page
        navigate("/");
      } catch (err) {
        console.error("Error:", err);
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setIsProcessing(false);
      }
    },
    [navigate]
  );

  useEffect(() => {
    const handleCallback = async () => {
      // ป้องกันการเรียกซ้ำ
      if (hasProcessed.current) return;
      hasProcessed.current = true;

      // ตรวจสอบ URL parameters
      const code = searchParams.get("code");
      const state = searchParams.get("state");
      const storedState = localStorage.getItem("oauth_state");

      // ตรวจสอบว่ามี code หรือไม่
      if (!code) {
        setError("No authorization code received");
        return;
      }

      // Verify state to prevent CSRF
      if (!state || state !== storedState) {
        setError("Invalid state parameter");
        return;
      }

      setIsProcessing(true);
      // Exchange code for token
      await exchangeCodeForToken(code);
    };

    handleCallback();
  }, [searchParams, exchangeCodeForToken]);

  if (error) {
    return (
      <div style={{ padding: "20px", color: "red" }}>
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={() => navigate("/")}>Back to Login</button>
      </div>
    );
  }

  return (
    <div style={{ padding: "20px", textAlign: "center" }}>
      <h2>{isProcessing ? "Processing login..." : "Redirecting..."}</h2>
      <p>Please wait while we complete your login.</p>
    </div>
  );
};

export default Callback;
