import React, { Fragment } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import axios from 'axios';

import Navbar from './components/layout/Navbar';
import Landing from './components/layout/Landing';
import Login from './components/auth/Login';
import Profile from './components/Profile';
import Register from './components/auth/Register';


// Styles
import './App.css';

axios.defaults.baseURL = 'http://127.0.0.1:5000';

const App = () => (
    <Router>
        <Fragment>
            <Navbar />
            <Route exact path="/" component={Landing}/>
            <section className="container">
                <Switch>
                    <Route exact path="/register" component={Register}/>
                    <Route exact path="/login" component={Login}/>
                    <Route exact path="/profile" component={Profile}/>
                </Switch>
            </section>
        </Fragment>
    </Router>
);

export default App;
