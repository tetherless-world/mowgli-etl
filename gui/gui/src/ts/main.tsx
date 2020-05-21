import {apolloClient} from "api/apolloClient";
import * as React from "react";
import * as ReactDOM from "react-dom";
import {BrowserRouter} from "react-router-dom";
import {ApolloProvider} from "react-apollo";
import {ApolloProvider as ApolloHooksProvider} from "@apollo/react-hooks";
import {CssBaseline} from "@material-ui/core";
import {ConsoleLogger, LoggerContext} from "@tetherless-world/twxplore-base";

// Logger
const logger = new ConsoleLogger();

ReactDOM.render(
  <ApolloProvider client={apolloClient}>
    <ApolloHooksProvider client={apolloClient}>
      <LoggerContext.Provider value={logger}>
        <BrowserRouter>
          <CssBaseline />
          {/*<Route component={Frame}></Route>*/}
        </BrowserRouter>
      </LoggerContext.Provider>
    </ApolloHooksProvider>
  </ApolloProvider>,
  document.getElementById("root")
);
