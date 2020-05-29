import {Page} from "./Page";

class EdgeList {
  constructor(private readonly selector: string) {}

  get edges() {
    return cy.get(this.selector + " [data-cy=edge]");
  }

  get title() {
    return cy.get(this.selector + " [data-cy=edge-list-title]");
  }
}

export class NodePage extends Page {
  constructor(private readonly nodeId: string) {
    super();
  }

  get datasource() {
    return cy.get(this.frame.selector + " [data-cy=node-datasource]");
  }

  edgeList(predicate: string) {
    return new EdgeList(
      this.frame.selector + ' [data-cy="' + predicate + '-edges"]'
    );
  }

  get nodeTitle() {
    return cy.get(this.frame.selector + " [data-cy=node-title]");
  }

  readonly relativeUrl = "/node/" + encodeURI(this.nodeId);
}
