import React, { useState } from 'react';
import Button from '@mui/material/Button';
import Input from '@mui/material/Input';
import Typography from '@mui/material/Typography';
import axios from 'axios';
import { Document, Page } from 'react-pdf';
import Grid from '@mui/material/Grid';


const FileUploader = () => {
  const [file, setFile] = useState(null);
  const [numPages, setNumPages] = useState(null);

  function onDocumentLoadSuccess(document) {
    const { numPages } = document;
    setNumPages(numPages);
  }

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
    <Grid container>
      <Grid item xs={6}>
        {/* Left half of the container */}
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
      </Grid>
      <Grid item xs={6}>
        {/* Right half of the container */}
        <div>
          <Document
            file={file}
          >
            {Array.from(
              new Array(1),
              (el, index) => (
                <Page key={`page_${index + 1}`} pageNumber={index + 1} />
              ),
            )}
          </Document>
        </div>
      </Grid>
    </Grid>
  );
}

export default FileUploader;
