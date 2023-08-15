import React from 'react';

import Container from 'react-bootstrap/Container';
import FileUploader from './FileUploader';

const Homework = () => {

  return (
    <>
      <Container className="mt-5">
        <FileUploader />
      </Container>
    </>
  );
}

export default Homework;

