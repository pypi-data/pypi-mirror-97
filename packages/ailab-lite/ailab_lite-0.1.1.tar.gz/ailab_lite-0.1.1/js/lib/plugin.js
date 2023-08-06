import "regenerator-runtime/runtime.js";

var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');


import Vue from 'vue';
import vuetify from "./plugins/vuetify";

import AilabLiteNodeEditor from "./ailab-lite-node-editor.esm.js";

import sklearnBasedSchemas from "./schemas/sklearn_based_schemas.json";
import dfoSchemas from "./schemas/dfo_schemas.json";
import runnableSchemas from "./schemas/runnable_schemas.json";
import rollingaggregationSchema from "./component_schemas/rollingaggregation_schema.json";

import "../styles/css/style.css";

Vue.config.productionTip = false

export class NodeEditorModel extends widgets.DOMWidgetModel {
    defaults() {
      return {
        ...super.defaults(),
        _model_name : 'NodeEditorModel',
        _view_name : 'NodeEditorView',
        _model_module : 'ailab-lite',
        _view_module : 'ailab-lite',
        _model_module_version : '0.1.0',
        _view_module_version : '0.1.0',
        running: false,
        validating: false,
      }
    }
};


export class NodeEditorView extends widgets.DOMWidgetView {
    render() {
        let componentSchemas = [
            ...sklearnBasedSchemas,
            ...dfoSchemas,
            ...runnableSchemas,
            ...rollingaggregationSchema,
          ],
          that = this,
          notebook_name = "";

          if(window.document.getElementsByTagName('body')[0].getAttribute("data-notebook-path")) {
            notebook_name = window.document.getElementsByTagName('body')[0].getAttribute("data-notebook-path");
          } else if(JSON.parse(window.document.getElementById("jupyter-config-data").innerHTML).treePath) {
            notebook_name = JSON.parse(window.document.getElementById("jupyter-config-data").innerHTML).treePath;
          } else {
            notebook_name = "Untitled.ipynb";
          }
          notebook_name = notebook_name.substr(0, notebook_name.lastIndexOf('.'));
          that.model.set("notebook_name", notebook_name);
          that.touch();
          setTimeout(function() {
            new Vue({
              vuetify,
              el: that.el,
              render: (h) =>
                h("v-app", [
                  h(AilabLiteNodeEditor, {
                    props: {
                      vuetify: vuetify,
                      componentSchemas: componentSchemas,
                      datasets: that.model.get("datasets"),
                      workflow: that.model.get("workflow_definition"),
                      widget_: that,
                    },
                  }),
                ]),
            });
          }, 1000);
    }

};
