import React from 'react';
import Container from 'react-bootstrap/Container';
import { CreditCard, PaymentForm } from 'react-square-web-payments-sdk';
import axios from 'axios';


function Payments() {
  return (
    <Container className="mt-5">
      <PaymentForm
        applicationId="sandbox-sq0idb-VjaXQsDt014XTRq4IY14aw"
        cardTokenizeResponseReceived={ async (token, verifiedBuyer) => {
          console.log('token:', token);
          console.log('verifiedBuyer:', verifiedBuyer);
          const formData = new FormData();
          formData.append('sourceId', token.token);
          const headers = {
            headers: {
              'content-type': 'application/json',
            },
          };
          const res = await axios.post('/payment', formData, headers);
          console.log(JSON.stringify(res));
        }}
        locationId='XXXXXXXXXX'
      >
        <CreditCard/>
      </PaymentForm>
    </Container>
  )
}

export default Payments
