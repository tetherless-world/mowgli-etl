import * as React from "react";

import {NodeSearchBox} from "components/search/NodeSearchBox";
import {HomePageQuery} from "api/queries/types/HomePageQuery";
import {useQuery} from "@apollo/react-hooks";
import * as HomePageQueryDocument from "api/queries/HomePageQuery.graphql";
import {Frame} from "components/frame/Frame";

import {
  Grid,
  Container,
  Typography,
  makeStyles,
  createStyles,
  Button,
} from "@material-ui/core";

import {useHistory} from "react-router-dom";

import {Hrefs} from "Hrefs";

const useStyles = makeStyles((theme) =>
  createStyles({
    container: {
      paddingTop: theme.spacing(5),
    },
    title: {
      fontFamily: "Hiragino Maru Gothic Pro",
    },
    primaryText: {
      color: theme.palette.primary.main,
    },
  })
);

export const HomePage: React.FunctionComponent = () => {
  const classes = useStyles();

  const history = useHistory();

  const {data} = useQuery<HomePageQuery>(HomePageQueryDocument);

  const [search, setSearch] = React.useState<{text: string}>({text: ""});

  const onSearchInputChange = (text: string) => {
    setSearch((prevSearch) => ({...prevSearch, text}));
  };

  const searchText = (text: string) => {
    if (text.length === 0) return;

    history.push(Hrefs.nodeSearch({text}));
  };

  return (
    <Frame>
      <Container maxWidth="md" className={classes.container}>
        <Grid container direction="column" spacing={3}>
          <Grid item>
            <Typography variant="h2" className={classes.title}>
              MOWGLI
            </Typography>
            <Typography variant="body1">
              DARPA Machine Common Sense (MCS) Multi-modal Open World Grounded
              Learning and Inference (MOWGLI)
            </Typography>
          </Grid>
          <Grid item>
            {data && (
              <Typography>
                Search{" "}
                <strong data-cy="totalNodeCount">
                  {data.totalNodesCount} nodes
                </strong>{" "}
                with{" "}
                <strong data-cy="totalEdgeCount">
                  {data.totalEdgesCount} relationships
                </strong>
              </Typography>
            )}
            <NodeSearchBox
              placeholder="Search a word"
              showIcon={true}
              onChange={onSearchInputChange}
            />
            <br />
            <Button
              color="primary"
              variant="contained"
              onClick={() => searchText(search.text)}
            >
              Search
            </Button>
            <Button color="primary" href={Hrefs.randomNode}>
              Show me something interesting
            </Button>
          </Grid>
        </Grid>
      </Container>
    </Frame>
  );
};
