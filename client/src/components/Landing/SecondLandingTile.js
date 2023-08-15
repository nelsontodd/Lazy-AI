import React from 'react';
import { Container } from 'react-bootstrap';

import Examples from '../Examples';


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
        <Examples />
      </Container>
    </div>
  )
}

export default SecondLandingTile;
