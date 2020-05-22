import * as React from "react";
import {Grid, Typography, Button} from "@material-ui/core";
import {Frame} from "components/frame/Frame";
import {SearchTextInput} from "components/search/SearchTextInput";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faFilter} from "@fortawesome/free-solid-svg-icons";
import {useQuery} from "@apollo/react-hooks";
import {MatchingNodesQuery} from "api/queries/types/MatchingNodesQuery";
import * as matchingNodesQuery from "api/queries/MatchingNodesQuery.graphql";
import {NodeTable} from "components/data/NodeTable";

export const NodeSearchPage: React.FunctionComponent<{}> = ({}) => {
  const [searchText, setSearchText] = React.useState<string>("");
  const [matchingNodesCount, setMatchingNodesCount] = React.useState<
    number | null
  >(null);
  const [matchingNodesPage, setMatchingNodesPage] = React.useState<number>(0);
  const [matchingNodesQueryLimit, setMatchingNodesQueryLimit] = React.useState<
    number
  >(10);

  const onSearchSubmit = (searchText: string) => {
    setSearchText(searchText);
    setMatchingNodesCount(null);
  };

  const {data, loading} = useQuery<MatchingNodesQuery>(matchingNodesQuery, {
    variables: {
      limit: matchingNodesQueryLimit,
      offset: matchingNodesPage,
      text: searchText,
      withCount: matchingNodesCount === null,
    },
    skip: searchText.length === 0,
  });

  const matchingNodes = data?.matchingNodes;

  if (data && data.matchingNodesCount && matchingNodesCount === null) {
    setMatchingNodesCount(data!.matchingNodesCount!);
  }

  const onTableChangePage = (newPage: number) => {
    setMatchingNodesPage(newPage);
  };

  const onTableChangeRowsPerPage = (newRowsPerPage: number) => {
    setMatchingNodesQueryLimit(newRowsPerPage);
    setMatchingNodesPage(0);
  };

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
          {loading && "Loading"}
          {matchingNodes && matchingNodesCount && (
            <React.Fragment>
              <Typography variant="body1">
                {matchingNodesCount} results for "{searchText}"
              </Typography>
              <NodeTable
                nodes={matchingNodes}
                rowsPerPage={matchingNodesQueryLimit}
                count={matchingNodesCount}
                page={matchingNodesPage}
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
