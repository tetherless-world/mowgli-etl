import * as React from "react";
import {Navbar} from "components/navbar/Navbar";

import {makeStyles, createStyles} from "@material-ui/core";

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
    <React.Fragment>
      <Navbar></Navbar>
      <div className={classes.root}>{children}</div>
    </React.Fragment>
  );
};
