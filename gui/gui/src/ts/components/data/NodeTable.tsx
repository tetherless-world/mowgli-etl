import * as React from "react";

import {
  Paper,
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
  Link,
} from "@material-ui/core";

import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {
  faAngleLeft,
  faAngleRight,
  faAngleDoubleLeft,
  faAngleDoubleRight,
} from "@fortawesome/free-solid-svg-icons";

import {Node} from "models/Node";
import {Hrefs} from "../../Hrefs";

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

const TablePaginationActions = (props: TablePaginationActionsProps) => {
  const classes = TablePaginationActionsUseStyles();
  const theme = useTheme();
  const {count, page, rowsPerPage, onChangePage} = props;

  return (
    <div className={classes.root}>
      <IconButton
        onClick={(event) => onChangePage(event, 0)}
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
        onClick={(event) => onChangePage(event, page - 1)}
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
        onClick={(event) => onChangePage(event, page + 1)}
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
        onClick={(event) =>
          onChangePage(event, Math.max(0, Math.ceil(count / rowsPerPage) - 1))
        }
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
};

const showListAsColumn = (list: string[]) =>
  list.map((item) => (
    <React.Fragment>
      {item}
      <br />
    </React.Fragment>
  ));

export const NodeTable: React.FunctionComponent<{
  nodes: Node[];
  rowsPerPage: number;
  count: number;
  page: number;
  onChangePage: (newPage: number) => void;
  onChangeRowsPerPage: (newRowsPerPage: number) => void;
}> = ({nodes, rowsPerPage, count, page, onChangePage, onChangeRowsPerPage}) => {
  return (
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
          {nodes.map((node, index) => (
            <TableRow key={node.id}>
              <TableCell>{page * rowsPerPage + index + 1}</TableCell>
              <TableCell>
                <Link href={Hrefs.node(node.id)}>{node.label}</Link>
              </TableCell>
              <TableCell>
                {node.aliases && showListAsColumn(node.aliases)}
              </TableCell>
              <TableCell>
                {node.datasource &&
                  showListAsColumn(node.datasource.split(","))}
              </TableCell>
              <TableCell>{node.other}</TableCell>
              <TableCell>
                {node.pos && showListAsColumn(node.pos.split(","))}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
        <TableFooter>
          <TablePagination
            rowsPerPage={rowsPerPage}
            count={count}
            page={page}
            onChangePage={(_, newPage) => onChangePage(newPage)}
            onChangeRowsPerPage={(event) =>
              onChangeRowsPerPage(+event.target.value)
            }
            ActionsComponent={TablePaginationActions}
          />
        </TableFooter>
      </Table>
    </TableContainer>
  );
};
