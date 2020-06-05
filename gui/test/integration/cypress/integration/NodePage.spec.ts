import {NodePage} from "../support/page_files/NodePage";

context("Node page", () => {
  const page = new NodePage("gui_test_data:0");

  beforeEach(() => page.visit());

  it("should have the node label in its card title", () => {
    page.nodeTitle.should("have.text", "Test node 0 (r)");
  });

  it("should show edges by predicate", () => {
    page.edgeList("/r/IsA").edges.contains("Test node 776");
  });

  it("should show the node datasource", () => {
    page.datasource.should("have.text", "gui_test_data");
  });
});
