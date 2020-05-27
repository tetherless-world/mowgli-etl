import * as React from "react";

import * as qs from "qs";

import {
  Typography,
  AppBar,
  Toolbar,
  makeStyles,
  createStyles,
} from "@material-ui/core";

import {NodeLabelSearch} from "components/search/NodeLabelSearch";
import {useHistory} from "react-router-dom";
import {Hrefs} from "Hrefs";

const useStyles = makeStyles((theme) =>
  createStyles({
    brand: {
      marginRight: theme.spacing(2),
    },
  })
);

export const Navbar: React.FunctionComponent<{}> = () => {
  const classes = useStyles();

  const history = useHistory();

  const onSearchSubmit = (text: string) => {
    history.push(
      Hrefs.nodeSearch + qs.stringify({text}, {addQueryPrefix: true})
    );
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" className={classes.brand}>
          MOWGLI
        </Typography>
        <NodeLabelSearch onSubmit={onSearchSubmit} />
      </Toolbar>
    </AppBar>
  );
};
