import { Component, h } from '@stencil/core';
export class GALoader {
    render() {
        return (h("limel-flex-container", { justify: "center" },
            h("limel-spinner", null)));
    }
    static get is() { return "ga-loader"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["ga-loader.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["ga-loader.css"]
    }; }
}
