import * as React from "react";

import {RouteComponentProps} from "react-router";

import {Frame} from "components/frame/Frame";

export const NoRoute: React.FunctionComponent<RouteComponentProps> = ({
  location,
}) => (
  <Frame>
    <h3>
      <code>{location.pathname}</code>
    </h3>
  </Frame>
);
