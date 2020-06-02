import {RandomNodePage} from "../support/page_files/RandomNodePage";

context("Random node page", () => {
  const page = new RandomNodePage();

  it("should immediately redirect to a node page", () => {
    cy.visit(page.relativeUrl);
    cy.url().should("contains", Cypress.config().baseUrl + "/node/");
  });
});
