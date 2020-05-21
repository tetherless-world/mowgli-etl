import * as React from "react";

export const Frame: React.FunctionComponent<{children: React.ReactNode}> = ({children}) => {
 return (
  <div>
      {children}
  </div>
 );
}
