import {NodeSearchResultsPage} from "../support/page_files/NodeSearchResultsPage";
import {NodePage} from "../support/page_files/NodePage";

context("Basic node search", () => {
  it("Show results after search and redirect to node page on node click", () => {
    const nodeSearchResultsPage = new NodeSearchResultsPage();

    nodeSearchResultsPage.visit();

    nodeSearchResultsPage.navbar.search("chicken");

    nodeSearchResultsPage
      .getVisualizationContainer()
      .contains('107 results for "chicken"');

    nodeSearchResultsPage.getNodeResultsTable();

    nodeSearchResultsPage.clickNodeLinkByResultIndex(0);

    const nodePage = new NodePage("foodon:03411457");

    nodePage.assertLoaded();
  });
});
