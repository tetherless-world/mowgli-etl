import {NodeSearchResultsPage} from "../support/page_files/NodeSearchResultsPage";
import {NodePage} from "../support/page_files/NodePage";

context("Basic node search", () => {
  it("Show results after search and redirect to node page on node click", () => {
    const nodeSearchResultsPage = new NodeSearchResultsPage();

    nodeSearchResultsPage.visit();

    nodeSearchResultsPage.navbar.search("oranges");

    nodeSearchResultsPage
      .getVisualizationContainer()
      .contains('results for "oranges"');

    // Increase timeout for first query
    nodeSearchResultsPage.getNodeResultsTable({timeout: 15000});

    nodeSearchResultsPage.clickNodeLinkByResultIndex(0);

    const nodePage = new NodePage("/c/en/oranges/n");

    nodePage.assertLoaded();
  });
});
