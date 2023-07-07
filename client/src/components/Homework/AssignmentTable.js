import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { saveAs } from 'file-saver';

import Button from 'react-bootstrap/Button';
import Table from 'react-bootstrap/Table';

import { getCookies } from '../../helpers/setAuthToken';

const AssignmentTable = () => {
  const [assignments, setAssignments] = useState([]);

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
    setAssignments(res.data.assignments);
  }

  const handleButtonClick = async (e, index) => {
    e.preventDefault();
    try {
      const assignmentName = assignments[index].name;
      const formData = { assignmentName }
      const token = getCookies().token;
      const headers = {
        responseType: 'blob',
        headers: {
          'x-auth-token': token
        },
      };
      const res = await axios.post('/homework/solution', formData, headers);
      const blob = new Blob([res.data], { type: 'application/pdf' });
      saveAs(blob);
    } catch (err) {
      const errorMessage = err.response.data.message;
      alert(JSON.stringify(errorMessage));
    }
  }

  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>Assignment Name</th>
          <th>Assignment Solution</th>
        </tr>
      </thead>
      <tbody>
        {assignments.map((assignment, index) => (
          <tr key={index}>
            <td>{assignment.name}</td>
            <td>
              <Button
                className='text-white'
                onClick={(e) => handleButtonClick(e, index)}>
                Get Solution
              </Button>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  )
}

export default AssignmentTable;
