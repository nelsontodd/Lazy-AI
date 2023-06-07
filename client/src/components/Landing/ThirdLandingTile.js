import React from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';


const ThirdLandingTile = () => {
  return (
    <div className="bg-primary">
      <Container className="pt-8 pb-8">
        <h2 className="text-white">
          Start now <br/> and finish now
        </h2>
        <h3 className="pt-3 text-offwhite">Get your assignments done and out of the way with the help of AI</h3>
        <Button
          href="/signup"
          className="mt-3 text-white"
          variant="secondary"
        >
          Sign Up
        </Button>
      </Container>
    </div>
  )
}

export default ThirdLandingTile;
