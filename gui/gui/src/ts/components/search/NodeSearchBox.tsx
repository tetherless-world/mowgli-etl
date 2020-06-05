import * as React from "react";
import * as _ from "lodash";
import {Paper, InputAdornment, InputBase} from "@material-ui/core";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faSearch} from "@fortawesome/free-solid-svg-icons";
import {useHistory} from "react-router-dom";
import {Hrefs} from "Hrefs";
import {GraphQLError} from "graphql";
import {
  NodeSearchResultsPageQuery,
  NodeSearchResultsPageQueryVariables,
} from "api/queries/types/NodeSearchResultsPageQuery";
import {useApolloClient} from "@apollo/react-hooks";
import * as NodeSearchResultsPageQueryDocument from "api/queries/NodeSearchResultsPageQuery.graphql";
import Autocomplete from "@material-ui/lab/Autocomplete";
import {Node} from "models/Node";
import {DatasourceSelect} from "components/search/DatasourceSelect";

// Throttle wait duration in milliseconds
// Minimum time between requests
const THROTTLE_WAIT_DURATION = 500;

// Maximum number of suggestions to show
const MAXIMUM_SUGGESTIONS = 5;

export const NodeSearchBox: React.FunctionComponent<{
  placeholder?: string;
  showIcon?: boolean;
  onSubmit?: (value: string | Node) => void;
  style?: React.CSSProperties;
  value?: string;
  onChange?: (value: string | Node) => void;
}> = ({
  onSubmit: onSubmitUserDefined,
  showIcon = false,
  placeholder,
  style,
  value,
  onChange,
}) => {
  const history = useHistory();

  const apolloClient = useApolloClient();

  const [search, setSearch] = React.useState<{text: string}>({
    text: value || "",
  });

  const [datasources, setDatasources] = React.useState<string[]>([]);

  const onSubmit = onSubmitUserDefined
    ? onSubmitUserDefined
    : (value: string | Node) => {
        if (typeof value === "string") {
          if (value.length === 0) return;

          history.push(Hrefs.nodeSearch({text: value}));
        } else {
          history.push(Hrefs.node(value.id));
        }
      };

  const [
    selectedSearchResult,
    setSelectedSearchResult,
  ] = React.useState<Node | null>(null);

  const [searchErrors, setSearchErrors] = React.useState<
    readonly GraphQLError[] | undefined
  >(undefined);

  const [searchResults, setSearchResults] = React.useState<Node[]>([]);

  const [isLoading, setIsLoading] = React.useState<boolean>(false);

  // Query server for search results to display
  // Is throttled so server request is only sent
  // once every THROTTLE_WAIT_DURATION
  // If a call is made within that duration, the
  // callback is called with the previous result
  const throttledQuery = React.useRef(
    _.throttle(
      (
        variables: NodeSearchResultsPageQueryVariables,
        callback: (
          data: NodeSearchResultsPageQuery,
          errors: readonly GraphQLError[] | undefined
        ) => void
      ) => {
        // If there were searchErrors from previous query,
        // clear errors before new query
        if (searchErrors !== undefined) {
          setSearchErrors(undefined);
        }

        setIsLoading(true);

        apolloClient
          .query<
            NodeSearchResultsPageQuery,
            NodeSearchResultsPageQueryVariables
          >({query: NodeSearchResultsPageQueryDocument, variables})
          .then(({data, errors}) => {
            setIsLoading(false);
            callback(data, errors);
          });
      },
      THROTTLE_WAIT_DURATION
    )
  );

  // Execute this block of code when the text input value changes
  React.useEffect(() => {
    let active = true;

    // If text input is empty, skip query
    if (search.text.length === 0) {
      return;
    }

    // Call throttled query with new search text
    throttledQuery.current(
      {
        text: `label:${search.text} ${datasources
          .map((d) => "datasource:" + d)
          .join(" ")}`,
        limit: MAXIMUM_SUGGESTIONS,
        offset: 0,
        withCount: false,
      },
      ({matchingNodes}, errors) => {
        if (!active) return;

        if (errors !== searchErrors) {
          setSearchErrors(errors);
        }

        setSearchResults(matchingNodes);
      }
    );

    return () => {
      active = false;
    };
  }, [search.text, datasources, throttledQuery]);

  return (
    <form
      data-cy="nodeSearchBox"
      onSubmit={(event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        onSubmit!(selectedSearchResult || search.text);
      }}
    >
      <Autocomplete
        style={{display: "inline-flex", verticalAlign: "top"}}
        getOptionLabel={(option: Node | string) =>
          typeof option === "string" ? option : option.label!
        }
        options={searchResults}
        freeSolo
        disablePortal
        includeInputInList
        loading={isLoading}
        noOptionsText="No results"
        inputValue={search.text}
        onInputChange={(_, newInputValue: string) => {
          setSearch((prevSearch) => ({...prevSearch, text: newInputValue}));
          if (onChange && !selectedSearchResult) onChange(newInputValue);
        }}
        onHighlightChange={(_, option: Node | null) => {
          if (onChange) onChange(option || search.text);
          setSelectedSearchResult(option);
        }}
        renderInput={(params) => (
          <Paper variant="outlined" square style={style}>
            <InputBase
              inputProps={{
                "data-cy": "searchTextInput",
                style: {paddingLeft: "5px"},
                ...params.inputProps,
              }}
              ref={params.InputProps.ref}
              placeholder={placeholder}
              fullWidth
              startAdornment={
                showIcon ? (
                  <InputAdornment position="end" style={{marginRight: "8px"}}>
                    <FontAwesomeIcon icon={faSearch} />
                  </InputAdornment>
                ) : null
              }
              error={searchErrors !== undefined}
            ></InputBase>
          </Paper>
        )}
        renderOption={(node) => (
          <a href={Hrefs.node(node.id)}>
            {node.label} - {node.datasource}
          </a>
        )}
      ></Autocomplete>
      <DatasourceSelect
        style={{display: "inline-flex", verticalAlign: "top"}}
        value={datasources}
        onChange={(newDatasources: string[]) => {
          setDatasources(newDatasources);
        }}
      ></DatasourceSelect>
    </form>
  );
};
