import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import './App.css';

import FAQ from './components/FAQ';
import Homework from './components/Homework';
import Landing from './components/Landing';


axios.defaults.baseURL = 'https://homeworkhero.io';
axios.defaults.withCredentials = true;

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/homework" element={<Homework />} />
          <Route path="/faq" element={<FAQ />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
