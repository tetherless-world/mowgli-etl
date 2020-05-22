import {NodeSearchPage} from "../support/page_files/NodeSearch.page";

context("Node Search Page", () => {
  const page = new NodeSearchPage();

  beforeEach(() => {
    page.visit();
  });

  it("Table should show after search", () => {
    page.getVisualizationContainer().children().should("have.length", 0);

    page.search("apples");

    page
      .getVisualizationContainer()
      .children()
      .should("have.length.greaterThan", 0);

    page.getMatchingNodesTable();
  });
});
