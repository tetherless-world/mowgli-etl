class NodeSearchPage {
  visit() {
    cy.visit("/");
    return this;
  }

  getSearchContainer() {
    return cy.get("[data-cy=searchContainer]");
  }

  getSearchTextInput() {
    return cy.get("[data-cy=searchTextInput]");
  }

  getVisualizationContainer() {
    return cy.get("[data-cy=visualizationContainer]");
  }

  getMatchingNodesTable() {
    return cy.get("[data-cy=matchingNodesTable]");
  }

  search(text: string) {
    const field = this.getSearchTextInput();
    field.clear();
    field.type(text + "{enter}");
    return this;
  }
}

export {NodeSearchPage};

export default new NodeSearchPage();
