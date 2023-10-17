import React from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

import logo from '../img/icon-128.png';


const Navigation = () => {
  return (
    <Navbar expand="md">
      <Container>
        <Navbar.Brand style={{fontSize:'2rem'}}>
          <img src={logo} alt="Logo"/>
          &nbsp;
          HomeworkHero
        </Navbar.Brand>
        <Navbar.Collapse className="justify-content-end">
          <Nav.Link href="/faq">FAQ</Nav.Link>
          &nbsp;
          &nbsp;
          &nbsp;
          <Nav.Link href="/blog">Blog</Nav.Link>
          &nbsp;
          &nbsp;
          &nbsp;
          <Button href="/homework" className="text-white">
            <b>Get Solutions</b>
          </Button>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  )
}

export default Navigation;
