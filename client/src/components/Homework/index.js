import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Table from 'react-bootstrap/Table';

import AssignmentTable from './AssignmentTable';
import { getCookies, isLoggedIn } from '../../helpers/setAuthToken';

const Homework = () => {
  let navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn()) {
      navigate('/login');
    }
  });

  return (
    <Container className="mt-5">
      <Button href="/homework/new" className="mb-3 text-white">
        New Assignment
      </Button>
      <AssignmentTable />
    </Container>
  );
}

export default Homework;

