const widget = document.getElementById('geeko-widget');
const drop = document.getElementById('geeko-drop');
const closeChat = document.getElementById('close-chat');
const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatMessages = document.getElementById('chat-messages');

// Переключение состояний
drop.addEventListener('click', () => {
    widget.classList.remove('collapsed');
    widget.classList.add('expanded');
});

closeChat.addEventListener('click', () => {
    widget.classList.remove('expanded');
    widget.classList.add('collapsed');
});

// Функция добавления сообщения в чат
function addMessage(text, sender, sources = []) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.innerText = text;

    if (sources.length > 0) {
        const sourceSpan = document.createElement('span');
        sourceSpan.classList.add('sources');
        sourceSpan.innerText = `Источник: ${sources.join(', ')}`;
        msgDiv.appendChild(sourceSpan);
    }

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Отправка сообщения
async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, 'user');
    userInput.value = '';

    // Индикатор загрузки
    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('message', 'bot');
    loadingDiv.innerText = 'Думаю...';
    chatMessages.appendChild(loadingDiv);

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        chatMessages.removeChild(loadingDiv);
        addMessage(data.answer, 'bot', data.sources);
    } catch (error) {
        chatMessages.removeChild(loadingDiv);
        addMessage('Ошибка связи с сервером.', 'bot');
        console.error(error);
    }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
