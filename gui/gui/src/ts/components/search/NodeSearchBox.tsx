import * as React from "react";

import {Paper, InputAdornment, InputBase} from "@material-ui/core";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faSearch} from "@fortawesome/free-solid-svg-icons";
import {useHistory} from "react-router-dom";
import {Hrefs} from "Hrefs";

export const NodeSearchBox: React.FunctionComponent<{
  placeholder?: string;
  showIcon?: boolean;
  onSubmit?: (value: string) => void;
  style?: React.CSSProperties;
  value?: string;
  onChange?: (value: string) => void;
}> = ({
  onSubmit: onSubmitUserDefined,
  showIcon = false,
  placeholder,
  style,
  value,
  onChange,
}) => {
  const [search, setSearch] = React.useState<{text: string}>({
    text: value || "",
  });

  const history = useHistory();

  const onSubmit = onSubmitUserDefined
    ? onSubmitUserDefined
    : (text: string) => {
        if (text.length === 0) return;

        history.push(Hrefs.nodeSearch({text}));
      };

  return (
    <Paper variant="outlined" square style={style}>
      <form
        onSubmit={(event: React.FormEvent<HTMLFormElement>) => {
          event.preventDefault();

          onSubmit!(search.text);
        }}
      >
        <InputBase
          inputProps={{
            "data-cy": "searchTextInput",
            style: {paddingLeft: "5px"},
          }}
          placeholder={placeholder}
          value={search.text}
          onChange={(event) => {
            const text = event.target.value;
            if (onChange) onChange(text);
            setSearch((prevSearch) => ({
              ...prevSearch,
              text,
            }));
          }}
          fullWidth
          startAdornment={
            showIcon ? (
              <InputAdornment position="end" style={{marginRight: "8px"}}>
                <FontAwesomeIcon icon={faSearch} />
              </InputAdornment>
            ) : null
          }
        ></InputBase>
      </form>
    </Paper>
  );
};
