import {BrowserRouter, Route, Switch} from "react-router-dom";
import {NodeSearchResultsPage} from "./components/pages/NodeSearchResultsPage";
import * as React from "react";
import {NodePage} from "./components/pages/NodePage";
import {NoRoute} from "./components/error/NoRoute";

export const Routes: React.FunctionComponent = () => (
  <BrowserRouter>
    <Switch>
      <Route component={NodePage} path="/node/" />
      <Route exact component={NodeSearchResultsPage} path="/"></Route>
      <Route component={NoRoute} />
    </Switch>
  </BrowserRouter>
);
