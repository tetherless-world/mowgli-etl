import {Frame} from "./Frame";

export class NodeSearchResultsPage extends Frame {
  visit() {
    cy.visit("/");
    return this;
  }

  getVisualizationContainer() {
    return cy.get("[data-cy=visualizationContainer]");
  }

  getNodeResultsTable() {
    return cy.get("[data-cy=matchingNodesTable]");
  }

  getNodeResultsTableRow(index: number) {
    return this.getNodeResultsTable().find("tbody>tr").eq(index);
  }

  /**
   * Clicks on link for node in search results table
   * @param index Starts at 0
   */
  clickNodeLinkByResultIndex(index: number) {
    this.getNodeResultsTableRow(index).find("a").click();

    return this;
  }
}
