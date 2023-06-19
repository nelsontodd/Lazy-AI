import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import axios from "axios";

import { setAuthToken } from "../../helpers/setAuthToken";

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const onSubmit = async (e) => {
    e.preventDefault();
    const formData = { email, password };
    try {
      const res = await axios.post("/login", formData);
      setAuthToken(res.data.token);
      navigate("/homework");
    } catch (err) {
      const errorMessage = err.response.data.message;
      alert(JSON.stringify(errorMessage));
    }
  };

  return (
    <Container>
      <Row>
        <Col md/>
        <Col md={4}>
          <h1>Sign In</h1>
          <Form onSubmit={onSubmit}>
            <Form.Group>
              <Form.Label>Email Address</Form.Label>
              <Form.Control
                type="email"
                placeholder="name@email.com"
                name="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group>
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                minLength="6"
                required
              />
            </Form.Group>

            <Button className="mt-3" variant="primary" type="submit">
              Sign In
            </Button>
          </Form>

          <p>
            Already have an account? &nbsp;
            <a href="/signup">
              Sign Up
            </a>
          </p>
        </Col>
        <Col md/>
      </Row>
    </Container>
  );
}

export default Login;
