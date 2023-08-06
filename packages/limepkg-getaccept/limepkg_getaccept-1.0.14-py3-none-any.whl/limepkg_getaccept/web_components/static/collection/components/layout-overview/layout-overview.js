import { Component, h, Prop, State } from '@stencil/core';
export class LayoutOverview {
    constructor() {
        this.documents = [];
    }
    render() {
        return [
            h("div", { class: "main-layout" },
                h("div", { class: "send-new-document-container" },
                    h("h3", null, "Send new document"),
                    h("div", { class: "send-new-document-buttons" },
                        h("send-new-document-button", { isSigning: true }),
                        h("send-new-document-button", { isSigning: false }))),
                h("div", { class: "related-documents" },
                    h("h3", null, "Related documents"),
                    this.isLoadingDocuments ? (h("ga-loader", null)) : (h("document-list", { documents: this.documents })))),
        ];
    }
    static get is() { return "layout-overview"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["layout-overview.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["layout-overview.css"]
    }; }
    static get properties() { return {
        "sentDocuments": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "IDocument",
                "resolved": "IDocument",
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
            }
        },
        "platform": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "LimeWebComponentPlatform",
                "resolved": "LimeWebComponentPlatform",
                "references": {
                    "LimeWebComponentPlatform": {
                        "location": "import",
                        "path": "@limetech/lime-web-components-interfaces"
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
        "externalId": {
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
            "attribute": "external-id",
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
        },
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
    static get states() { return {
        "isLoadingDocuments": {}
    }; }
}
