import * as React from "react";
import {Grid, Typography} from "@material-ui/core";
import {Frame} from "components/frame/Frame";

import {useQuery} from "@apollo/react-hooks";
import {
  NodeSearchResultsPageQuery,
  NodeSearchResultsPageQueryVariables,
} from "api/queries/types/NodeSearchResultsPageQuery";
import * as NodeSearchResultsPageQueryDocument from "api/queries/NodeSearchResultsPageQuery.graphql";
import {NodeTable} from "components/data/NodeTable";

import * as ReactLoader from "react-loader";
import {useLocation, useHistory} from "react-router-dom";
import * as qs from "qs";
import {FatalErrorModal} from "components/error/FatalErrorModal";
import {ApolloException} from "@tetherless-world/twxplore-base";

interface NodeSearchVariables {
  text: string;
  offset?: number;
  limit?: number;
}

class QueryStringNodeSearchVariables implements NodeSearchVariables {
  private constructor(
    public readonly text: string,
    public readonly offset: number = 0,
    public readonly limit: number = 10
  ) {}

  get page() {
    return this.offset / this.limit;
  }

  get object() {
    return {text: this.text, offset: this.offset, limit: this.limit};
  }

  static parse(queryString: string) {
    const {text, offset, limit} = (qs.parse(queryString, {
      ignoreQueryPrefix: true,
    }) as unknown) as {
      text: string;
      offset: string;
      limit: string;
    };
    return new QueryStringNodeSearchVariables(
      text,
      offset === undefined ? undefined : +offset,
      limit === undefined ? undefined : +limit
    );
  }

  stringify() {
    return qs.stringify(this.object, {addQueryPrefix: true});
  }

  replace({text, offset, limit}: Partial<NodeSearchVariables>) {
    return new QueryStringNodeSearchVariables(
      text !== undefined ? text : this.text,
      offset !== undefined ? offset : this.offset,
      limit !== undefined ? limit : this.limit
    );
  }
}

export const NodeSearchResultsPage: React.FunctionComponent<{}> = ({}) => {
  const history = useHistory();

  const location = useLocation();

  const searchVariables = QueryStringNodeSearchVariables.parse(location.search);

  const [count, setCount] = React.useState<number | null>(null);

  const {data, loading, error} = useQuery<
    NodeSearchResultsPageQuery,
    NodeSearchResultsPageQueryVariables
  >(NodeSearchResultsPageQueryDocument, {
    variables: {...searchVariables.object, withCount: count === null},
    skip: !searchVariables.text, // Remove this when new landing page is added
  });

  if (error) {
    return <FatalErrorModal exception={new ApolloException(error)} />;
  }

  if (loading && count !== null) {
    setCount(null);
  }

  if (data?.matchingNodesCount && count === null) {
    setCount(data.matchingNodesCount);
  }

  return (
    <Frame>
      <Grid container spacing={3}>
        <Grid item xs={8} data-cy="visualizationContainer">
          <ReactLoader loaded={!loading}>
            <Typography variant="h6">
              {count || "No"} results for "{searchVariables.text}"
            </Typography>
            {count && (
              <NodeTable
                nodes={data?.matchingNodes || []}
                rowsPerPage={searchVariables.limit}
                count={count}
                page={searchVariables.page}
                onChangePage={(newPage: number) =>
                  history.push(
                    searchVariables
                      .replace({offset: newPage * searchVariables.limit})
                      .stringify()
                  )
                }
                onChangeRowsPerPage={(newRowsPerPage: number) =>
                  history.push(
                    searchVariables
                      .replace({offset: 0, limit: newRowsPerPage})
                      .stringify()
                  )
                }
              />
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
