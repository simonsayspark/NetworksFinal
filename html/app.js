// Explicitly set the API base URL with port 5000
const baseURL = "http://100.75.3.75:5000";

// Define API endpoints
const sendMessageURL = `${baseURL}/send`;
const fetchMessagesURL = `${baseURL}/messages`;

// Fetch messages from the API and display them
async function fetchMessages() {
  try {
    const response = await fetch(fetchMessagesURL);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const messages = await response.json();
    displayMessages(messages);
  } catch (error) {
    console.error('Error fetching messages:', error);
  }
}

// Display messages in the message list
function displayMessages(messages) {
  const messageList = document.getElementById('message-list');
  messageList.innerHTML = ''; // Clear existing messages
  messages.forEach((msg) => {
    const listItem = document.createElement('li');
    listItem.textContent = `${msg.sender}: ${msg.message}`;
    messageList.appendChild(listItem);
  });
}

// Send a new message
async function sendMessage() {
  const sender = document.getElementById('sender').value.trim();
  const message = document.getElementById('message').value.trim();

  if (!sender || !message) {
    alert('Both sender and message are required!');
    return;
  }

  try {
    const response = await fetch(sendMessageURL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sender, message }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Clear input fields
    document.getElementById('sender').value = '';
    document.getElementById('message').value = '';

    // Fetch updated messages
    fetchMessages();
  } catch (error) {
    console.error('Error sending message:', error);
  }
}

// Fetch messages when the page loads
document.addEventListener('DOMContentLoaded', fetchMessages);
