import * as React from "react";
import {Navbar} from "components/navbar/Navbar";

import {makeStyles, createStyles, Grid} from "@material-ui/core";
import {Footer} from "../footer/Footer";

const useStyles = makeStyles((theme) =>
  createStyles({
    root: {
      flexGrow: 1,
      padding: theme.spacing(3),
    },
  })
);

export const Frame: React.FunctionComponent<{children: React.ReactNode}> = ({
  children,
}) => {
  const classes = useStyles();

  return (
    <Grid container data-cy="frame" direction="column" spacing={2}>
      <Grid item>
        <Navbar />
      </Grid>
      <Grid item>
        <div className={classes.root} data-cy="frame-content">
          {children}
        </div>
      </Grid>
      <Grid item>
        <hr />
        <Footer />
      </Grid>
    </Grid>
  );
};
