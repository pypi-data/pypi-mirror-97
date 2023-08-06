var path = require("path");
var version = require("./package.json").version;

// Custom webpack rules are generally the same for all webpack bundles, hence
// stored in a separate local variable.
var rules = [
  {
    test: /\.s(c|a)ss$/,
    use: [
      "vue-style-loader",
      {
        loader: "css-loader",
        options: {
          esModule: false,
        },
      },
      {
        loader: "sass-loader",
        options: {
          implementation: require("sass"),
          sassOptions: {
            fiber: require("fibers"),
            indentedSyntax: true, // optional
          },
        },
      },
    ],
  },
  { test: /\.css$/, use: ["style-loader", "css-loader"] },
];

const externals = [
  "@jupyter-widgets/base"
];

const resolve = {
  alias: {
    vue$: "vue/dist/vue.esm.js",
  },
};

var plugins = [];

module.exports = (env, argv) => {
  var devtool = argv.mode === "development" ? "source-map" : false;
  return [
    {
      // Notebook extension
      //
      // This bundle only contains the part of the JavaScript that is run on
      // load of the notebook. This section generally only performs
      // some configuration for requirejs, and provides the legacy
      // "load_ipython_extension" function which is required for any notebook
      // extension.
      //
      entry: "./lib/extension.js",
      output: {
        filename: "extension.js",
        path: path.resolve(__dirname, "..", "ailab_lite", "nbextension"),
        libraryTarget: "amd",
        publicPath: "", // publicPath is set in extension.js
      },
      plugins,
      externals,
      resolve,
      devtool,
      mode: "production",
      performance: {
        maxEntrypointSize: 1400000,
        maxAssetSize: 1400000,
      },
    },
    {
      // Bundle for the notebook containing the custom widget views and models
      //
      // This bundle contains the implementation for the custom widget views and
      // custom widget.
      // It must be an amd module
      //
      entry: "./lib/index.js",
      output: {
        filename: "index.js",
        path: path.resolve(__dirname, "..", "ailab_lite", "nbextension"),
        libraryTarget: "amd",
        publicPath: "",
      },
      devtool,
      module: {
        rules: rules,
      },
      plugins,
      resolve,
      externals,
      mode: "production",
      performance: {
        maxEntrypointSize: 1400000,
        maxAssetSize: 1400000,
      },
    },
    {
      // Embeddable ailab-lite bundle
      //
      // This bundle is generally almost identical to the notebook bundle
      // containing the custom widget views and models.
      //
      // The only difference is in the configuration of the webpack public path
      // for the static assets.
      //
      // It will be automatically distributed by unpkg to work with the static
      // widget embedder.
      //
      // The target bundle is always `dist/index.js`, which is the path required
      // by the custom widget embedder.
      //
      entry: "./lib/embed.js",
      output: {
        filename: "index.js",
        path: path.resolve(__dirname, "dist"),
        libraryTarget: "amd",
        publicPath: "https://unpkg.com/ailab-lite@" + version + "/dist/",
      },
      devtool,
      module: {
        rules: rules,
      },
      plugins,
      externals,
      resolve,
      mode: "production",
      performance: {
        maxEntrypointSize: 1400000,
        maxAssetSize: 1400000,
      },
    },
  ];
};
