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
    <div data-cy="frame">
      <Navbar></Navbar>
      <div className={classes.root} data-cy="frame-content">
        {children}
      </div>
    </div>
  );
};
