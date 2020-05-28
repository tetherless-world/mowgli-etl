import {Page} from "./Page";

class NodeResultsTable {
  get() {
    return cy.get("[data-cy=matchingNodesTable]");
  }

  row(index: number): NodeResultsTableRow {
    return new NodeResultsTableRow(index, this);
  }
}

class NodeResultsTableRow {
  constructor(
    private readonly index: number,
    private readonly table: NodeResultsTable
  ) {}

  get() {
    return this.table.get().find("tbody>tr").eq(this.index);
  }

  readonly nodeLink = new NodeResultsNodeTableRowNodeLink(this);
}

class NodeResultsNodeTableRowNodeLink {
  constructor(private readonly row: NodeResultsTableRow) {}

  click() {
    this.row.get().find("a").click();
  }
}

export class NodeSearchResultsPage extends Page {
  readonly nodeResultsTable = new NodeResultsTable();

  readonly relativeUrl = "/";

  get visualizationContainer() {
    return cy.get("[data-cy=visualizationContainer]");
  }
}
