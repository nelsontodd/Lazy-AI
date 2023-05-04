import React from "react";
import Box from '@mui/material/Box';
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { Link as RouterLink } from "react-router-dom";

import quill from "../img/quill.svg";

const Landing = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Daybook
      </Typography>

      <Typography variant="h6" gutterBottom>
        This is a micro-journaling service to enable you to record and remember
        your life.
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={6}>
          <Button
            component={RouterLink}
            to="/signup"
            variant="contained"
            color="primary"
            fullWidth
          >
            Sign Up
          </Button>
        </Grid>
        <Grid item xs={6}>
          <Button component={RouterLink} to="/login" variant="outlined" fullWidth>
            Login
          </Button>
        </Grid>
      </Grid>

      <hr />

      <Grid container spacing={2}>
        <Grid item md={6}>
          <Typography variant="h5" gutterBottom>
            What is Daybook and why should I use it?
          </Typography>
          <Typography paragraph>
            Daybook is a micro-journaling service to help you record your life
            in a tweet length entries to easily help you form a journaling
            habit.
          </Typography>

          <Typography paragraph>
            By keeping entries short and easy, Daybook enables consistency and
            let's you focus on the most important parts of each day. You can
            then remember the major events and trends in your life.
          </Typography>
        </Grid>
        <Grid item md={6}>
          <img src={quill} className="img-height" alt="quill" />
        </Grid>
      </Grid>
    </Box>
  );
};

export default Landing;
