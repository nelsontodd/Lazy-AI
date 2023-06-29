import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';
// import './App.css';

import Login from './components/auth/Login';
import SignUp from './components/auth/SignUp';
import Homework from './components/Homework';
import NewHomework from './components/Homework/NewHomework';
import Landing from './components/Landing';


axios.defaults.baseURL = 'http://127.0.0.1:5000';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/homework" element={<Homework />} />
          <Route path="/homework/new" element={<NewHomework />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
