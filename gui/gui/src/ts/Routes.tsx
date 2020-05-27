import {Route} from "react-router-dom";
import {NodeSearchPage} from "./components/pages/NodeSearchPage";
import * as React from "react";
import {NodePage} from "./components/pages/NodePage";

export const Routes: React.FunctionComponent = () => (
    <React.Fragment>
        <Route exact component={NodePage} path="/node/:id"/>
        <Route component={NodeSearchPage}></Route>
    </React.Fragment>
);

