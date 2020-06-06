import {NodeSearchResultsPage} from "../support/page_files/NodeSearchResultsPage";
import {NodePage} from "../support/page_files/NodePage";
import {HomePage} from "../support/page_files/HomePage";

context("Navigate to test NodePage from HomePage using search", () => {
  const homePage = new HomePage();

  beforeEach(() => {
    homePage.visit();

    homePage.search.get().type("Test node 0");
  });

  afterEach(() => {
    const nodePage = new NodePage("gui_test_data:0");

    nodePage.assertLoaded();
  });

  it("Use search suggestions to reach node page", () => {
    homePage.search.suggestion(0).get().click();
  });

  it("Use all results to reach node page", () => {
    homePage.search.enter();

    const nodeSearchResultsPage = new NodeSearchResultsPage("Test node 0");

    nodeSearchResultsPage.assertLoaded();

    nodeSearchResultsPage.visualizationContainer.contains(
      '1000 results for "Test node 0"'
    );

    nodeSearchResultsPage.nodeResultsTable.row(0).nodeLink.click();
  });
});
