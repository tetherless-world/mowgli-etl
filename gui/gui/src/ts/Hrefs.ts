import * as qs from "qs";

export class Hrefs {
  static get contact() {
    return "mailto:gordom6@rpi.edu";
  }

  static get gitHub() {
    return "https://github.com/tetherless-world/mowgli";
  }

  static node(id: string) {
    return "/node/" + encodeURI(id);
  }

  static nodeSearch(kwds?: {text: string}) {
    return (
      "/node/search" + (kwds ? qs.stringify(kwds, {addQueryPrefix: true}) : "")
    );
  }

  static get home() {
    return "/";
  }
}
