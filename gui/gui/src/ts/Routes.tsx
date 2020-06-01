import {BrowserRouter, Route, Switch} from "react-router-dom";
import {NodeSearchResultsPage} from "./components/pages/NodeSearchResultsPage";
import * as React from "react";
import {NodePage} from "./components/pages/NodePage";
import {NoRoute} from "./components/error/NoRoute";
import {HomePage} from "./components/pages/HomePage";

export const Routes: React.FunctionComponent = () => (
  <BrowserRouter>
    <Switch>
      <Route component={NodeSearchResultsPage} path="/node/search"></Route>
      <Route component={NodePage} path="/node/" />
      <Route exact component={HomePage} path="/"></Route>
      <Route component={NoRoute} />
    </Switch>
  </BrowserRouter>
);
