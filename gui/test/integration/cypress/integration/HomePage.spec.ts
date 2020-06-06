import {HomePage} from "../support/page_files/HomePage";
import {TestData} from "../support/TestData";

context("Home Page", () => {
  const data = new TestData();
  const page = new HomePage();

  beforeEach(() => page.visit());

  it("should show total node and edge counts", () => {
    page.totalNodeCount.should("have.text", `${data.nodeCount} nodes`);
    page.totalEdgeCount.should("have.text", `${data.edgeCount} relationships`);
  });

  it("should show all datasources", () => {
    page.search.selectedDatasource.should("have.text", "All datasources");
  });

  it("should show selected datasource", () => {
    page.search.selectDatasource(data.datasources[0]);

    page.search.selectedDatasource.should("have.text", data.datasources[0]);
  });
});
