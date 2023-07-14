import React, { useState } from 'react';
import { Container, Row, Col, Button, Form } from 'react-bootstrap';
import axios from 'axios';

import RenderPDF from './RenderPDF';


const FileUploader = () => {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

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
      setIsLoading(true);
      const formData = new FormData();
      try {
        formData.append('file', file);
        formData.append('fileName', file.name);
        const headers = {
          headers: {
            'content-type': 'multipart/form-data',
          },
        };
        await axios.post('/homework', formData, headers);
      } catch (err) {
        const errorMessage = err.response.data.message;
        alert(errorMessage);
      }
      setIsLoading(false);
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
                disabled={isLoading}
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
          <RenderPDF file={file}/>
        </Col>
      </Row>
    </Container>
  );
}

export default FileUploader;
