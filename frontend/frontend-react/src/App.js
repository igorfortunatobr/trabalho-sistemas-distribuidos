import React, { useState, useEffect } from "react";
import LoginPage from "./LoginPage";
import RegisterPage from "./RegisterPage";
import HomePage from "./HomePage";
import "./App.css";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const handleLoginSuccess = (user) => {
    setIsAuthenticated(true);
    setCurrentUser(user);
    setShowRegister(false);
  };

  const handleRegisterSuccess = () => {
    setShowRegister(false);
    // Mostrar mensagem de sucesso ou redirecionar para login
  };

  const handleShowRegister = () => {
    setShowRegister(true);
  };

  // Verificar token ao carregar a aplicação
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      
      if (token) {
        try {
          // Usar o endpoint /me para obter dados do usuário atual
          const response = await fetch('http://localhost:8000/me', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json',
            },
          });
          
          if (response.ok) {
            const data = await response.json();
            setIsAuthenticated(true);
            setCurrentUser(data.user);
          } else {
            // Token inválido, limpar localStorage
            localStorage.removeItem('token');
            localStorage.removeItem('user');
          }
        } catch (error) {
          console.error('Erro ao verificar token:', error);
          localStorage.removeItem('token');
          localStorage.removeItem('user');
        }
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const handleLogout = () => {
    setIsAuthenticated(false);
    setCurrentUser(null);
    setShowRegister(false);
    localStorage.removeItem('token');
  };

  if (isLoading) {
    return <div className="App">Carregando...</div>;
  }

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
