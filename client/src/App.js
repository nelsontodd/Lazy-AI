import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import './App.css';

import FAQ from './components/FAQ';
import Blog from './components/Blog';
import BridgingTheEducationGap from './components/Blog/BridgingTheEducationGap';
import FromHallowedHalls from './components/Blog/FromHallowedHalls';
import RescuingStudents from './components/Blog/RescuingStudents';
import TheFutureOfHomeworkAssistance from './components/Blog/TheFutureOfHomeworkAssistance';
import Unapologetically from './components/Blog/Unapologetically';
import WhyAutomatedHomework from './components/Blog/WhyAutomatedHomework';
import Homework from './components/Homework';
import Landing from './components/Landing';
import Navigation from './components/Navigation';


axios.defaults.baseURL = 'https://homeworkhero.io';
axios.defaults.withCredentials = true;

function App() {

  return (
    <div className="App">
      <Navigation />
      <Router>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/blog" element={<Blog />} />
          <Route path="/blog/bridging-the-education-gap" element={<BridgingTheEducationGap />} />
          <Route path="/blog/from-hallowed-halls" element={<FromHallowedHalls />} />
          <Route path="/blog/rescuing-students" element={<RescuingStudents />} />
          <Route path="/blog/the-future-of-homework-assistance" element={<TheFutureOfHomeworkAssistance />} />
          <Route path="/blog/unapologetically" element={<Unapologetically />} />
          <Route path="/blog/why-automated-homework" element={<WhyAutomatedHomework />} />
          <Route path="/homework" element={<Homework />} />
          <Route path="/faq" element={<FAQ />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
