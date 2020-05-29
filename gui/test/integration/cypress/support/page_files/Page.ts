export abstract class Page {
  get absoluteUrl() {
    return Cypress.config().baseUrl + this.relativeUrl;
  }

  assertLoaded() {
    cy.url().should("eq", this.absoluteUrl);
  }

  readonly frame = {
    navbar: {
      get nodeLabelSearchInput() {
        return cy.get("[data-cy=frame] [data-cy=searchTextInput]");
      },

      search(text: string) {
        const field = this.nodeLabelSearchInput;
        field.clear();
        field.type(text + "{enter}");
        return this;
      },
    },
    selector: "[data-cy=frame]",
  };

  abstract readonly relativeUrl: string;

  visit() {
    cy.visit(this.relativeUrl);
    this.assertLoaded();
  }
}
