import React from 'react';

const ChatMessage = ({ message }) => (
  <div className={`message ${message.sender}`}>
    <p>{message.text}</p>
  </div>
);

export default ChatMessage;
