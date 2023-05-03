import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';

import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { Link as RouterLink } from 'react-router-dom';

import { setAuthToken } from '../../helpers/setAuthToken';

const SignUp = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');
  const history = useHistory();

  const onSubmit = async (e) => {
    e.preventDefault();
    if (password !== password2) {
      alert('Your passwords do not match');
    } else {
      const formData = { name, email, password };

      try {
        const res = await axios.post('/user', formData);
        setAuthToken(res.data.token);
        history.push('/homework');
      } catch (err) {
        const errorMessage = err.response.data.message;
        alert(errorMessage);
      }
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Sign Up
      </Typography>
      <Typography variant="h6" gutterBottom>
        <i className="fas fa-user"></i> Create Your Account
      </Typography>

      <form onSubmit={onSubmit}>
        <Box marginBottom={2}>
          <TextField
            label="Name"
            type="text"
            variant="outlined"
            fullWidth
            placeholder="James"
            name="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </Box>
        <Box marginBottom={2}>
          <TextField
            label="Email Address"
            type="email"
            variant="outlined"
            fullWidth
            placeholder="name@email.com"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </Box>
        <Box marginBottom={2}>
          <TextField
            label="Password"
            type="password"
            variant="outlined"
            fullWidth
            placeholder="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            minLength="6"
            required
          />
        </Box>
        <Box marginBottom={2}>
          <TextField
            label="Confirm Password"
            type="password"
            variant="outlined"
            fullWidth
            placeholder="password"
            name="password2"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
            minLength="6"
            required
          />
        </Box>
        <Box marginBottom={2}>
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Sign Up
          </Button>
        </Box>
        <Typography>
          Already have an account? &nbsp;
          <Button component={RouterLink} to="/login" color="primary">
            Login
          </Button>
        </Typography>
      </form>
    </Box>
  );
};

export default SignUp;
