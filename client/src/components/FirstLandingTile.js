import React from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';

import messages from '../imessages.png';


const FirstLandingTile = () => {
  return (
    <Container className="pb-5 pt-5">
      <h1>
        <b>
          Homework done
          <span className="text-primary">
            <br/>today.
          </span>
        </b>
      </h1>
      <h3 className="text-muted">Get help on your homework and assignments.</h3>
      <Button className="mt-3 text-white"variant="primary">
        Sign Up
      </Button>
      <br/>
    </Container>
  )
}

export default FirstLandingTile;
