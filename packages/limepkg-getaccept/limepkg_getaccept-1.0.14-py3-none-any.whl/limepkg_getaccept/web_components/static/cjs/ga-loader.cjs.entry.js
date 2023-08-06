'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-60d4a812.js');

const gaLoaderCss = "limel-spinner{margin:1rem 0;color:#f49132}";

const GALoader = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
    }
    render() {
        return (index.h("limel-flex-container", { justify: "center" }, index.h("limel-spinner", null)));
    }
};
GALoader.style = gaLoaderCss;

exports.ga_loader = GALoader;
