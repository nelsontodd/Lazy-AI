import React from 'react';
import Button from 'react-bootstrap/Button';
import { Container, Row, Col } from 'react-bootstrap';



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
        <Row>
            <Col md={6}>
            <img src="/test_input.png" alt="Example Input" className="img-fluid" style={{height:'400px', width: 'auto'}}/>
            </Col>
            <Col md={6}>
            <img src="/test_output.png" alt="Example Output" className="img-fluid" style={{height:'400px', width: 'auto'}}/>
            </Col>
        </Row>
      </Container>
    </div>
  )
}

export default SecondLandingTile;
