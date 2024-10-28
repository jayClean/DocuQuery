import React, { useState } from 'react';

const DocumentUpload = ({ onUpload }) => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (file) {
      await onUpload(file);
      setFile(null);
    }
  };

  return (
    <div className="upload-container">
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload Document</button>
    </div>
  );
};

export default DocumentUpload;
