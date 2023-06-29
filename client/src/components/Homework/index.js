import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Table from 'react-bootstrap/Table';



import { getCookies, isLoggedIn } from '../../helpers/setAuthToken';

const Homework = () => {
  let navigate = useNavigate();
  const [assignments, setAssignments] = useState([]);

  useEffect(() => {
    if (!isLoggedIn()) {
      navigate('/login');
    }
  });

  useEffect(() => {
    getAssignments()
  }, []);

  const getAssignments = async () => {
    const token = getCookies().token;
    const headers = {
      headers: {
        'x-auth-token': token
      },
    };
    const res = await axios.get('/homework', headers);
    console.log(JSON.stringify(res.data));
    setAssignments(res.data.assignments);
  }

  const renderAssignments = () => {
    if (assignments == null) {
      return null;
    } else {
      return (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Assignment Name</th>
            </tr>
          </thead>
          <tbody>
            {assignments.map((assignment, index) => (
              <tr key={index}>
                <td>{assignment.name}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      )
    }
  }

  return (
    <Container className="mt-5">
      <Button href="/homework/new" className="mb-3 text-white">
        New Assignment
      </Button>
      { renderAssignments() }
    </Container>
  );
}

export default Homework;

