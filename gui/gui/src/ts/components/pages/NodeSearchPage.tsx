import * as React from "react";
import {
  Grid,
  InputBase,
  Paper,
  InputAdornment,
  Typography,
  Button,
  Table,
  TableContainer,
  TableCell,
  TableHead,
  TableRow,
  TableFooter,
  TablePagination,
  TableBody,
  IconButton,
  useTheme,
  createStyles,
  makeStyles,
} from "@material-ui/core";
import {Frame} from "components/frame/Frame";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {
  faSearch,
  faFilter,
  faAngleLeft,
  faAngleRight,
  faAngleDoubleLeft,
  faAngleDoubleRight,
} from "@fortawesome/free-solid-svg-icons";
import {useQuery} from "@apollo/react-hooks";
import {MatchingNodesQuery} from "api/queries/types/MatchingNodesQuery";
import {MatchingNodesCountQuery} from "api/queries/types/MatchingNodesCountQuery";
import * as matchingNodesQuery from "api/queries/MatchingNodesQuery.graphql";
import * as matchingNodesCountQuery from "api/queries/MatchingNodesCountQuery.graphql";

// Using example Table Pagination Actions toolbar given by docs
// https://material-ui.com/components/tables/
const TablePaginationActionsUseStyles = makeStyles((theme) =>
  createStyles({
    root: {
      flexShrink: 0,
      marginLeft: theme.spacing(2.5),
    },
  })
);

interface TablePaginationActionsProps {
  count: number;
  page: number;
  rowsPerPage: number;
  onChangePage: (
    event: React.MouseEvent<HTMLButtonElement>,
    newPage: number
  ) => void;
}

function TablePaginationActions(props: TablePaginationActionsProps) {
  const classes = TablePaginationActionsUseStyles();
  const theme = useTheme();
  const {count, page, rowsPerPage, onChangePage} = props;

  const handleFirstPageButtonClick = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    onChangePage(event, 0);
  };

  const handleBackButtonClick = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    onChangePage(event, page - 1);
  };

  const handleNextButtonClick = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    onChangePage(event, page + 1);
  };

  const handleLastPageButtonClick = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    onChangePage(event, Math.max(0, Math.ceil(count / rowsPerPage) - 1));
  };

  return (
    <div className={classes.root}>
      <IconButton
        onClick={handleFirstPageButtonClick}
        disabled={page === 0}
        aria-label="first page"
      >
        {theme.direction === "rtl" ? (
          <FontAwesomeIcon icon={faAngleDoubleRight} />
        ) : (
          <FontAwesomeIcon icon={faAngleDoubleLeft} />
        )}
      </IconButton>
      <IconButton
        onClick={handleBackButtonClick}
        disabled={page === 0}
        aria-label="previous page"
      >
        {theme.direction === "rtl" ? (
          <FontAwesomeIcon icon={faAngleRight} />
        ) : (
          <FontAwesomeIcon icon={faAngleLeft} />
        )}
      </IconButton>
      <IconButton
        onClick={handleNextButtonClick}
        disabled={page >= Math.ceil(count / rowsPerPage) - 1}
        aria-label="next page"
      >
        {theme.direction === "rtl" ? (
          <FontAwesomeIcon icon={faAngleLeft} />
        ) : (
          <FontAwesomeIcon icon={faAngleRight} />
        )}
      </IconButton>
      <IconButton
        onClick={handleLastPageButtonClick}
        disabled={page >= Math.ceil(count / rowsPerPage) - 1}
        aria-label="last page"
      >
        {theme.direction === "rtl" ? (
          <FontAwesomeIcon icon={faAngleDoubleLeft} />
        ) : (
          <FontAwesomeIcon icon={faAngleDoubleRight} />
        )}
      </IconButton>
    </div>
  );
}

export const NodeSearchPage: React.FunctionComponent<{}> = ({}) => {
  const searchTextInputRef = React.useRef<HTMLInputElement>();

  const [searchText, setSearchText] = React.useState<string>("");
  const [matchingNodesPage, setMatchingNodesPage] = React.useState<number>(0);
  const [matchingNodesQueryLimit, setMatchingNodesQueryLimit] = React.useState<
    number
  >(10);

  const {data: matchingNodesData} = useQuery<MatchingNodesQuery>(
    matchingNodesQuery,
    {
      variables: {
        limit: matchingNodesQueryLimit,
        offset: matchingNodesPage,
        text: searchText,
      },
      skip: searchText.length === 0,
    }
  );
  const {data: matchingNodesCountData} = useQuery<MatchingNodesCountQuery>(
    matchingNodesCountQuery,
    {
      variables: {text: searchText},
      skip: searchText.length === 0,
    }
  );
  const matchingNodes = matchingNodesData?.matchingNodes;
  const matchingNodesCount = matchingNodesCountData?.matchingNodesCount;

  const onSearchTextInputEnter = () => {
    setSearchText(searchTextInputRef.current!.value);
  };

  const onTableChangePage = (
    event: React.MouseEvent<HTMLButtonElement> | null,
    newPage: number
  ) => {
    setMatchingNodesPage(newPage);
  };

  const onTableChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setMatchingNodesQueryLimit(+event.target.value);
    setMatchingNodesPage(0);
  };

  return (
    <Frame>
      <Grid container spacing={3}>
        <Grid item xs={12} data-cy="searchContainer">
          <Typography variant="body1">
            Searching <span>all data sources</span>
          </Typography>
          <Paper variant="outlined" square>
            <InputBase
              inputProps={{ref: searchTextInputRef, 'data-cy': 'searchTextInput'}}
              fullWidth
              startAdornment={
                <InputAdornment position="end" style={{marginRight: "8px"}}>
                  <FontAwesomeIcon icon={faSearch} />
                </InputAdornment>
              }
              onKeyDown={(event: React.KeyboardEvent<HTMLInputElement>) => {
                if (event.which === 13) {
                  onSearchTextInputEnter();
                }
              }}
            ></InputBase>
          </Paper>
          <Button>
            <FontAwesomeIcon icon={faFilter} /> &nbsp;Filters
          </Button>
        </Grid>
        <Grid item xs={8} data-cy="visualizationContainer">
          {matchingNodes && matchingNodesCount && (
            <React.Fragment>
              <Typography variant="body1">
                {matchingNodesCount} results for "
                {searchTextInputRef.current!.value}"
              </Typography>
              <TableContainer component={Paper}>
                <Table data-cy="matchingNodesTable">
                  <TableHead>
                    <TableRow>
                      <TableCell></TableCell>
                      <TableCell>Label</TableCell>
                      <TableCell>Aliases</TableCell>
                      <TableCell>DataSource</TableCell>
                      <TableCell>Other</TableCell>
                      <TableCell>Pos</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {matchingNodes.map((node, index) => (
                      <TableRow key={node.id}>
                        <TableCell>
                          {matchingNodesPage * matchingNodesQueryLimit +
                            index +
                            1}
                        </TableCell>
                        <TableCell>{node.label}</TableCell>
                        <TableCell>{node.aliases}</TableCell>
                        <TableCell>{node.datasource}</TableCell>
                        <TableCell>{node.other}</TableCell>
                        <TableCell>{node.pos}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                  <TableFooter>
                    <TablePagination
                      rowsPerPage={matchingNodesQueryLimit}
                      count={matchingNodesCount}
                      page={matchingNodesPage}
                      onChangePage={onTableChangePage}
                      onChangeRowsPerPage={onTableChangeRowsPerPage}
                      ActionsComponent={TablePaginationActions}
                    />
                  </TableFooter>
                </Table>
              </TableContainer>
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
