import {Page} from "./Page";

export class NodePage extends Page {
  constructor(private readonly nodeId: string) {
    super();
  }

  readonly relativeUrl = "/node/" + encodeURI(this.nodeId);
}
