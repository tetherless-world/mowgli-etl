class NodeSearchSuggestionLink {
  constructor(
    private readonly index: number,
    private readonly searchSuggestions: NodeSearchSuggestions
  ) {}

  get() {
    return this.searchSuggestions.get().find("ul>a").eq(this.index);
  }

  click() {
    this.get().click();

    return this;
  }
}

class NodeSearchAllResultsLink {
  constructor(private readonly searchSuggestions: NodeSearchSuggestions) {}

  get() {
    return this.searchSuggestions.get().find("ul>a:last-child");
  }

  click() {
    this.get().click();

    return this;
  }
}

export class NodeSearchSuggestions {
  // The component `div` is actually created in the root component
  // so it has 'no parent elements'
  readonly selector: string = "[data-cy=nodeSearchSuggestions]";

  get() {
    return cy.get(this.selector);
  }

  assertNoResults() {
    this.get().find("ul").children().should("have.length", 1);
    this.get().find("ul>li").should("have.text", "No Results");

    return this;
  }

  suggestion(index: number) {
    return new NodeSearchSuggestionLink(index, this);
  }

  clickSuggestion(index: number) {
    return this.suggestion(index).click();
  }

  get allResults() {
    return new NodeSearchAllResultsLink(this);
  }

  clickAllResults() {
    return this.allResults.click();
  }
}

export class NodeSearchInput {
  private readonly componentSelector = "[data-cy=searchTextInput]";
  public readonly selector: string;

  constructor(parentSelector: string) {
    this.selector = parentSelector + " " + this.componentSelector;
  }

  get() {
    return cy.get(this.selector);
  }

  get autocomplete() {
    return new NodeSearchSuggestions();
  }

  clear() {
    this.get().clear();

    return this;
  }

  type(text: string) {
    this.get().type(text);

    return this;
  }

  enter() {
    this.get().type("{enter}");

    return this;
  }
}
