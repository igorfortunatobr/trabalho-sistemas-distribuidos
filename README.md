# ♻️ Sistema Distribuído de Classificação e Descarte de Resíduos

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
