import React, { useState } from 'react';
import axios from 'axios';

const FileUploader = () => {
  const [file, setFile] = useState(null);

  const onFileChange = (e) => {
    setFile(e.target.files[0]);
  }

  const onFileUpload = async (e) => {
    e.preventDefault();
    const formDate = {file: file, name: file.name};
    try {
      console.log('Create a backend route');
    } catch (err) {
      const errorMessage = err.response.data.message;
      alert(errorMessage);
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
      return (
        <div>
          <br />
          <h4>Choose before Pressing the Upload button</h4>
        </div>
      );
    }
  }

  return (
    <div>
      <h3>Upload file using React!</h3>
      <div>
        <input type="file" onChange={(e) => onFileChange(e)} />
        <button onClick={(e) => onFileUpload(e)}>
          Upload!
        </button>
      </div>
      { fileData() }
    </div>
  );
}

export default FileUploader;
