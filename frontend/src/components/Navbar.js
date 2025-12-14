import React from "react";

function Navbar({ onLogout }) {
  return (
    <nav style={{ padding: "10px", background: "#282c34", color: "white" }}>
      <h3>📚 Learning & Wellbeing Hub</h3>
      <button onClick={onLogout} style={{ marginLeft: "20px" }}>
        Logout
      </button>
    </nav>
  );
}

export default Navbar;
