import {Frame} from "./Frame";

export class NodePage extends Frame {
  private readonly relativePathName: string;

  constructor(private readonly nodeId: string) {
    super();
    this.relativePathName = "/node/" + encodeURI(this.nodeId);
  }

  visit() {
    cy.visit(this.relativePathName);

    return this.assertLoaded();
  }

  assertLoaded() {
    cy.location().should((location) =>
      expect(location.pathname).to.equal(this.relativePathName)
    );

    return this;
  }
}
