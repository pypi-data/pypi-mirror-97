import { Component, h, Prop } from '@stencil/core';
export class EmptyState {
    constructor() {
        this.icon = 'nothing_found';
    }
    render() {
        return (h("div", { class: "empty-state" },
            h("limel-icon", { name: this.icon }),
            h("p", null, this.text)));
    }
    static get is() { return "empty-state"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["empty-state.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["empty-state.css"]
    }; }
    static get properties() { return {
        "text": {
            "type": "string",
            "mutable": false,
            "complexType": {
                "original": "string",
                "resolved": "string",
                "references": {}
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": ""
            },
            "attribute": "text",
            "reflect": false
        },
        "icon": {
            "type": "string",
            "mutable": false,
            "complexType": {
                "original": "string",
                "resolved": "string",
                "references": {}
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": ""
            },
            "attribute": "icon",
            "reflect": false,
            "defaultValue": "'nothing_found'"
        }
    }; }
}
