# ♻️ Sistema Distribuído de Classificação e Descarte de Resíduos

## 👥 Membros do Grupo

  * [FELLIPE SILVERIO BRANDAO]
  * [IGOR ABREU FORTUNATO]
  * [ROBSON FERREIRA DOS SANTOS JUNIOR]
  * [VITOR MOREIRA DOS SANTOS]

-----

Este projeto implementa um sistema distribuído inteligente para auxiliar no descarte correto de resíduos. Ele combina inteligência artificial visual para classificar tipos de lixo com inteligência artificial textual para fornecer instruções detalhadas de descarte, tudo orquestrado em um ambiente de microsserviços containerizados.

-----

## 💡 Validação do Problema (Requisito 5)

A gestão inadequada de resíduos sólidos urbanos é um problema ambiental global crescente. A falta de conhecimento sobre como descartar corretamente diferentes tipos de materiais leva a taxas de reciclagem baixas, contaminação de recicláveis e aumento da poluição. Muitos materiais que poderiam ser reciclados acabam em aterros sanitários, enquanto resíduos perigosos são descartados de forma incorreta, causando danos ao meio ambiente e à saúde pública.

**A "dor" que este projeto visa resolver é a falta de informação e a complexidade percebida no descarte consciente.** Ao fornecer uma ferramenta simples e acessível que classifica visualmente o lixo e imediatamente oferece instruções claras de descarte, buscamos capacitar indivíduos a tomar decisões mais informadas, contribuindo para:

  * **Aumento das taxas de reciclagem:** Facilitando a separação correta.
  * **Redução da contaminação:** Orientando sobre o que não é reciclável ou requer tratamento especial.
  * **Conscientização ambiental:** Educando sobre as melhores práticas de descarte.

Nosso sistema atua como um guia prático, transformando a tarefa de descartar o lixo em um processo mais fácil e eficaz para o cidadão comum, impactando positivamente a sustentabilidade e a economia circular.

