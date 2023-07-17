import React, { useState } from 'react';
import { Container, Row, Col, Form } from 'react-bootstrap';
import { CreditCard, PaymentForm } from 'react-square-web-payments-sdk';
import axios from 'axios';
import { saveAs } from 'file-saver';

import RenderPDF from './RenderPDF';


const FileUploader = () => {
  const [file, setFile] = useState(null);
  const [processingSolution, setProcessingSolution] = useState(false);

  const onFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile.size > 5242880) {
      alert('The file you selected is too large. Max size 5MB.');
    } else{
      setFile(selectedFile);
    }
  }

  const onSubmit = async (token, verifiedBuyer) => {
    if (file) {
      const formData = new FormData();
      try {
        formData.append('file', file);
        formData.append('fileName', file.name);
        formData.append('sourceId', token.token);
        setProcessingSolution(true);
        const headers = {
          responseType: 'blob',
          headers: {
            'content-type': 'multipart/form-data',
          },
        };
        const res = await axios.post('/homework', formData, headers);
        const blob = new Blob([res.data], { type: 'application/pdf' });
        saveAs(blob, 'solutions.pdf');
        setProcessingSolution(false);
      } catch (err) {
        const errorMessage = err.response.data.message;
        alert(errorMessage);
      }
    } else {
      alert('No file selected.');
    }
  }

  const headerText = () => {
    if (processingSolution) {
      return "Processing homework...."
    } else {
      return "Upload your homework."
    }
  }

  return (
    <Container>
      <Row>
        <Col xs={6}>
          <div>
            <h5>{headerText()}</h5>
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
              <h6>Get solutions for $1</h6>
              <PaymentForm
                applicationId="sandbox-sq0idb-VjaXQsDt014XTRq4IY14aw"
                cardTokenizeResponseReceived={
                  (token, verifiedBuyer) => onSubmit(token, verifiedBuyer)
                }
                locationId='XXXXXXXXXX'
              >
                <CreditCard/>
              </PaymentForm>
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
