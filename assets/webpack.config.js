const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const devMode = process.env.NODE_ENV !== "production";
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');


const plugins = [
  new MiniCssExtractPlugin({
    // Options similar to the same options in webpackOptions.output
    // both options are optional
    filename: devMode ? "[name].css" : "[name].[contenthash].css",
    chunkFilename: devMode ? "[id].css" : "[id].[contenthash].css",
  }),
  new WebpackManifestPlugin({}),
];

module.exports = {
  plugins,
  mode: 'development',
  entry: ['./js/index.js', './css/main.css'],
  output: {
    path: path.resolve(__dirname, '..', 'app', 'static', 'dist')
  },
  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          "postcss-loader",
        ],
      },
    ],
  }
}
