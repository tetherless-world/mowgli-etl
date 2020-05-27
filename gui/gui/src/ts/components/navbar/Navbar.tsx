import * as React from "react";

import {Typography, AppBar, Toolbar} from "@material-ui/core";

export const Navbar: React.FunctionComponent<{}> = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6">MOWGLI</Typography>
      </Toolbar>
    </AppBar>
  );
};
