import {NodeSearchResultsPage} from "../support/page_files/NodeSearchResultsPage";
import {NodePage} from "../support/page_files/NodePage";
import {HomePage} from "../support/page_files/HomePage";

context("Basic node search", () => {
  it("Show results after search and redirect to node page on node click", () => {
    const homePage = new HomePage();

    homePage.visit();

    homePage.search("chicken");

    const nodeSearchResultsPage = new NodeSearchResultsPage("chicken");

    nodeSearchResultsPage.assertLoaded();

    nodeSearchResultsPage.visualizationContainer.contains(
      '107 results for "chicken"'
    );

    nodeSearchResultsPage.nodeResultsTable.row(0).nodeLink.click();

    const nodePage = new NodePage("foodon:03304139");

    nodePage.assertLoaded();
  });
});
