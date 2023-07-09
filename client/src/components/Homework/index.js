import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';

import AssignmentTable from './AssignmentTable';
import { isLoggedIn } from '../../helpers/setAuthToken';

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

