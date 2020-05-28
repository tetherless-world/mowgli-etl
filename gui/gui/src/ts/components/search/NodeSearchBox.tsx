import * as React from "react";

import {Paper, InputAdornment, InputBase} from "@material-ui/core";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faSearch} from "@fortawesome/free-solid-svg-icons";

export const NodeSearchBox: React.FunctionComponent<{
  onSubmit: (value: string) => void;
}> = ({onSubmit}) => {
  const [search, setSearch] = React.useState<{text: string}>({text: ""});

  return (
    <Paper variant="outlined" square>
      <form
        onSubmit={(event: React.FormEvent<HTMLFormElement>) => {
          event.preventDefault();

          onSubmit(search.text);
        }}
      >
        <InputBase
          inputProps={{
            "data-cy": "searchTextInput",
          }}
          value={search.text}
          onChange={(event: React.ChangeEvent<HTMLInputElement>) =>
            setSearch((prevSearch) => ({
              ...prevSearch,
              text: event.target.value,
            }))
          }
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
