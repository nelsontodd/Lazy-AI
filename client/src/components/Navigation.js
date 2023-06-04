import React from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';

import logo from '../logoipsum-298.svg';


const Navigation = () => {
  return (
    <Navbar expand="md">
      <Container>
        <Navbar.Brand><img src={logo} alt="Logo"/></Navbar.Brand>
        <Navbar.Collapse className="justify-content-end">
          <Button href="/login" className="text-white">
            <b>Sign In</b>
          </Button>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  )
}

export default Navigation;
