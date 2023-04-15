import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';

import Container from './utilities/Container';
import EntryCard from './utilities/EntryCard';
import FileUploader from './utilities/FileUploader';

import { formatDates, sortEntries } from '../helpers/entries';
import { getCookies, isLoggedIn } from '../helpers/setAuthToken';

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
