const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const devMode = process.env.NODE_ENV !== "production";
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');

class WatchRunPlugin {
	apply(compiler) {
		compiler.hooks.watchRun.tap('WatchRun', (comp) => {
			if (comp.modifiedFiles) {
				const changedFiles = Array.from(comp.modifiedFiles, (file) => `\n  ${file}`).join('');
				console.log('===============================');
				console.log('FILES CHANGED:', changedFiles);
				console.log('===============================');
			}
		});
	}
}

const plugins = [
	new MiniCssExtractPlugin({
		// Options similar to the same options in webpackOptions.output
		// both options are optional
		filename: devMode ? "[name].css" : "[name].[contenthash].css",
		chunkFilename: devMode ? "[id].css" : "[id].[contenthash].css",
	}),
	new WebpackManifestPlugin({}),
	new WatchRunPlugin()
];

module.exports = {
	plugins,
	mode: 'production',
	watchOptions: {
		ignored: path.resolve(__dirname, '..', 'app')
	},
	entry: ['./ts/index.ts', './css/main.css'],
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
			{
				test: /\.tsx?$/,
				use: 'ts-loader',
				exclude: '/node_modules/'
			}
		],
	}
}
