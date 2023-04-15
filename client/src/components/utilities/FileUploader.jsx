import React, { useState } from 'react';

const FileUploader = () => {
  const [file, setFile] = useState(null);

  const onFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile.size > 5242880) {
      alert('The file you selected is too large. Max size 5MB.');
    } else{
      setFile(selectedFile);
    }
  }

  const onFileUpload = async (e) => {
    e.preventDefault();
    if (file) {
      const formData = {file: file, name: file.name};
      try {
        console.log('Create a backend route');
      } catch (err) {
        const errorMessage = err.response.data.message;
        alert(errorMessage);
      }
    } else {
      alert('No file selected.');
    }
  }

  const fileData = () => {
    if (file) {
      return (
        <div>
          <h2>File Details:</h2>
          <p>File Name: { file.name }</p>
          <p>File Type: { file.type }</p>
          <p>
            Last Modified:{ " " }
            { file.lastModifiedDate.toDateString() }
          </p>
        </div>
      );
    } else {
      return null;
    }
  }

  return (
    <div>
      <h3>Upload your homework.</h3>
      <div>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => onFileChange(e)}
        />
        <p>Select a file smaller than 5MB before uploading</p>
        <button onClick={(e) => onFileUpload(e)}>Upload!</button>
      </div>
      { fileData() }
    </div>
  );
}

export default FileUploader;
