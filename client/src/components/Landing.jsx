import React from "react";

import Container from "./utilities/Container";

import quill from "../img/quill.svg"


const Landing = () => {
    return (
        <Container>
            <h1 className="title">Daybook</h1>

            <p className="lead">
                This is a micro-journaling service to enable you to
                record and remember your life.
            </p>

            <div className="row">
                <div className="six columns">
                    <a className="button button-primary u-full-width" href="/signup">
                        Sign Up
                    </a>
                </div>
                <div className="six columns">
                    <a className="button u-full-width" href="/login">
                        Login
                    </a>
                </div>
            </div>

            <hr/>

            <div className="row">
                <div className="six columns">
                    <h5>What is Daybook and why should I use it?</h5>
                    <p>
                        Daybook is a micro-journaling service to help you
                        record your life in a tweet length entries to easily
                        help you form a journaling habit.
                    </p>

                    <p>
                        By keeping entries short and easy, Daybook enables
                        consistency and let's you focus on the most important
                        parts of each day. You can then remember the major
                        events and trends in your life.
                    </p>
                </div>
                <div className="six columns">
                    <img src={quill} className="img-height" alt="quill"/>
                </div>
            </div>
        </Container>
    );
}

export default Landing;
