// src/pages/Chat.js
import React from 'react';
import ChatBox from '../components/ChatBox';
import { uploadDocument } from '../api/documents';
import { queryDocuments } from '../api/query';

const Chat = ({ }) => {
  const handleQuery = async (queryText) => {
    try {
      const data = await queryDocuments(queryText);
      // Handle the data received from the query
      console.log(data);
    } catch (error) {
      console.error("Error querying documents:", error);
      alert("Failed to query documents.");
    }
  };

  const handleUpload = async (file) => {
    try {
      const data = await uploadDocument(file);
      // Handle the upload response
      console.log(data);
    } catch (error) {
      console.error("Error uploading document:", error);
      alert("Failed to upload document.");
    }
  };

  return (
    <div>
      <ChatBox onQuery={handleQuery} onUpload={handleUpload} />
    </div>
  );
};

export default Chat;
