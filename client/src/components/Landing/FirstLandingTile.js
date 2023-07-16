import React from 'react';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';


const FirstLandingTile = () => {
  return (
    <Container className="pb-5 pt-5">
      <h1>
        <b>
          Homework Solutions
          <span className="text-primary">
            <br/>for $1.
          </span>
        </b>
      </h1>
      <h3 className="text-muted">GPT 4 Solutions Manual For any Subject.</h3>
      <Button href="/homework" className="mt-3 text-white">
        Get Solutions
      </Button>
      <br/>
    </Container>
  )
}

export default FirstLandingTile;
