import { Component, h, Prop } from '@stencil/core';
export class DocumentErrorFeedback {
    constructor() {
        this.errorList = [];
    }
    render() {
        return [
            h("div", null,
                h("h3", null, "You need to fix following tasks to send:"),
                h("ul", { class: "document-error-list" }, this.errorList.map((error) => {
                    return h("document-error", { error: error });
                })))
        ];
    }
    static get is() { return "document-error-feedback"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["document-error-feedback.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["document-error-feedback.css"]
    }; }
    static get properties() { return {
        "document": {
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
        "errorList": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "IError[]",
                "resolved": "IError[]",
                "references": {
                    "IError": {
                        "location": "import",
                        "path": "../../types/Error"
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
