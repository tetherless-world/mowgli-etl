import * as React from "react";
import {
  Typography,
  AppBar,
  Toolbar,
  makeStyles,
  createStyles,
} from "@material-ui/core";

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
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">Mowgli</Typography>
        </Toolbar>
      </AppBar>
      <div className={classes.root}>{children}</div>
    </React.Fragment>
  );
};
