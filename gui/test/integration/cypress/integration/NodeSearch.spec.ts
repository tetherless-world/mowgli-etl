import {NodeSearchResultsPage} from "../support/page_files/NodeSearchResultsPage";
import {NodePage} from "../support/page_files/NodePage";
import {HomePage} from "../support/page_files/HomePage";

context("Navigate to chicken NodePage from HomePage using search", () => {
  const homePage = new HomePage();

  beforeEach(() => {
    homePage.visit();

    homePage.search.get().type("chicken");
  });

  afterEach(() => {
    const nodePage = new NodePage("foodon:03411457");

    nodePage.assertLoaded();
  });

  it("Use search suggestions to reach node page", () => {
    homePage.search.suggestion(0).get().click();
  });

  it("Use all results to reach node page", () => {
    homePage.search.enter();

    const nodeSearchResultsPage = new NodeSearchResultsPage("chicken");

    nodeSearchResultsPage.assertLoaded();

    nodeSearchResultsPage.visualizationContainer.contains(
      '107 results for "chicken"'
    );

    nodeSearchResultsPage.nodeResultsTable.row(0).nodeLink.click();
  });
});
