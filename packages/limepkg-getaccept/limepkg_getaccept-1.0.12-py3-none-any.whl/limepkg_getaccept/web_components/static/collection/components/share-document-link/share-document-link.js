import { Component, h, Prop } from '@stencil/core';
export class ShareDocumentLink {
    constructor() {
        this.handleCopyLink = this.handleCopyLink.bind(this);
    }
    render() {
        return (h("li", { class: "share-document-list-item" },
            h("div", { class: "recipient-info-container" },
                h("div", { class: "recipient-icon" },
                    h("limel-icon", { name: "user", size: "small" })),
                h("div", { class: "recipient-info" },
                    h("span", { class: "recipient-info-name" }, this.recipient.name),
                    h("span", { class: "recipient-info-role" }, this.recipient.role))),
            h("div", null,
                h("limel-input-field", { label: "Signing link", type: "email", value: this.recipient.document_url, trailingIcon: "copy_link", onAction: this.handleCopyLink }))));
    }
    handleCopyLink() {
        var copyText = document.createElement('textarea');
        copyText.value = this.recipient.document_url;
        document.body.appendChild(copyText);
        copyText.select();
        document.execCommand('copy');
        document.body.removeChild(copyText);
    }
    static get is() { return "share-document-link"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["share-document-link.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["share-document-link.css"]
    }; }
    static get properties() { return {
        "recipient": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "IRecipient",
                "resolved": "IRecipient",
                "references": {
                    "IRecipient": {
                        "location": "import",
                        "path": "../../types/Recipient"
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
