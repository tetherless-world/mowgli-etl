import {RandomNodePage} from "../support/page_files/RandomNodePage";

context("Random node page", () => {
  const page = new RandomNodePage();

  beforeEach(() => page.visit());

  it("should immediately redirect to a node page", () => {
    cy.url().should("contains", Cypress.config().baseUrl + "/node/");
  });
});
