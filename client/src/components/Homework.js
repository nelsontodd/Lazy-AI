import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import Container from 'react-bootstrap/Container';
import FileUploader from './FileUploader';

import { isLoggedIn } from '../helpers/setAuthToken';

const Homework = () => {
  let navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn()) {
      navigate('/login');
    }
  });

  return (
    <Container className="mt-5">
      <FileUploader />
    </Container>
  );
}

export default Homework;

