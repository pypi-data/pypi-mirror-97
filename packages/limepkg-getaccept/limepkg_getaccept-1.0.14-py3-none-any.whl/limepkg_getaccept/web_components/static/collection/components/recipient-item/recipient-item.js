import { Component, h, Prop } from '@stencil/core';
export class RecipientItem {
    constructor() {
        this.showAdd = true;
    }
    render() {
        const { name, email, mobile, limetype, company } = this.recipient;
        const icon = this.getIcon(limetype);
        const recipientList = `recipient-list-item ${this.isDisabled()}`;
        const contactInfoClasses = `recipient-info-contact-data${email ? ' contact--email' : ''}${mobile ? ' contact--phone' : ''}`;
        return (h("li", { class: recipientList },
            h("div", { class: `recipient-icon ${limetype}` },
                h("limel-icon", { name: icon, size: "small" })),
            h("div", { class: "recipient-info-container" },
                h("span", null, name),
                h("div", null,
                    h("span", null, company)),
                h("div", { class: contactInfoClasses },
                    h("span", { class: "recipient-email" }, email),
                    h("span", { class: "recipient-phone" }, mobile))),
            this.renderAddIcon(this.showAdd)));
    }
    renderAddIcon(show) {
        return show ? (h("div", { class: "recipient-add-button" },
            h("limel-icon", { name: "add", size: "medium" }))) : ([]);
    }
    getIcon(limetype) {
        return limetype === 'coworker' ? 'school_director' : 'guest_male';
    }
    isDisabled() {
        return !this.recipient.email && !this.recipient.mobile
            ? 'disabled'
            : '';
    }
    static get is() { return "recipient-item"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["recipient-item.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["recipient-item.css"]
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
        },
        "showAdd": {
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
            "attribute": "show-add",
            "reflect": false,
            "defaultValue": "true"
        }
    }; }
}
