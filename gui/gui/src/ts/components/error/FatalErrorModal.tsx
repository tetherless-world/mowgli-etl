import * as React from "react";
import {Exception} from "@tetherless-world/twxplore-base";
import {Dialog, DialogContent, DialogTitle} from "@material-ui/core";

interface Props {
  error?: Error;
  exception?: Exception;
  message?: string;
  onExit?: () => void;
}

export class FatalErrorModal extends React.Component<Props> {
  render() {
    let {message, onExit} = this.props;
    if (!onExit) {
      onExit = () => {
        return;
      };
    }
    const {error, exception} = this.props;
    if (!message) {
      if (error) {
        message = error.toString();
      } else if (exception) {
        message = exception.message;
      } else {
        message = "";
      }
    }

    return (
      <div>
        <Dialog open={true} onClose={onExit}>
          <DialogTitle>Fatal error</DialogTitle>
          <DialogContent>{message}</DialogContent>
        </Dialog>
      </div>
    );
  }
}
