import * as React from "react";
import {useLocation} from "react-router-dom";
import * as NodePageQueryDocument from "api/queries/NodePageQuery.graphql";
import {
  NodePageQuery,
  NodePageQuery_nodeById_subjectOfEdges,
  NodePageQueryVariables,
} from "api/queries/types/NodePageQuery";
import {useQuery} from "@apollo/react-hooks";
import {ApolloException} from "@tetherless-world/twxplore-base";
import {FatalErrorModal} from "components/error/FatalErrorModal";
import * as ReactLoader from "react-loader";
import {Frame} from "components/frame/Frame";
import {
  Card,
  CardContent,
  CardHeader,
  Grid,
  List,
  ListItem,
  ListItemText,
} from "@material-ui/core";
import {NodeLink} from "../node/NodeLink";
// import {makeStyles} from "@material-ui/core/styles";

// const useStyles = makeStyles((theme) => ({
//   nodePropertyValue: {
//     fontWeight: "bold",
//   },
// }));

const EDGE_PREDICATE_DISPLAY_NAMES: {[index: string]: string} = {};

const EdgeList: React.FunctionComponent<{
  edges: NodePageQuery_nodeById_subjectOfEdges[];
  predicate: string;
}> = ({edges, predicate}) => {
  let title = EDGE_PREDICATE_DISPLAY_NAMES[predicate];
  if (!title) {
    title = predicate;
  }
  return (
    <Card>
      <CardHeader
        data-cy="edge-list-title"
        title={title}
        style={{textAlign: "center"}}
      />
      <CardContent>
        <List>
          {edges.map((edge) => (
            <ListItem data-cy="edge" key={edge.object}>
              <NodeLink node={edge.objectNode!} />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export const NodePage: React.FunctionComponent = () => {
  const location = useLocation();
  const nodeId = location.pathname.split("/").slice(2).join("/");

  // const classes = useStyles();

  const {data, error, loading} = useQuery<
    NodePageQuery,
    NodePageQueryVariables
  >(NodePageQueryDocument, {variables: {id: nodeId}});

  if (error) {
    return <FatalErrorModal exception={new ApolloException(error)} />;
  } else if (loading) {
    return (
      <Frame>
        <ReactLoader loaded={false} />
      </Frame>
    );
  } else if (!data) {
    throw new EvalError();
  }

  const node = data.nodeById;
  if (!node) {
    return (
      <Frame>
        <h3>
          <code>{nodeId} not found</code>
        </h3>
      </Frame>
    );
  }

  const nodeLabel = node.label ? node.label : node.id;

  let title = nodeLabel;
  if (node.pos) {
    title += " (" + node.pos + ")";
  }

  const subjectOfEdgesByPredicate: {
    [index: string]: NodePageQuery_nodeById_subjectOfEdges[];
  } = {};
  for (const edge of node.subjectOfEdges) {
    if (!edge.objectNode) {
      continue;
    } else if (!edge.predicate) {
      continue;
    }
    const edges = subjectOfEdgesByPredicate[edge.predicate];
    if (edges) {
      edges.push(edge);
    } else {
      subjectOfEdgesByPredicate[edge.predicate] = [edge];
    }
  }

  return (
    <Frame>
      <Grid container direction="column">
        <Grid item container>
          <Grid item xs={10}>
            <h2 data-cy="node-title">{title}</h2>
          </Grid>
          <Grid item xs={2}>
            <h3>
              Data source:{" "}
              <span data-cy="node-datasource">{node.datasource}</span>
            </h3>
            {node.aliases ? (
              <React.Fragment>
                <h3>Aliases</h3>
                <List>
                  {node.aliases.map((alias) => (
                    <ListItemText key={alias}>{alias}</ListItemText>
                  ))}
                </List>
              </React.Fragment>
            ) : null}
          </Grid>
        </Grid>
        <Grid item>
          <Grid container spacing={4}>
            {Object.keys(subjectOfEdgesByPredicate).map((predicate) => (
              <Grid item key={predicate} data-cy={predicate + "-edges"}>
                <EdgeList
                  edges={subjectOfEdgesByPredicate[predicate]!}
                  predicate={predicate}
                />
              </Grid>
            ))}
          </Grid>
        </Grid>
      </Grid>
    </Frame>
  );
};
