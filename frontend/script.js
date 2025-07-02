async function sendImage() {
    const input = document.getElementById('imageInput');
    const file = input.files[0];
    
    if (!file) return;
    
    const reader = new FileReader();
    
    reader.onload = async function(event) {
        const imageUrl = event.target.result;
        appendMessage('user', `<img src="${imageUrl}">`);

        console.log(imageUrl)

        const formData = new FormData();
        formData.append('file', file);

        fetch('http://localhost:8000/process_trash_image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('api', data?.discard_instructions || 'Não foi possível identificar o material.');
            console.log(data);
        });

        appendMessage('api', result);
    };
    reader.readAsDataURL(file);
    input.value = '';
}

function appendMessage(sender, content) {
    const chat = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(sender === 'user' ? 'user-message' : 'api-message');
    messageDiv.innerHTML = content;
    chat.appendChild(messageDiv);
    chat.scrollTop = chat.scrollHeight;
}