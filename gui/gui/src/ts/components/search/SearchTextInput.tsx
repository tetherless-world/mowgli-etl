import * as React from "react";

import {Paper, InputAdornment, InputBase} from "@material-ui/core";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faSearch} from "@fortawesome/free-solid-svg-icons";

export const SearchTextInput: React.FunctionComponent<{
  onSubmit: (value: string) => void;
}> = ({onSubmit}) => {
  return (
    <Paper variant="outlined" square>
      <InputBase
        inputProps={{
          "data-cy": "searchTextInput",
        }}
        fullWidth
        startAdornment={
          <InputAdornment position="end" style={{marginRight: "8px"}}>
            <FontAwesomeIcon icon={faSearch} />
          </InputAdornment>
        }
        onKeyDown={(event: React.KeyboardEvent<HTMLInputElement>) => {
          if (event.which === 13) {
            // Submit when user presses enter
            onSubmit(event.currentTarget!.value);
          }
        }}
      ></InputBase>
    </Paper>
  );
};
