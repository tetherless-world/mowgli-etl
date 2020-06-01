import {Page} from "./Page";

export class HomePage extends Page {
  get searchInput() {
    return cy.get(this.frame.bodySelector + " [data-cy=searchTextInput]");
  }

  get totalNodeCount() {
    return cy.get(this.frame.bodySelector + " [data-cy=totalNodeCount]");
  }

  get totalEdgeCount() {
    return cy.get(this.frame.bodySelector + " [data-cy=totalEdgeCount]");
  }

  search(text: string) {
    const field = this.searchInput;
    field.clear();
    field.type(text + "{enter}");
    return this;
  }

  readonly relativeUrl: string = "/";
}
