import * as React from "react";
import {Grid, Typography, Button} from "@material-ui/core";
import {Frame} from "components/frame/Frame";
import {SearchTextInput} from "components/search/SearchTextInput";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faFilter} from "@fortawesome/free-solid-svg-icons";
import {useApolloClient} from "@apollo/react-hooks";
import {
  MatchingNodesQuery,
  MatchingNodesQueryVariables,
} from "api/queries/types/MatchingNodesQuery";
import * as MatchingNodesQueryDocument from "api/queries/MatchingNodesQuery.graphql";
import {NodeTable} from "components/data/NodeTable";
import {Node} from "models/Node";

interface MatchingNodesQueryState {
  matchingNodes: Node[];
  searchText: string;
  count: number;
  offset: number;
  queryLimit: number;
}

export const NodeSearchPage: React.FunctionComponent<{}> = ({}) => {
  const [state, setState] = React.useState<MatchingNodesQueryState>({
    matchingNodes: [],
    searchText: "",
    count: 0,
    offset: 0,
    queryLimit: 10,
  });

  const onLoadedData = (updatedState: Partial<MatchingNodesQueryState>) =>
    setState((prevState) => ({...prevState, ...updatedState}));

  const apolloClient = useApolloClient();

  const onSearchSubmit = (searchText: string) =>
    apolloClient
      .query<MatchingNodesQuery, MatchingNodesQueryVariables>({
        query: MatchingNodesQueryDocument,
        variables: {
          limit: state.queryLimit,
          offset: state.offset,
          text: searchText,
          withCount: true,
        },
      })
      .then(({data}) =>
        onLoadedData({
          matchingNodes: data.matchingNodes,
          count: data.matchingNodesCount,
          searchText: searchText,
        })
      );

  const onTableChangePage = (newPage: number) => {
    const newOffset = newPage * state.queryLimit;

    apolloClient
      .query<MatchingNodesQuery, MatchingNodesQueryVariables>({
        query: MatchingNodesQueryDocument,
        variables: {
          limit: state.queryLimit,
          offset: newOffset,
          text: state.searchText,
          withCount: false,
        },
      })
      .then(({data}) =>
        onLoadedData({matchingNodes: data.matchingNodes, offset: newOffset})
      );
  };

  const onTableChangeRowsPerPage = (newRowsPerPage: number) =>
    apolloClient
      .query<MatchingNodesQuery, MatchingNodesQueryVariables>({
        query: MatchingNodesQueryDocument,
        variables: {
          limit: newRowsPerPage,
          offset: 0,
          text: state.searchText,
          withCount: false,
        },
      })
      .then(({data}) =>
        onLoadedData({
          matchingNodes: data.matchingNodes,
          offset: 0,
          queryLimit: newRowsPerPage,
        })
      );

  const {matchingNodes, count, searchText, queryLimit, offset} = state;

  return (
    <Frame>
      <Grid container spacing={3}>
        <Grid item xs={12} data-cy="searchContainer">
          <Typography variant="body1">
            Searching <span>all data sources</span>
          </Typography>
          <SearchTextInput onSubmit={onSearchSubmit} />
          <Button>
            <FontAwesomeIcon icon={faFilter} /> &nbsp;Filters
          </Button>
        </Grid>
        <Grid item xs={8} data-cy="visualizationContainer">
          {searchText.length > 0 && (
            <React.Fragment>
              <Typography variant="body1">
                {count} results for "{searchText}"
              </Typography>
              <NodeTable
                nodes={matchingNodes}
                rowsPerPage={queryLimit}
                count={count}
                page={offset / queryLimit}
                onChangePage={onTableChangePage}
                onChangeRowsPerPage={onTableChangeRowsPerPage}
              />
            </React.Fragment>
          )}
        </Grid>
        <Grid item xs={4} container direction="column">
          <Grid item>Extra information</Grid>
        </Grid>
      </Grid>
    </Frame>
  );
};
