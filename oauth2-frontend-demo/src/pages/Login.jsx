import {
  AUTH_SERVER,
  CLIENT_ID,
  generateRandomString,
  REDIRECT_URI,
} from "../config";

const Login = () => {
  const handleLogin = () => {
    const state = generateRandomString();
    localStorage.setItem("oauth_state", state);

    // สร้าง URL สำหรับขอ authorization
    const authUrl =
      `${AUTH_SERVER}/api/v1/auth/authorize?` +
      `client_id=${CLIENT_ID}&` +
      `response_type=code&` +
      `redirect_uri=${encodeURIComponent(REDIRECT_URI)}&` +
      `scope=read&` +
      `state=${state}`;

    // redirect ไปยัง authorization server
    window.location.href = authUrl;
  };

  return <button onClick={handleLogin}>Login with OAuth</button>;
};

export default Login;
