import React, { useState } from 'react';
import Button from '@mui/material/Button';
import Input from '@mui/material/Input';
import Typography from '@mui/material/Typography';
import axios from 'axios';


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
      const formData = new FormData();
      try {
        formData.append('file', file);
        formData.append('fileName', file.name);
        const config = {
          headers: {
            'content-type': 'multipart/form-data',
          },
        };
        const res = await axios.post('/homework', formData, config);
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
          <Typography variant="h5">File Details:</Typography>
          <Typography>File Name: { file.name }</Typography>
          <Typography>File Type: { file.type }</Typography>
          <Typography>
            Last Modified:{ " " }
            { file.lastModifiedDate.toDateString() }
          </Typography>
        </div>
      );
    } else {
      return null;
    }
  }

  return (
    <div>
      <Typography variant="h5">Upload your homework.</Typography>
      <div>
        <Input
          type="file"
          inputProps={{
            accept: "application/pdf",
            display: 'none'
          }}
          onChange={(e) => onFileChange(e)}
          sx={{ mb: 1 }}
        />
        <Typography variant="body2" color="textSecondary">
          Select a file smaller than 5MB before uploading
        </Typography>
        <Button variant="contained" color="primary" onClick={(e) => onFileUpload(e)}>
          Upload!
        </Button>
      </div>
      { fileData() }
    </div>
  );
}

export default FileUploader;
