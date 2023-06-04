import React, { useState } from 'react';
import { Container, Row, Col, Button, Form } from 'react-bootstrap';
import axios from 'axios';
import { Document, Page } from 'react-pdf';


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
        await axios.post('/homework', formData, config);
      } catch (err) {
        const errorMessage = err.response.data.message;
        alert(errorMessage);
      }
    } else {
      alert('No file selected.');
    }
  }

  return (
    <Container>
      <Row>
        <Col xs={6}>
          <div>
            <h5>Upload your homework.</h5>
            <div>
              <Form.Group>
                <Form.Control
                  type="file"
                  accept=".pdf"
                  id="fileUploader"
                  onChange={(e) => onFileChange(e)}
                />
              </Form.Group>
              <p>Select a file smaller than 5MB before uploading</p>
              <Button
                className="text-white"
                variant="primary"
                onClick={(e) => onFileUpload(e)}
              >
                Upload!
              </Button>
            </div>
          </div>
        </Col>
        <Col xs={6}>
          <div>
            <Document file={file}>
              {Array.from(new Array(1), (el, index) => (
                <Page key={`page_${index + 1}`} pageNumber={index + 1} />
              ))}
            </Document>
          </div>
        </Col>
      </Row>
    </Container>
  );
}

export default FileUploader;
