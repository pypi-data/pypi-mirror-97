import { Component, h, Prop } from '@stencil/core';
export class DocumentValidateInfo {
    constructor() {
        this.hasProperty = this.hasProperty.bind(this);
    }
    render() {
        return [
            h("div", { class: "validate-document-success" },
                h("div", { class: "validate-document-summary" },
                    h("h3", null, "Summary"),
                    h("ul", { class: "validate-document-property-list" },
                        h("li", null,
                            h("span", { class: "document-property" }, "Name: "),
                            h("span", null, this.document.name)),
                        h("li", null,
                            h("span", { class: "document-property" }, "Value: "),
                            h("span", null, this.document.value)),
                        h("li", null,
                            h("span", { class: "document-property" },
                                "Document is for signing:",
                                ' '),
                            h("span", null, this.hasProperty(this.document.is_signing))),
                        h("li", null,
                            h("span", { class: "document-property" },
                                "Video is added:",
                                ' '),
                            h("span", null, this.hasProperty(this.document.is_video))),
                        h("li", null,
                            h("span", { class: "document-property" },
                                "Send smart reminders:",
                                ' '),
                            h("span", null, this.hasProperty(this.document.is_reminder_sending))),
                        h("li", null,
                            h("span", { class: "document-property" },
                                "Send link by SMS:",
                                ' '),
                            h("span", null, this.hasProperty(this.document.is_sms_sending))))),
                h("div", { class: "validate-document-recipients" },
                    h("h3", null, "Recipients"),
                    h("ul", { class: "document-recipient-list" }, this.document.recipients.map(recipient => {
                        return (h("recipient-item", { recipient: recipient, showAdd: false }));
                    })))),
        ];
    }
    hasProperty(value) {
        return value ? 'Yes' : 'No';
    }
    static get is() { return "document-validate-info"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["document-validate-info.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["document-validate-info.css"]
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
        }
    }; }
}
