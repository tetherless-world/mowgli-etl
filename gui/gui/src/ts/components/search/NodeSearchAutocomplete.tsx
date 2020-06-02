import * as React from "react";
import * as _ from "lodash";
import {
  Popper,
  PopperProps,
  List,
  ListItem,
  ListItemText,
  Paper,
} from "@material-ui/core";
import {useApolloClient} from "@apollo/react-hooks";
import {
  NodeSearchResultsPageQuery,
  NodeSearchResultsPageQueryVariables,
} from "api/queries/types/NodeSearchResultsPageQuery";
import * as NodeSearchResultsPageQueryDocument from "api/queries/NodeSearchResultsPageQuery.graphql";
import {Hrefs} from "Hrefs";

const THROTTLE_WAIT_DURATION = 200;

export const NodeSearchAutocomplete: React.FunctionComponent<
  {
    search: string;
  } & Omit<PopperProps, "open" | "children">
> = ({search, ...popperProps}) => {
  const apolloClient = useApolloClient();

  const [isOpen, setIsOpen] = React.useState<boolean>(false);

  const [searchResults, setSearchResults] = React.useState<
    NodeSearchResultsPageQuery
  >({matchingNodes: [], matchingNodesCount: 0});

  const throttledQuery = React.useRef(
    _.throttle(
      (
        variables: NodeSearchResultsPageQueryVariables,
        callback: (data: NodeSearchResultsPageQuery) => void
      ) => {
        apolloClient
          .query<
            NodeSearchResultsPageQuery,
            NodeSearchResultsPageQueryVariables
          >({query: NodeSearchResultsPageQueryDocument, variables})
          .then(({data}) => callback(data));
      },
      THROTTLE_WAIT_DURATION
    )
  );

  React.useEffect(() => {
    let active = true;

    if (search.length === 0) {
      setSearchResults((prevResults) => ({
        ...prevResults,
        matchingNodes: [],
        matchingNodesCount: 0,
      }));

      setIsOpen(false);
    } else {
      throttledQuery.current(
        {text: search, limit: 5, offset: 0, withCount: true},
        ({matchingNodes, matchingNodesCount}) => {
          if (!active) return;

          if (!isOpen) setIsOpen(true);

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

  return (
    <Popper open={isOpen} {...popperProps}>
      <Paper variant="outlined" square>
        <List>
          {searchResults.matchingNodes.map((node) => (
            <ListItem component="a" href={Hrefs.node(node.id)}>
              <ListItemText primary={node.label}></ListItemText>
            </ListItem>
          ))}
          {searchResults.matchingNodesCount > 0 && (
            <ListItem component="a" href={Hrefs.nodeSearch({text: search})}>
              <ListItemText
                primary={`See ${searchResults.matchingNodesCount} results`}
              ></ListItemText>
            </ListItem>
          )}
          {searchResults.matchingNodesCount === 0 && (
            <ListItem>
              <ListItemText primary="No results"></ListItemText>
            </ListItem>
          )}
        </List>
      </Paper>
    </Popper>
  );
};
