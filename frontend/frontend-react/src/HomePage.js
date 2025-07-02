import React, { useState } from "react";

export default function HomePage({ user, onLogout }) {
  const [file, setFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setError(""); // Limpa erro anterior
    setResult(null); // Limpa resultado anterior
    
    // Cria preview da imagem
    if (selectedFile) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setImagePreview(event.target.result);
      };
      reader.readAsDataURL(selectedFile);
    } else {
      setImagePreview(null);
    }
  };

  const handleSend = async () => {
    if (!file) {
      setError("Por favor, selecione uma imagem.");
      return;
    }

    setLoading(true);
    setError("");
    
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/process_trash_image", {
        method: "POST",
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Erro ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      setResult(data);
      
      // Adiciona ao histórico
      const historyItem = {
        id: Date.now(),
        fileName: file.name,
        imagePreview: imagePreview,
        classification: data.image_classification,
        timestamp: new Date().toLocaleString('pt-BR')
      };
      
      setHistory(prev => [historyItem, ...prev.slice(0, 4)]); // Mantém apenas os últimos 5
      
    } catch (err) {
      setError(`Erro ao processar imagem: ${err.message}`);
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const clearSelection = () => {
    setFile(null);
    setImagePreview(null);
    setResult(null);
    setError("");
    // Limpa o input file
    const fileInput = document.getElementById('imageInput');
    if (fileInput) fileInput.value = '';
  };

  const clearHistory = () => {
    setHistory([]);
  };

  return (
    <div className="home-page">
      {/* Header com logo e informações do usuário */}
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">♻️</span>
            <span className="logo-text">Sistema de Resíduos</span>
          </div>
          <div className="user-info">
            <span className="user-name">Olá, {user?.full_name || user?.username}</span>
            <button onClick={onLogout} className="logout-btn">
              Sair
            </button>
          </div>
        </div>
      </header>

      <div className="home-container">
        <h2>Classificação de Resíduos</h2>
        
        <div className="upload-section">
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleFileChange}
            id="imageInput"
          />
          
          {imagePreview && (
            <div className="image-preview">
              <h3>Imagem Selecionada:</h3>
              <img src={imagePreview} alt="Preview" />
              <div className="image-info">
                <p><strong>Nome:</strong> {file?.name}</p>
                <p><strong>Tamanho:</strong> {(file?.size / 1024).toFixed(2)} KB</p>
              </div>
              <button onClick={clearSelection} className="clear-btn">
                Limpar Seleção
              </button>
            </div>
          )}
          
          <button onClick={handleSend} disabled={loading || !file}>
            {loading ? "Processando..." : "Enviar para Classificação"}
          </button>
        </div>
        
        {error && <div className="error">{error}</div>}
        
        {result && (
          <div className="result">
            <h3>Resultado da Classificação:</h3>
            <div className="result-grid">
              <div className="result-item">
                <span className="label">Classificação:</span>
                <span className="value classification">{result.image_classification}</span>
              </div>
              <div className="result-item">
                <span className="label">Instruções:</span>
                <span className="value">{result.discard_instructions}</span>
              </div>
              <div className="result-item">
                <span className="label">Dicas:</span>
                <span className="value">{result.discard_tips}</span>
              </div>
            </div>
          </div>
        )}

        {/* Histórico de processamentos */}
        {history.length > 0 && (
          <div className="history-section">
            <div className="history-header">
              <h3>Histórico Recente</h3>
              <button onClick={clearHistory} className="clear-btn small">
                Limpar Histórico
              </button>
            </div>
            <div className="history-grid">
              {history.map((item) => (
                <div key={item.id} className="history-item">
                  <img src={item.imagePreview} alt={item.fileName} />
                  <div className="history-info">
                    <p className="history-filename">{item.fileName}</p>
                    <p className="history-classification">
                      <strong>Classificação:</strong> {item.classification}
                    </p>
                    <p className="history-timestamp">{item.timestamp}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}