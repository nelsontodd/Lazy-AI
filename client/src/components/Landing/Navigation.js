import React from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';

import logo from '../../logoipsum-298.svg';


const Navigation = () => {
  return (
    <Navbar expand="md">
      <Container>
        <Navbar.Brand><img src={logo} alt="Logo"/></Navbar.Brand>
        <Navbar.Collapse className="justify-content-end">
          <Button href="/FAQ" className="text-white" variant="secondary">
            <b>FAQ</b>
          </Button>
          <Button href="/homework" className="text-white">
            <b>Get Solutions</b>
          </Button>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  )
}

export default Navigation;
