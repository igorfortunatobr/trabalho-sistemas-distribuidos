# Frontend React - Sistema de Classificação de Resíduos

Este é o frontend React para o sistema de classificação e descarte de resíduos.

## Funcionalidades

- **Login simples**: Autenticação com credenciais fictícias
- **Upload de imagem**: Interface para enviar imagens de resíduos
- **Classificação**: Exibe o resultado da classificação e instruções de descarte
- **Design responsivo**: Funciona em desktop e mobile

## Como usar

### 1. Instalar dependências
```bash
npm install
```

### 2. Iniciar o servidor de desenvolvimento
```bash
npm start
```

O aplicativo abrirá automaticamente em [http://localhost:3000](http://localhost:3000).

### 3. Fazer login
Use as credenciais:
- **Usuário**: `admin`
- **Senha**: `123456`

### 4. Enviar imagem
Após o login, você será redirecionado para a tela de upload onde pode:
1. Selecionar uma imagem de resíduo
2. Clicar em "Enviar"
3. Ver o resultado da classificação e instruções de descarte

## Pré-requisitos

Certifique-se de que o backend (API) esteja rodando em `http://localhost:8000` antes de usar o frontend.

Para iniciar o backend:
```bash
cd ../api
docker compose up --build -d
```

## Estrutura do projeto

```
src/
├── App.js              # Componente principal com lógica de autenticação
├── LoginPage.js        # Tela de login
├── HomePage.js         # Tela principal com upload de imagem
├── App.css             # Estilos CSS
└── index.js            # Ponto de entrada da aplicação
```

## Tecnologias utilizadas

- React 19.1.0
- CSS3 com design responsivo
- Fetch API para comunicação com o backend
