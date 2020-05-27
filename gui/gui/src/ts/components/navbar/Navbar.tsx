import * as React from "react";

import * as qs from "qs";

import {
  Typography,
  AppBar,
  Toolbar,
  makeStyles,
  createStyles,
} from "@material-ui/core";

import {SearchTextInput} from "components/search/SearchTextInput";
import {useHistory} from "react-router-dom";

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

  const onSearchSubmit = (search: string) => {
    history.push(qs.stringify({search}, {addQueryPrefix: true}));
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" className={classes.brand}>
          MOWGLI
        </Typography>
        <SearchTextInput onSubmit={onSearchSubmit} />
      </Toolbar>
    </AppBar>
  );
};
