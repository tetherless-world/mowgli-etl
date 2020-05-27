import * as React from "react";
import {Grid, Typography} from "@material-ui/core";
import {Frame} from "components/frame/Frame";
// import {SearchTextInput} from "components/search/SearchTextInput";
import {useApolloClient} from "@apollo/react-hooks";
import {
  MatchingNodesQuery,
  MatchingNodesQueryVariables,
} from "api/queries/types/MatchingNodesQuery";
import * as MatchingNodesQueryDocument from "api/queries/MatchingNodesQuery.graphql";
import {NodeTable} from "components/data/NodeTable";
import {Node} from "models/Node";
import * as ReactLoader from "react-loader";
import {useLocation} from 'react-router-dom';
import * as qs from 'qs';

interface Matching

class MatchingNodesQueryState {
  // matchingNodes: Node[];
  private constructor (
  public readonly searchText: string,
  // public readonly count: number,
  public readonly offset: number = 0,
  public readonly queryLimit: number = 10,
  ) {}

  parse(queryString: string) {
    const {search, offset, limit} = qs.parse(queryString, {ignoreQueryPrefix:true})
    return new MatchingNodesQueryState(search as string, offset, limit);
  }
}

export const NodeSearchPage: React.FunctionComponent<{}> = ({}) => {
  const location = useLocation();

  const locationQueryObject = ((qs.parse(location.search, {ignoreQueryPrefix:true}) as unknown) as MatchingNodesQuery);

  // const [state, setState] = React.useState<MatchingNodesQueryState>({
  //   matchingNodes: [],
  //   // searchText: "",
  //   count: 0,
  //   offset: 0,
  //   queryLimit: 10,
  // });

  // const [loading, setLoading] = React.useState<boolean>(false);

  // const onLoadedData = (updatedState: Partial<MatchingNodesQuery>) => {
  //   setState((prevState) => ({...prevState, ...updatedState}));
  //   setLoading(false);
  // };

  // const apolloClient = useApolloClient();

  // const onSearchSubmit = (searchText: string) => {
  //   setLoading(true);
  //   apolloClient
  //     .query<MatchingNodesQuery, MatchingNodesQueryVariables>({
  //       query: MatchingNodesQueryDocument,
  //       variables: {
  //         limit: state.queryLimit,
  //         offset: state.offset,
  //         text: searchText,
  //         withCount: true,
  //       },
  //     })
  //     .then(({data}) =>
  //       onLoadedData({
  //         matchingNodes: data.matchingNodes,
  //         count: data.matchingNodesCount,
  //         searchText: searchText,
  //       })
  //     );
  // };

  const onTableChangePage = (newPage: number) => {
    const newOffset = newPage * state.queryLimit;

    // apolloClient
    //   .query<MatchingNodesQuery, MatchingNodesQueryVariables>({
    //     query: MatchingNodesQueryDocument,
    //     variables: {
    //       limit: state.queryLimit,
    //       offset: newOffset,
    //       text: searchText,
    //       withCount: false,
    //     },
    //   })
    //   .then(({data}) =>
    //     onLoadedData({matchingNodes: data.matchingNodes, offset: newOffset})
    //   );
  };

  const onTableChangeRowsPerPage = (newRowsPerPage: number) => {}
    // apolloClient
    //   .query<MatchingNodesQuery, MatchingNodesQueryVariables>({
    //     query: MatchingNodesQueryDocument,
    //     variables: {
    //       limit: newRowsPerPage,
    //       offset: 0,
    //       text: searchText,
    //       withCount: false,
    //     },
    //   })
    //   .then(({data}) =>
    //     onLoadedData({
    //       matchingNodes: data.matchingNodes,
    //       offset: 0,
    //       queryLimit: newRowsPerPage,
    //     })
    //   );

  const {matchingNodes, count, queryLimit, offset} = state;

  return (
    <Frame>
      <Grid container spacing={3}>
        <Grid item xs={12} data-cy="searchContainer">
          <Typography variant="body1">
            Searching <span>all data sources</span>
          </Typography>
          {/* <SearchTextInput onSubmit={onSearchSubmit} /> */}
          {/* <Button>
            <FontAwesomeIcon icon={faFilter} /> &nbsp;Filters
          </Button> */}
        </Grid>
        <Grid item xs={8} data-cy="visualizationContainer">
          <ReactLoader loaded={!loading}>
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
          </ReactLoader>
        </Grid>
        {/* <Grid item xs={4} container direction="column">
          <Grid item>Extra information</Grid>
        </Grid> */}
      </Grid>
    </Frame>
  );
};
