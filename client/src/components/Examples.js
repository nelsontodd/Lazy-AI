import React from 'react';
import { Row, Col } from 'react-bootstrap';

import test_input from '../img/test_input.png'
import test_output from '../img/test_output.png'



const Examples = () => {
  return (
    <Row>
      <Col md={6}>
        <img src={test_input} alt="Example Input" className="img-fluid" style={{height:'400px', width: 'auto'}}/>
      </Col>
      <Col md={6}>
        <img src={test_output} alt="Example Output" className="img-fluid" style={{height:'400px', width: 'auto'}}/>
      </Col>
    </Row>
  )
}

export default Examples;
