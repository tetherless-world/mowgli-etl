import NodeSearchPage from "../support/page_files/NodeSearch.page";

context("Node Search Page", () => {
  beforeEach(() => {
    NodeSearchPage.visit();
  });

  it("Table should show after search", () => {
    NodeSearchPage.getVisualizationContainer()
      .children()
      .should("have.length", 0);

    NodeSearchPage.search("apples");

    NodeSearchPage.getVisualizationContainer()
      .children()
      .should("have.length.greaterThan", 0);

    NodeSearchPage.getMatchingNodesTable();
  });
});
