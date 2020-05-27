import * as React from "react";

import {Paper, InputAdornment, InputBase} from "@material-ui/core";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faSearch} from "@fortawesome/free-solid-svg-icons";

export const SearchTextInput: React.FunctionComponent<{
  onSubmit: (value: string) => void;
}> = ({onSubmit}) => {
  const searchInputRef = React.useRef<HTMLInputElement>(null);

  return (
    <Paper variant="outlined" square>
      <form
        onSubmit={(event: React.FormEvent<HTMLFormElement>) => {
          event.preventDefault();

          onSubmit(searchInputRef.current!.value);
        }}
      >
        <InputBase
          inputProps={{
            "data-cy": "searchTextInput",
            ref: searchInputRef,
          }}
          fullWidth
          startAdornment={
            <InputAdornment position="end" style={{marginRight: "8px"}}>
              <FontAwesomeIcon icon={faSearch} />
            </InputAdornment>
          }
        ></InputBase>
      </form>
    </Paper>
  );
};
