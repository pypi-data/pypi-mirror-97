'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-60d4a812.js');

const emptyStateCss = ".empty-state{margin-top:1.5rem;font-style:italic;text-align:center;opacity:0.8}.empty-state limel-icon{width:3rem;height:3rem}";

const EmptyState = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.icon = 'nothing_found';
    }
    render() {
        return (index.h("div", { class: "empty-state" }, index.h("limel-icon", { name: this.icon }), index.h("p", null, this.text)));
    }
};
EmptyState.style = emptyStateCss;

exports.empty_state = EmptyState;
