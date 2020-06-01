import * as React from "react";
import {makeStyles} from "@material-ui/core";
import {Hrefs} from "../../Hrefs";

const useStyles = makeStyles((theme) => ({
  footerParagraph: {
    textAlign: "center",
  },
}));

export const Footer: React.FunctionComponent = () => {
  const classes = useStyles();
  return (
    <footer>
      <p className={classes.footerParagraph}>
        This work is supported by the{" "}
        <a href="https://www.darpa.mil/program/machine-common-sense">
          DARPA Machine Common Sense (MCS)
        </a>{" "}
        program.
      </p>
      <p className={classes.footerParagraph}>
        <a href={Hrefs.contact}>Contact</a>&nbsp;|&nbsp;
        <a href={Hrefs.gitHub}>GitHub</a>
      </p>
    </footer>
  );
};
