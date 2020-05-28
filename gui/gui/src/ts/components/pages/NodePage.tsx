import * as React from "react";
import {useLocation} from "react-router-dom";
import * as NodePageQueryDocument from "api/queries/NodePageQuery.graphql";
import {
  NodePageQuery,
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
  ListItemText,
  Table,
  TableBody,
  TableCell,
  TableRow,
} from "@material-ui/core";
import {NodeLink} from "../node/NodeLink";
// import {makeStyles} from "@material-ui/core/styles";

// const useStyles = makeStyles((theme) => ({
//   nodePropertyValue: {
//     fontWeight: "bold",
//   },
// }));

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

  return (
    <Frame>
      <Card>
        <Grid container direction="column">
          <Grid item container>
            <Grid item xs={10}>
              <CardHeader title={title} />
            </Grid>
            <Grid item xs={2}>
              <h3>Data source: {node.datasource}</h3>
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
            <CardContent>
              <Table>
                <TableBody>
                  {node.subjectOfEdges.map((edge) => (
                    <TableRow>
                      <TableCell>{edge.predicate}</TableCell>
                      <TableCell>
                        {edge.objectNode ? (
                          <NodeLink node={edge.objectNode} />
                        ) : (
                          edge.object
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Grid>
        </Grid>
      </Card>
    </Frame>
  );
};
