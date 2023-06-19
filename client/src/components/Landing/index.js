import React from 'react';
import Navigation from './Navigation';
import FirstLandingTile from './FirstLandingTile';
import SecondLandingTile from './SecondLandingTile';
import ThirdLandingTile from './ThirdLandingTile';


const Landing = () => {
  return (
    <>
      <Navigation />
      <FirstLandingTile />
      <SecondLandingTile />
      <ThirdLandingTile />
    </>
  )
}

export default Landing;

