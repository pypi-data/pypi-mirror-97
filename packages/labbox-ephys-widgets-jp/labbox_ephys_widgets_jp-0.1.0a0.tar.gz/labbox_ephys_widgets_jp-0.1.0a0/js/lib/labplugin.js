var plugin = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'labbox-ephys-widgets-jp:plugin',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'labbox-ephys-widgets-jp',
          version: plugin.version,
          exports: plugin
      });
  },
  autoStart: true
};

