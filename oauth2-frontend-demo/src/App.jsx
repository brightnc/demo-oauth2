import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Callback from "./pages/CallBack";
import Home from "./pages/Home";
import "./App.css";
import { Navigate } from "react-router-dom";

function App() {
  // Protected Route component
  const ProtectedRoute = ({ children }) => {
    const token = localStorage.getItem("access_token");

    // ถ้าไม่มี token ให้ redirect ไปหน้า login
    if (!token) {
      return <Navigate to="/login" replace />;
    }

    // ตรวจสอบว่า token เป็น UUID ที่ถูกต้อง
    const uuidRegex =
      /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    if (!uuidRegex.test(token)) {
      console.error("Invalid token format");
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      return <Navigate to="/login" replace />;
    }

    return children;
  };

  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/callback" element={<Callback />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

