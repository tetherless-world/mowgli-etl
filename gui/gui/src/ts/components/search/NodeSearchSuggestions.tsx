import * as React from "react";
import * as _ from "lodash";
import * as ReactLoader from "react-loader";
import {
  Popper,
  PopperProps,
  List,
  ListItem,
  ListItemText,
  Paper,
  Typography,
  makeStyles,
} from "@material-ui/core";
import {GraphQLError} from "graphql";
import {useApolloClient} from "@apollo/react-hooks";
import {
  NodeSearchResultsPageQuery,
  NodeSearchResultsPageQueryVariables,
} from "api/queries/types/NodeSearchResultsPageQuery";
import * as NodeSearchResultsPageQueryDocument from "api/queries/NodeSearchResultsPageQuery.graphql";
import {Hrefs} from "Hrefs";

const useStyles = makeStyles({
  paper: {
    minWidth: "100px",
    minHeight: "50px",
  },
});

// Throttle wait duration in milliseconds
// Minimum time between requests
const THROTTLE_WAIT_DURATION = 500;

// Maximum number of suggestions to show
const MAXIMUM_SUGGESTIONS = 5;

// Used example in docs as reference
// https://material-ui.com/components/autocomplete/#google-maps-place

export const NodeSearchSuggestions: React.FunctionComponent<
  {
    search: string;
  } & Omit<PopperProps, "open" | "children">
> = ({search, ...popperProps}) => {
  const classes = useStyles();

  const apolloClient = useApolloClient();

  const [isLoading, setIsLoading] = React.useState<boolean>(false);

  const [isOpen, setIsOpen] = React.useState<boolean>(false);

  const [searchErrors, setSearchErrors] = React.useState<
    readonly GraphQLError[] | undefined
  >(undefined);

  const [searchResults, setSearchResults] = React.useState<
    NodeSearchResultsPageQuery
  >({matchingNodes: [], matchingNodesCount: 0});

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

    // If text input is empty, close dropdown
    if (search.length === 0) {
      setSearchResults((prevResults) => ({
        ...prevResults,
        matchingNodes: [],
        matchingNodesCount: 0,
      }));

      setIsOpen(false);

      // Call throttled query with new search text
    } else {
      throttledQuery.current(
        {text: search, limit: MAXIMUM_SUGGESTIONS, offset: 0, withCount: true},
        ({matchingNodes, matchingNodesCount}, errors) => {
          if (!active) return;

          if (!isOpen) setIsOpen(true);

          if (errors !== searchErrors) {
            setSearchErrors(errors);
          }

          setSearchResults((prevResults) => ({
            ...prevResults,
            matchingNodes,
            matchingNodesCount,
          }));
        }
      );
    }

    return () => {
      active = false;
    };
  }, [search, throttledQuery]);

  // See https://material-ui.com/components/lists/
  const ListItemLink = (props: any) => (
    <ListItem button component="a" {...props} />
  );

  return (
    <Popper open={isOpen} {...popperProps} data-cy="nodeSearchSuggestions">
      <Paper className={classes.paper} variant="outlined" square>
        <ReactLoader loaded={!isLoading}>
          {!searchErrors && (
            <List>
              {searchResults.matchingNodes.map((node) => (
                <ListItemLink href={Hrefs.node(node.id)}>
                  <ListItemText primary={node.label}></ListItemText>
                </ListItemLink>
              ))}
              {searchResults.matchingNodesCount > 0 && (
                <ListItemLink href={Hrefs.nodeSearch({text: search})}>
                  <ListItemText
                    primary={`See ${searchResults.matchingNodesCount} results`}
                  ></ListItemText>
                </ListItemLink>
              )}
              {searchResults.matchingNodesCount === 0 && (
                <ListItem>
                  <ListItemText primary="No results"></ListItemText>
                </ListItem>
              )}
            </List>
          )}
          {searchErrors && <Typography>{searchErrors.toString()}</Typography>}
        </ReactLoader>
      </Paper>
    </Popper>
  );
};
