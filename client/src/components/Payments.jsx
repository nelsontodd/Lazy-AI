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
          try {
            const formData = new FormData();
            formData.append('sourceId', token.token);
            const headers = {
              headers: {
                'content-type': 'application/json',
              },
            };
            await axios.post('/payment', formData, headers);
          } catch (err) {
            const errorMessage = err.response.data.message;
            alert(errorMessage);
          }
        }}
        locationId='XXXXXXXXXX'
      >
        <CreditCard/>
      </PaymentForm>
    </Container>
  )
}

export default Payments
