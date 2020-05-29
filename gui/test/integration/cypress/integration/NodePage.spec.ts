import {NodePage} from "../support/page_files/NodePage";

context("Node page", () => {
  const page = new NodePage("foodon:03411457");

  beforeEach(() => page.visit());

  it("should have the node label in its card title", () => {
    page.nodeTitle.should("have.text", "chicken");
  });

  it("should show edges by predicate", () => {
    page.edgeList("/r/IsA").edges.contains("poultry or game bird");
  });

  it("should show the node datasource", () => {
    page.datasource.should("have.text", "foodon");
  });
});
