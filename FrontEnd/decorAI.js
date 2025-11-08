let chatHistory = [];
let currentChatId = 1;

function sendMessage() {
  const input = document.getElementById('userInput');
  const chatArea = document.getElementById('chatArea');
  const message = input.value.trim();
  
  if (message === '') return;
  
  // Add to chat history on first message
  if (chatArea.children.length === 1) {
    addToChatHistory(message);
  }
  
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
      <div class="messageContent">That's a great idea! I'd be happy to help you with designing your space. Let me provide some suggestions based on your space.</div>
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

function addToChatHistory(firstMessage) {
  const chatHistoryDiv = document.getElementById('chatHistory');
  
  // Remove empty state if present
  const emptyState = chatHistoryDiv.querySelector('.emptyState');
  if (emptyState) {
    emptyState.remove();
  }
  
  // Create chat item with truncated message
  const chatItem = document.createElement('div');
  chatItem.className = 'chatItem';
  const truncated = firstMessage.length > 30 ? firstMessage.substring(0, 30) + '...' : firstMessage;
  chatItem.textContent = truncated;
  chatItem.dataset.chatId = currentChatId;
  
  // Store full conversation
  chatHistory.push({
    id: currentChatId,
    title: truncated,
    messages: []
  });
  
  chatItem.onclick = function() {
    loadChat(this.dataset.chatId);
  };
  
  // Add to top of history
  chatHistoryDiv.insertBefore(chatItem, chatHistoryDiv.firstChild);
  currentChatId++;
}

function newChat() {
  const chatArea = document.getElementById('chatArea');
  chatArea.innerHTML = `
    <div class="message aiMessage">
      <div class="avatar">AI</div>
      <div class="messageContent">Hello! I'm DecorAI, your party design assistant. How can I help you transform your space today?</div>
    </div>
  `;
}

function loadChat(id) {
  const chatArea = document.getElementById('chatArea');
  chatArea.innerHTML = `
    <div class="message aiMessage">
      <div class="avatar">DA</div>
      <div class="messageContent">Loading previous conversation...</div>
    </div>
  `;
}