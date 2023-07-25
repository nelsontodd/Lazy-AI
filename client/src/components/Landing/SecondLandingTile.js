import React from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';


const SecondLandingTile = () => {
  return (
    <div className="gradient-background-top">
      <Container className="pt-8 pb-8 text-center">
        <h2>
          Your own personal tutor <br/> even at 3 in the morning
        </h2>
        <h3 className="pt-3 text-muted">
          Finish assignments with ease: whatever and whenever.
        </h3>
        <Button
          href="/homework"
          className="mt-3 text-white"
          variant="secondary"
        >
          Get Solutions
        </Button>
      </Container>
    </div>
  )
}

export default SecondLandingTile;
