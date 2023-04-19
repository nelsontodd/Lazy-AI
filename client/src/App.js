import React, { Fragment } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import axios from 'axios';

import Landing from './components/Landing';
import Login from './components/auth/Login';
import Entry from './components/Entry';
import Homework from './components/Homework';
import SignUp from './components/auth/SignUp';


// Styles
// import './css/normalize.css';
// import './css/skeleton.css';
// import './css/custom.css'


axios.defaults.baseURL = 'http://127.0.0.1:5000';

const App = () => (
  <Router>
    <Fragment>
      <Route exact path="/" component={Landing}/>
      <section className="container">
        <Switch>
          <Route exact path="/signup" component={SignUp}/>
          <Route exact path="/login" component={Login}/>
          <Route exact path="/entry" component={Entry}/>
          <Route exact path="/homework" component={Homework}/>
        </Switch>
      </section>
    </Fragment>
  </Router>
);

export default App;
