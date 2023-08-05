import { Component, h, Prop } from '@stencil/core';
export class TemplatePreview {
    constructor() {
        this.getThumbUrl = this.getThumbUrl.bind(this);
    }
    getThumbUrl() {
        const path = `${this.session.entity_id}/${this.template.value}`;
        return `getaccept/preview_proxy/${path}`;
    }
    render() {
        if (!this.template || this.isLoading) {
            return [];
        }
        return (h("div", { class: "page-info-container" },
            h("img", { class: "page-thumb", src: this.getThumbUrl() })));
    }
    static get is() { return "template-preview"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["template-preview.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["template-preview.css"]
    }; }
    static get properties() { return {
        "template": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "IListItem",
                "resolved": "IListItem",
                "references": {
                    "IListItem": {
                        "location": "import",
                        "path": "../../types/ListItem"
                    }
                }
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": ""
            }
        },
        "isLoading": {
            "type": "boolean",
            "mutable": false,
            "complexType": {
                "original": "boolean",
                "resolved": "boolean",
                "references": {}
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": ""
            },
            "attribute": "is-loading",
            "reflect": false
        },
        "session": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "ISession",
                "resolved": "ISession",
                "references": {
                    "ISession": {
                        "location": "import",
                        "path": "../../types/Session"
                    }
                }
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": ""
            }
        }
    }; }
}
