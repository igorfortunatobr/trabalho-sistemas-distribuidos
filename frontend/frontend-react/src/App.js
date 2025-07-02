import React, { useState } from "react";
import LoginPage from "./LoginPage";
import RegisterPage from "./RegisterPage";
import HomePage from "./HomePage";
import "./App.css";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);

  const handleLoginSuccess = (user) => {
    setIsAuthenticated(true);
    setCurrentUser(user);
    setShowRegister(false);
  };

  const handleRegisterSuccess = () => {
    setShowRegister(false);
    // Mostrar mensagem de sucesso ou redirecionar para login
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setCurrentUser(null);
    setShowRegister(false);
  };

  const handleShowRegister = () => {
    setShowRegister(true);
  };

  return (
    <div className="App">
      {isAuthenticated ? (
        <HomePage user={currentUser} onLogout={handleLogout} />
      ) : showRegister ? (
        <RegisterPage onRegisterSuccess={handleRegisterSuccess} />
      ) : (
        <LoginPage onLoginSuccess={handleLoginSuccess} onShowRegister={handleShowRegister} />
      )}
    </div>
  );
}

export default App;
