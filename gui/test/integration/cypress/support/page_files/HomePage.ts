import {Page} from "./Page";
import {NodeSearchInput} from "./NodeSearchInput";

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

  get search() {
    return new NodeSearchInput(this.frame.bodySelector);
  }

  readonly relativeUrl: string = "/";
}