### Referências:

  * [Global Waste Management Outlook 2024 - UNEP](https://www.google.com/search?q=https://www.unep.org/resources/report/global-waste-management-outlook-2024)
  * [The World Bank - Waste Management](https://www.worldbank.org/en/topic/urbandevelopment/brief/solid-waste-management)
  * [MMA - Gerenciamento de Resíduos Sólidos](https://www.google.com/search?q=https://www.gov.br/mma/pt-br/assuntos/qualidade-ambiental/gerenciamento-de-residuos-solidos)

-----

## ⚙️ Como Funciona?

O sistema é composto por três microsserviços independentes que colaboram para processar a solicitação do usuário:

1.  **`image-classifier`**: Recebe uma imagem de um item de lixo. Utiliza um modelo de **Vision Transformer (ViT)** pré-treinado no Hugging Face (`tribber93/my-trash-classification`) e fine-tunado para classificar a imagem em uma das seguintes categorias: `cardboard` (papelão), `glass` (vidro), `metal` (metal), `paper` (papel), `plastic` (plástico) ou `trash` (lixo comum/não reciclável).
2.  **`text-generator`**: Recebe o tipo de material classificado. Consulta uma base de dados interna de regras de descarte para gerar instruções detalhadas e dicas relevantes para aquele material.
3.  **`api-gateway` (Orquestrador)**: Este é o ponto de entrada principal do sistema. Ele recebe a imagem do usuário, encaminha-a para o `image-classifier`, pega o resultado da classificação, o envia para o `text-generator` e, finalmente, combina a classificação e as instruções de descarte em uma única resposta para o usuário.

Todo o sistema é **containerizado** usando **Docker** e orquestrado com **Docker Compose**, garantindo isolamento, portabilidade e fácil implantação.

-----

## 🎯 Atendimento aos Requisitos do Trabalho

Este projeto foi cuidadosamente projetado para atender a todos os requisitos do trabalho de Sistemas Distribuídos:

### 1\. Agentes de IA (10 pts)

  * **Mínimo de dois agentes (modelos) de IA:**
      * **Agente 1 (Visão):** O serviço `image-classifier` utiliza um modelo **Vision Transformer (ViT)**, uma arquitetura de Deep Learning para classificação de imagens.
      * **Agente 2 (Texto):** O serviço `text-generator` atua como um agente de IA textual, processando o tipo de material e gerando instruções baseadas em uma base de conhecimento estruturada, simulando uma IA baseada em regras para geração de conteúdo informativo.
  * **Pelo menos um modelo local e containerizado (Docker):**
      * Ambos os agentes (`image-classifier` e `text-generator`) são totalmente **containerizados com Docker**, rodando localmente, o que excede o requisito.

### 2\. Comunicação (10 pts)

  * **Implementação de comunicação entre IAs utilizando MCP ou A2A:**
      * Utilizamos a comunicação **A2A (Agent-to-Agent)** via **APIs RESTful (HTTP)**. O `api-gateway` faz chamadas HTTP para os serviços `image-classifier` e `text-generator` para orquestrar o fluxo de dados.
  * **As IAs devem funcionar como microserviços:**
      * Cada agente (`image-classifier`, `text-generator`) e o `api-gateway` são implementados como **microsserviços independentes**. Cada um tem seu próprio `Dockerfile`, suas próprias dependências e roda em seu próprio container isolado, com APIs dedicadas.
  * **Implementação de uma API na solução:**
      * O serviço `api-gateway` expõe a **API principal** (`/process_trash_image`) para interação externa. Os outros serviços (`image-classifier` com `/classify` e `text-generator` com `/get_discard_instructions`) expõem APIs internas para comunicação entre os microsserviços.

### 3\. Controle de Versão

  * **Utilização obrigatória do GitHub para desenvolvimento:**
      * Todo o código-fonte, configurações e documentação do projeto estão hospedados neste repositório GitHub.
      * A contribuição de todos os membros do grupo é registrada através dos commits e do histórico do repositório.

### 4\. Documentação Arquitetônica (15 pts)
  * **Visão inicial pré-modelagem de ameaças:**
      * **Diagrama de Componentes:** (Ex: Boxes para Cliente, API Gateway, Image Classifier, Text Generator com setas indicando HTTP).
      * **Diagrama de Implantação:** (Ex: Containers Docker para cada serviço em um único host).
      * **Fluxo de Dados:** Usuário -\> API Gateway -\> Image Classifier -\> API Gateway -\> Text Generator -\> API Gateway -\> Usuário.
      * **Ativos:** Imagens de lixo, modelos de IA, instruções de descarte.
      * **Ameaças Iniciais:** Acesso não autorizado às APIs, injeção de dados maliciosos na imagem/entrada de texto, negação de serviço.
      * **As rotas dos microsserviços não possuíam proteção CORS (Cross-Origin Resource Sharing).
      * **Não havia autenticação JWT (JSON Web Token) implementada para controle de acesso.
  * **Visão final após implementação das medidas de mitigação:**
      * **Medidas de Mitigação Implementadas:**
          * **Validação de Entrada:** As APIs validam o tipo e formato dos dados recebidos para prevenir ataques de injeção ou dados inválidos.
          * **Tratamento de Erros:** Respostas de erro claras, mas sem expor detalhes internos sensíveis do servidor.
          * **Isolamento de Containers:** O Docker fornece isolamento inerente entre os microsserviços, limitando o impacto de uma eventual falha em um único serviço.
          * **Princípio do Privilégio Mínimo:** Os containers rodam com as permissões essenciais para suas funções.
          * **Configuração de Rede Interna do Docker Compose:** Os serviços se comunicam por nomes de serviço (ex: `http://image-classifier:5000`), o que é mais seguro do que expor todas as portas diretamente.
          * **Implementação de CORS para restringir e controlar o acesso às APIs apenas por origens autorizadas.
          * **Inclusão de autenticação JWT, exigindo token válido para acessar rotas protegidas, aumentando a segurança e o controle de acesso ao sistema.
      * **Diagramas Atualizados:** Refletindo as medidas de segurança, como validação de dados nas entradas das APIs.

-----

## 🚀 Como Usar o Projeto

Siga estes passos para configurar e executar o sistema em sua máquina local.

### Pré-requisitos

  * **Docker Desktop** (ou Docker Engine e Docker Compose) instalado.
      * [Instruções de instalação do Docker](https://docs.docker.com/get-docker/)

### 1\. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio-sd.git
cd seu-repositorio-sd
```

*(Lembre-se de substituir `seu-usuario/seu-repositorio-sd.git` pelo caminho real do seu repositório)*

### 2\. Estrutura de Pastas

Certifique-se de que a estrutura do seu projeto esteja organizada da seguinte forma:

```
.
├── api-gateway/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── image-classifier/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── text-generator/
│   ├── app.py
│   ├── discard_rules.json
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
└── test_image.jpg         # Exemplo de imagem para teste (pode ser a sua 'aa.jpg')
```

### 3\. Construir e Iniciar os Serviços Docker

Navegue até a raiz do diretório do projeto (onde está o `docker-compose.yml`) e execute o seguinte comando para construir as imagens e iniciar os containers:

```bash
docker compose up --build -d
```

  * `--build`: Garante que as imagens Docker sejam construídas (ou reconstruídas) antes de iniciar.
  * `-d`: Inicia os containers em segundo plano (detached mode).

Aguarde alguns minutos. O Docker fará o download das imagens base, instalará as dependências e o `image-classifier` baixará o modelo do Hugging Face.

### 4\. Verificar o Status dos Serviços

Você pode verificar se todos os serviços estão rodando corretamente com:

```bash
docker compose ps
```

Todos os serviços (`api-gateway`, `image-classifier`, `text-generator`) devem ter o status `Up`.

### 5\. Testar a API Principal

Com os serviços em execução, você pode enviar uma imagem para o `api-gateway` para obter a classificação e as instruções de descarte. Certifique-se de ter uma imagem para teste no diretório raiz do projeto (ex: `test_image.jpg` ou `aa.jpg`).

```bash
curl -X POST -F "file=@test_image.jpg" http://localhost:8000/process_trash_image
```

### Exemplo de Saída (JSON):

```json
{
  "discard_instructions": "Latas de alumínio (refrigerante, cerveja) e latas de aço (molho de tomate, milho). Lave para remover resíduos. Amasse as latas para economizar espaço. Aerossóis vazios também podem ser recicláveis, mas verifique as normas locais.",
  "discard_tips": "Não é necessário remover os rótulos de papel. Não descarte latas de tinta ou produtos químicos sem esvaziá-las e verificar as instruções de descarte especial.",
  "image_classification": "metal"
}
```

### 6\. Parar os Serviços Docker

Quando terminar de usar o sistema, você pode derrubar todos os containers e remover as redes criadas pelo Docker Compose com:

```bash
docker compose down
```

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
