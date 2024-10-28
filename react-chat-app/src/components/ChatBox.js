import React, { useState } from 'react';
import ChatMessage from './ChatMessage';
import DocumentUpload from './DocumentUpload';

const ChatBox = ({ onQuery, onUpload }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleQuerySubmit = async () => {
    try {
      const response = await onQuery(input);
  
      // Check if response and response.content are defined
      const botMessage = response && response.content ? response.content : "No response from server";
  
      // Update messages state
      setMessages([...messages, { text: input, sender: 'user' }, { text: botMessage, sender: 'bot' }]);
    } catch (error) {
      console.error("Error handling query:", error);
      setMessages([...messages, { text: input, sender: 'user' }, { text: "Error processing your query.", sender: 'bot' }]);
    } finally {
      setInput('');
    }
  };
  

  return (
    <div className="chat-box">
      <DocumentUpload onUpload={onUpload} />
      <div className="messages">
        {messages.map((msg, index) => (
          <ChatMessage key={index} message={msg} />
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your question..."
        />
        <button onClick={handleQuerySubmit}>Send</button>
      </div>
    </div>
  );
};

export default ChatBox;
