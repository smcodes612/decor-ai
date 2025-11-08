function sendMessage() {
  const input = document.getElementById('userInput');
  const chatArea = document.getElementById('chatArea');
  const message = input.value.trim();
  
  if (message === '') return;
  
  const userMsg = document.createElement('div');
  userMsg.className = 'message userMessage';
  userMsg.innerHTML = `
    <div class="avatar">You</div>
    <div class="messageContent">${message}</div>
  `;
  chatArea.appendChild(userMsg);
  
  input.value = '';
  
  setTimeout(() => {
    const aiMsg = document.createElement('div');
    aiMsg.className = 'message aiMessage';
    aiMsg.innerHTML = `
      <div class="avatar">AI</div>
      <div class="messageContent">That's a great question! I'd be happy to help you with that design idea. Let me provide some suggestions based on current trends and best practices.</div>
    `;
    chatArea.appendChild(aiMsg);
    chatArea.scrollTop = chatArea.scrollHeight;
  }, 800);
  
  chatArea.scrollTop = chatArea.scrollHeight;
}

function handleKeyPress(event) {
  if (event.key === 'Enter') {
    sendMessage();
  }
}

function newChat() {
  const chatArea = document.getElementById('chatArea');
  chatArea.innerHTML = `
    <div class="message aiMessage">
      <div class="avatar">AI</div>
      <div class="messageContent">Hello! I'm DecorAI, your interior design assistant. How can I help you transform your space today?</div>
    </div>
  `;
}

function loadChat(id) {
  const chatArea = document.getElementById('chatArea');
  chatArea.innerHTML = `
    <div class="message aiMessage">
      <div class="avatar">AI</div>
      <div class="messageContent">Loading previous conversation...</div>
    </div>
  `;
}