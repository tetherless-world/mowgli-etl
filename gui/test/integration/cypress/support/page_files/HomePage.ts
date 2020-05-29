import {Page} from "./Page";

export class HomePage extends Page {
  get searchInput() {
    return cy.get("[data-cy=searchTextInput]");
  }

  search(text: string) {
    const field = this.searchInput;
    field.clear();
    field.type(text + "{enter}");
    return this;
  }

  readonly relativeUrl: string = "/";
}
