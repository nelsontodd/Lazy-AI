import React from 'react';

import Container from 'react-bootstrap/Container';

import Examples from './Examples';

const FAQ = () => {

  return (
    <Container className="mt-5 mb-5">
      <h2 className="mb-5">Frequently asked questions.</h2>
      <h3>How does it work?</h3>
      <p>You upload a file with your assignment, pay us $1, wait a couple
        minutes, and then you get your formatted homework answers. We use LLMs
        under the hood to understand your assignment and generate reasonable
        answers for these problems.</p>

      <h3 className="mt-3">What file types are supported?</h3>
      <p>PDF, JPG, and PNG.</p>

      <h3 className="mt-3">How much does it cost?</h3>
      <p>Solutions costs $1, regardless of your assignment.</p>

      <h3 className="mt-3">What subjects can I use this for?</h3>
      <p>All subjects. HomeworkHero uses LLMs underneath the hood, so it will be able to
        assist you an any assignment that you have.</p>

      <h3 className="mt-3">Can I use this for exams?</h3>
      <p>Yes, HomeworkHero works well for exams.</p>

      <h3 className="mt-3">Why type of assignments does this work for?</h3>
      <p>HomeworkHero can be used for homework assignments, study guide review
        questions, and exams.</p>

      <h3 className="mt-3">Why do you need my name?</h3>
      <p>HomeworkHero uses your name by placing it at the top of the answer
        key. This is to save you the trouble of forgetting to add your name to
        the assignment. Providing your name is completely optional.</p>

      <h3 className="mt-3">What is the title for?</h3>
      <p>HomeworkHero uses the title to title your answers document. This is to
        help you with formatting.</p>

      <h3 className="mt-3">What do the outputs look like?</h3>
      <p>On the left is a randomly chosen page from an old calculus textbook. On the right are solutions we would generate to some of the problems on that page. Open each image in a new tab to get a better idea.</p>
      <Examples />

      <h3 className="mt-3">How long is the wait?</h3>
      <p>Less than 5 minutes. HomeworkHero usually takes about a couple of
        minutes to understand your assignments and create answers..</p>

    </Container>
  );
}

export default FAQ;

