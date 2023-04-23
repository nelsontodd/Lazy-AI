import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';

import Container from '@mui/material/Container';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import { Link as RouterLink } from 'react-router-dom';

import { setAuthToken } from '../../helpers/setAuthToken';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const history = useHistory();

  const onSubmit = async (e) => {
    e.preventDefault();
    const formData = { email, password };
    try {
      const res = await axios.post('/login', formData);
      setAuthToken(res.data.token);
      history.push('/homework');
    } catch (err) {
      const errorMessage = err.response.data.message;
      alert(errorMessage);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Login
      </Typography>
      <Typography variant="h6" gutterBottom>
        <i className="fas fa-user"></i> Sign Into Your Account
      </Typography>

      <form onSubmit={onSubmit}>
        <Box marginBottom={2}>
          <TextField
            label="Email address"
            type="email"
            variant="outlined"
            fullWidth
            placeholder="name@email.com"
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
          <Button type="submit" variant="contained" color="primary" fullWidth>
            Login
          </Button>
        </Box>
        <Typography>
          Don't have an account? &nbsp;
          <Button component={RouterLink} to="/signup" color="primary">
            Sign Up
          </Button>
        </Typography>
      </form>
    </Container>
  );
};

export default Login;
