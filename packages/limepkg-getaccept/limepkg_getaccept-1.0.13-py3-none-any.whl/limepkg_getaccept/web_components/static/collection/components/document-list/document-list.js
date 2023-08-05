import { Component, h, Prop } from '@stencil/core';
export class DocumentList {
    constructor() {
        this.documents = [];
    }
    render() {
        if (!this.documents.length) {
            return h("empty-state", { text: "No documents were found!" });
        }
        return [
            h("ul", { class: "document-list" }, this.documents.map(document => {
                return h("document-list-item", { document: document });
            })),
        ];
    }
    static get is() { return "document-list"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["document-list.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["document-list.css"]
    }; }
    static get properties() { return {
        "documents": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "IDocument[]",
                "resolved": "IDocument[]",
                "references": {
                    "IDocument": {
                        "location": "import",
                        "path": "../../types/Document"
                    }
                }
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": ""
            },
            "defaultValue": "[]"
        }
    }; }
}
