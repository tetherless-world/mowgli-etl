import {HomePage} from "../support/page_files/HomePage";

context("Home Page", () => {
  const page = new HomePage();

  beforeEach(() => page.visit());

  it("should show total node and edge counts", () => {
    page.totalNodeCount.should("have.text", "10376 nodes");
    page.totalEdgeCount.should("have.text", "10623 relationships");
  });
});
