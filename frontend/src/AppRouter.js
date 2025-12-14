import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import Login from "./Login";
import BookList from "./components/BookList";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import { getBooks, logout } from "./services/api";

function AppRouter() {
  const [books, setBooks] = useState([]);
  const [token, setToken] = useState(localStorage.getItem("token") || "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) return;

    setLoading(true);
    setError("");

    getBooks(token)
      .then((data) => setBooks(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [token]);

  const handleLogout = () => {
    logout();
    setToken("");
    setBooks([]);
  };

  return (
    <BrowserRouter>
      {token && <Navbar onLogout={handleLogout} />}
      <Routes>
        {/* Login route */}
        <Route
          path="/login"
          element={
            token ? <Navigate to="/books" /> : <Login onLogin={setToken} />
          }
        />

        {/* Protected books route */}
        <Route
          path="/books"
          element={
            <ProtectedRoute token={token}>
              {loading && <p>Loading books...</p>}
              {error && <p style={{ color: "red" }}>{error}</p>}
              <BookList books={books} />
            </ProtectedRoute>
          }
        />

        {/* Default route */}
        <Route
          path="*"
          element={
            token ? <Navigate to="/books" /> : <Navigate to="/login" />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRouter;
