const configBase = require("@tetherless-world/twxplore-base/webpack.config.base");
const configDevServer = require("@tetherless-world/twxplore-base/webpack.config.devServer");
const merge = require("webpack-merge");
const path = require("path");

// variables
const distPath = path.join(__dirname, "dist");

// plugins
const CopyWebpackPlugin = require("copy-webpack-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = function (env, argv) {
  return merge(configBase(env, argv), configDevServer(distPath), {
    context: path.join(__dirname, "src"),
    entry: {
      "mowgli-gui": "./ts/main.tsx",
    },
    output: {
      path: distPath,
      filename: "js/[name].js",
      publicPath: "",
    },
    plugins: [
      new CopyWebpackPlugin([
        "robots.txt",
      ]),
      new HtmlWebpackPlugin({
        hash: true,
        template: "index.html",
      }),
    ],
  });
};
