class NodeSearchSuggestionLink {
  constructor(
    private readonly index: number,
    private readonly parentSelector: string
  ) {}

  get() {
    return cy.get(this.parentSelector).find("ul>li>a").eq(this.index);
  }
}

export class NodeSearchInput {
  static readonly componentSelector = "[data-cy=searchTextInput]";
  public readonly selector: string;

  constructor(private readonly parentSelector: string) {
    this.selector =
      this.parentSelector + " " + NodeSearchInput.componentSelector;
  }

  get() {
    return cy.get(this.selector);
  }

  enter() {
    return this.get().type("{enter}");
  }

  suggestion(index: number) {
    return new NodeSearchSuggestionLink(index, this.parentSelector);
  }

  selectDatasource(label: string) {
    cy.get(this.parentSelector + " [data-cy=datasourceSelect]").click();

    cy.get("[data-cy=datasourceSelectMenuItem]").contains(label).click();
  }

  get selectedDatasource() {
    return cy.get(
      this.parentSelector + " [data-cy=datasourceSelect] [data-cy=value]"
    );
  }
}
