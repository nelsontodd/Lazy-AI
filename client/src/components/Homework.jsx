import React from 'react';
import { useHistory } from 'react-router-dom';

import Container from '@mui/material/Container';
import FileUploader from './utilities/FileUploader';

import { isLoggedIn } from '../helpers/setAuthToken';

const Homework = () => {
  const history = useHistory();

  if (!isLoggedIn()) {
    history.push('/login')
    return null;
  } else {
    return (
      <Container maxWidth="md">
        <FileUploader />
      </Container>
    );
  }
}

export default Homework;
