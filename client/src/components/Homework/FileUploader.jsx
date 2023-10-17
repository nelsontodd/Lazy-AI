import React, { useState } from 'react';
import { Container, Row, Col, Form } from 'react-bootstrap';
import { CreditCard, PaymentForm } from 'react-square-web-payments-sdk';
import axios from 'axios';
import { saveAs } from 'file-saver';

import RenderPDF from './RenderPDF';


const FileUploader = () => {
  const [file, setFile] = useState(null);
  const [hasLatex, setHasLatex] = useState(true);
  const [assignmentType, setAssignmentType] = useState("HOMEWORK");
  const [name, setName] = useState('');
  const [programminglanguage, setProgrammingLanguage] = useState('');
  const [email, setEmail] = useState(null);
  const [processingSolution, setProcessingSolution] = useState(false);
  const [title, setTitle] = useState('');

  const onFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile.size > 5242880) {
      alert('The file you selected is too large. Max size 5MB.');
    } else{
      setFile(selectedFile);
    }
  }

  const handleLatexRadioButton = (e) => {
    setHasLatex(!hasLatex);
  }

  const onSubmit = async (token, verifiedBuyer) => {
    if (file && email) {
      const formData = new FormData();
      try {
        formData.append('file', file);
        formData.append('fileName', file.name);
        formData.append('hasLatex', hasLatex);
        formData.append('assignmentType', assignmentType);
        formData.append('name', name);
        formData.append('programminglanguage', programminglanguage);
        formData.append('email', email);
        formData.append('sourceId', token.token);
        formData.append('title', title);
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
      } catch (err) {
        const errorMessage = err.response.data.message;
        alert(errorMessage);
      }
    } else {
      alert('No file selected.');
    }
    setProcessingSolution(false);
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
      <Form.Group>
        <Row>
          <Col xs={6}>
            <div>
              <h5>{headerText()}</h5>
              <div>
                <Form.Control
                  type="file"
                  accept=".pdf, .jpg, .png, .jpeg"
                  id="fileUploader"
                  onChange={(e) => onFileChange(e)}
                />
                <p>Select a file smaller than 5MB before uploading</p>
                <p className="mt-3">
                  <b>Email Address</b>
                </p>
                <Form.Control
                  type="email"
                  id="email"
                  value={email}
                  placeholder="Your Email"
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
                <p className="mt-3">
                  <b>What name do you want on the solutions? (Optional)</b>
                </p>
                <Form.Control
                  type="text"
                  id="name"
                  value={name}
                  placeholder="Your Name"
                  onChange={(e) => setName(e.target.value)}
                  required
                />
                <p className="mt-3">
                  <b>Title (Optional)</b>
                </p>
                <Form.Control
                  type="text"
                  id="title"
                  value={title}
                  placeholder="Your Assignment Name"
                  onChange={(e) => setTitle(e.target.value)}
                  required
                />
                <p className="mt-3">
                  <b>If this is a programming assignment, input the language below. (Leave blank if not).</b>
                </p>
                <Form.Control
                  type="text"
                  id="programminglanguage"
                  value={programminglanguage}
                  placeholder="Programming Language"
                  onChange={(e) => setProgrammingLanguage(e.target.value)}
                  required
                />
              </div>
            </div>
          </Col>
          <Col xs={6}>
            <p className="mt-3">
              <b>Does your assignment have equations? (Example: Latex, physics,
                chemistry, etc)</b>
            </p>
            <Form.Check
              value={true}
              type="radio"
              aria-label="radio 1"
              label="Yes"
              onChange={handleLatexRadioButton}
              checked={hasLatex === true}
            />
            <Form.Check
              value={false}
              type="radio"
              aria-label="radio 2"
              label="No"
              onChange={handleLatexRadioButton}
              checked={hasLatex === false}
            />
            <p className="mt-3">
              <b>What type of assignment is this?</b>
            </p>
            <Form.Check
              value={"HOMEWORK"}
              type="radio"
              aria-label="radio 1"
              label="Homework Assignment"
              onChange={(e) => setAssignmentType(e.target.value)}
              checked={assignmentType === "HOMEWORK"}
            />
            <Form.Check
              value={"STUDYGUIDE"}
              type="radio"
              aria-label="radio 2"
              label="Study Guide"
              onChange={(e) => setAssignmentType(e.target.value)}
              checked={assignmentType === "STUDYGUIDE"}
            />
            <Form.Check
              value={"EXAM"}
              type="radio"
              aria-label="radio 3"
              label="Exam"
              onChange={(e) => setAssignmentType(e.target.value)}
              checked={assignmentType === "EXAM"}
            />
            <h6 className="mt-3">Get solutions for $1</h6>
            <PaymentForm
              applicationId="sq0idp-Ik5Cdo6-ipbu5bdcDhQYqw"
              cardTokenizeResponseReceived={
                (token, verifiedBuyer) => onSubmit(token, verifiedBuyer)
              }
              locationId='XXXXXXXXXX'
            >
              <CreditCard/>
            </PaymentForm>
          </Col>
        </Row>
      </Form.Group>
      <Row>
        <Col xs={2}/>
        <Col xs={8}>
          <RenderPDF file={file}/>
        </Col>
        <Col xs={2}/>
      </Row>
    </Container>
  );
}

export default FileUploader;
