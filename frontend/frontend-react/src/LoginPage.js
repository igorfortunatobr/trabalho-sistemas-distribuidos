import React, { useState } from "react";

export default function LoginPage({ onLoginSuccess, onShowRegister }) {
  const [user, setUser] = useState("");
  const [pass, setPass] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json" 
        },
        body: JSON.stringify({ username: user, password: pass }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        // Salvar apenas o token no localStorage
        localStorage.setItem('token', data.token);
        onLoginSuccess(data.user);
      } else {
        setError(data.error || "Erro no login");
      }
    } catch (err) {
      setError("Erro de conexão com o servidor");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleLogin}>
        <h2>Login</h2>
        <input
          type="text"
          placeholder="Usuário"
          value={user}
          onChange={(e) => setUser(e.target.value)}
          required
          disabled={loading}
        />
        <input
          type="password"
          placeholder="Senha"
          value={pass}
          onChange={(e) => setPass(e.target.value)}
          required
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? "Entrando..." : "Entrar"}
        </button>
        {error && <div className="error">{error}</div>}
        <div className="login-info">
          <p>Não tem uma conta?</p>
          <button 
            type="button" 
            onClick={onShowRegister}
            className="link-btn"
          >
            Cadastrar-se
          </button>
        </div>
      </form>
    </div>
  );
}