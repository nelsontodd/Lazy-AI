import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';

import Container from "@mui/material/Container";
import { setAuthToken } from '../../helpers/setAuthToken';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const history = useHistory();

  const onSubmit = async (e) => {
    e.preventDefault();
    const formData = {email, password};
    try {
      const res = await axios.post('/login', formData);
      setAuthToken(res.data.token);
      history.push('/homework');
    } catch (err) {
      const errorMessage = err.response.data.message;
      alert(errorMessage);
    }
  }

  return (
    <Container>
      <h1>Login</h1>
      <p className="lead">
        <i className="fas fa-user"></i> Sign Into Your Account
      </p>

      <form onSubmit={onSubmit}>
        <label>Email address</label>
        <input
          type="email"
          className="u-full-width"
          placeholder="name@email.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label>Password</label>
        <input
          type="password"
          className="u-full-width"
          placeholder="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          minLength="6"
          required
        />

        <input className="button button-primary" type="submit" value="Login" />
        <p>
          Don't have an account? &nbsp;
          <a className="button" href="/signup">
            Sign Up
          </a>
        </p>
      </form>

    </Container>
  );
}

export default Login;
