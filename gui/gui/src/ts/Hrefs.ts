export class Hrefs {
  static node(id: string) {
    return "/node/" + encodeURI(id);
  }

  static get nodeSearch() {
    return "/";
  }
}
