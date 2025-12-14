import { BrowserRouter, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import BookList from "./components/BookList";
import Login from "./components/Login";

function App() {
  const token = localStorage.getItem("token");

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/books"
          element={
            <ProtectedRoute token={token}>
              <BookList />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
