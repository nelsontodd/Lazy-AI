import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';

import Container from "@mui/material/Container";
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
      const formData = {name, email, password};

      try {
        const res = await axios.post('/user', formData);
        setAuthToken(res.data.token);
        history.push('/homework');
      } catch (err) {
        const errorMessage = err.response.data.message;
        alert(errorMessage);
      }
    }
  }

  return (
    <Container>
      <h1>Sign Up</h1>
      <p className="lead">
        <i className="fas fa-user"></i> Create Your Account
      </p>

      <form onSubmit={onSubmit}>
        <label>Name</label>
        <input
          type="text"
          className="u-full-width"
          placeholder="James"
          name="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <label>Email Address</label>
        <input
          type="email"
          className="u-full-width"
          placeholder="name@email.com"
          name="email"
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

        <label>Confirm Password</label>
        <input
          type="password"
          className="u-full-width"
          placeholder="password"
          name="password2"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
          minLength="6"
          required
        />

        <input
          className="button button-primary"
          type="submit"
          value="Sign Up"
        />

        <p>
          Already have an account? &nbsp;
          <a className="button" href="/login">
            Login
          </a>
        </p>
      </form>

    </Container>
  );
}

export default SignUp;
