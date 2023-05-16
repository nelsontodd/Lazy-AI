import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import Container from '@mui/material/Container';
import FileUploader from 'components/utilities/FileUploader';

import { isLoggedIn } from 'helpers/setAuthToken';

const Homework = () => {
  let navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn()) {
      navigate('/sign-in');
    }
  });

  return (
    <Container>
      <FileUploader />
    </Container>
  );
}

export default Homework;
