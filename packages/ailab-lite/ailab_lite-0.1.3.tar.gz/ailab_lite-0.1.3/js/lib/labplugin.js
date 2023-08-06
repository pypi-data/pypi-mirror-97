var plugin = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'ailab-lite:plugin',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'ailab-lite',
          version: plugin.version,
          exports: plugin
      });
  },
  autoStart: true
};

