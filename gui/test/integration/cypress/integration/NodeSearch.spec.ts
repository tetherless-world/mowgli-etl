import {NodeSearchResultsPage} from "../support/page_files/NodeSearchResultsPage";
import {NodePage} from "../support/page_files/NodePage";

context("Basic node search", () => {
  it("Show results after search and redirect to node page on node click", () => {
    const nodeSearchResultsPage = new NodeSearchResultsPage();

    nodeSearchResultsPage.visit();

    nodeSearchResultsPage.frame.navbar.search("chicken");

    nodeSearchResultsPage.visualizationContainer.contains(
      '107 results for "chicken"'
    );

    nodeSearchResultsPage.nodeResultsTable.row(0).nodeLink.click();

    const nodePage = new NodePage("foodon:03411457");

    nodePage.assertLoaded();
  });
});
