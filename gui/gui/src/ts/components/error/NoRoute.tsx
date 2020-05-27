import * as React from "react";

import {useLocation} from "react-router";

import {Frame} from "components/frame/Frame";

export const NoRoute: React.FunctionComponent = () => {
  const location = useLocation();
  return (
    <Frame>
      <h3>
        <code>{location.pathname}</code>
      </h3>
    </Frame>
  );
};
