import {Page} from "./Page";
import {NodeSearchInput} from "./NodeSearchBox";

export class HomePage extends Page {
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
