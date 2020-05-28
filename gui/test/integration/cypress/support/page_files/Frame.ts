export abstract class Frame {
  abstract visit(): void;

  public readonly navbar = {
    getNodeLabelSearchInput() {
      return cy.get("[data-cy=searchTextInput]");
    },

    search(text: string) {
      const field = this.getNodeLabelSearchInput();
      field.clear();
      field.type(text + "{enter}");
      return this;
    },
  };
}
