// 处理与Kimi AI的对话
const chatBox = document.getElementById('chatBox');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');

// 发送消息函数
async function sendMessage() {
  const message = chatInput.value.trim();
  if (!message) return;

  // 添加用户消息到聊天框
  addMessage(message, 'user');
  
  // 清空输入框
  chatInput.value = '';

  try {
    // 调用Kimi API获取AI回复
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    // 添加AI回复到聊天框
    addMessage(data.reply, 'ai');
  } catch (error) {
    console.error('Error:', error);
    addMessage('抱歉，发生错误无法获取回复。', 'ai');
  }
}

// 添加消息到聊天框
function addMessage(text, sender) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `mb-4 p-3 rounded-md ${sender === 'user' ? 'bg-primary text-white ml-auto' : 'bg-gray-200 text-gray-800'}`;
  messageDiv.style.maxWidth = '70%';
  messageDiv.textContent = text;
  chatBox.appendChild(messageDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// 事件监听
sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', function(e) {
  if (e.key === 'Enter') {
    sendMessage();
  }
});

// 初始化时自动聚焦输入框
window.addEventListener('load', () => {
  chatInput.focus();
});