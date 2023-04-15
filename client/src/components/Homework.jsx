import React from 'react';
import { useHistory } from 'react-router-dom';

import FileUploader from './utilities/FileUploader';

import { isLoggedIn } from '../helpers/setAuthToken';

const Homework = () => {
  const history = useHistory();

  if (!isLoggedIn()) {
    history.push('/login')
    return null;
  } else {
    return (
      <FileUploader />
    );
  }
}

export default Homework;
