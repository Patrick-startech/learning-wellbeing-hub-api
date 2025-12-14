import "./App.css";
import { useState, useEffect } from "react";
import Login from "./Login";
import BookList from "./components/BookList";
import Navbar from "./components/Navbar";
import { getBooks, logout } from "./services/api";

function App() {
  const [books, setBooks] = useState([]);
  const [token, setToken] = useState(localStorage.getItem("access_token") || "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Fetch books when token changes
  useEffect(() => {
    if (!token) return;

    const fetchBooks = async () => {
      setLoading(true);
      setError("");

      try {
        const data = await getBooks();
        setBooks(data);
      } catch (err) {
        console.error("Error fetching books:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchBooks();
  }, [token]);

  // Logout handler
  const handleLogout = () => {
    logout();
    setToken("");
    setBooks([]);
  };

  return (
    <div className="App">
      {token && <Navbar onLogout={handleLogout} />}
      {!token ? (
        <Login onLogin={setToken} />
      ) : (
        <div>
          {loading && <p>Loading books...</p>}
          {error && <p style={{ color: "red" }}>{error}</p>}
          {books.length > 0 ? (
            <BookList books={books} />
          ) : (
            !loading && <p>No books available</p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
