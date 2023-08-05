import { Component, h, State, Event, Prop } from '@stencil/core';
export class CreateEmail {
    constructor() {
        this.emailSubject = '';
        this.emailMessage = '';
        this.handleChangeEmailSubject = this.handleChangeEmailSubject.bind(this);
        this.handleChangeEmailMessage = this.handleChangeEmailMessage.bind(this);
    }
    componentWillLoad() {
        this.emailSubject = this.document.email_send_subject;
        this.emailMessage = this.document.email_send_message;
    }
    render() {
        return [
            h("div", null,
                h("h3", null, "Write your email"),
                h("limel-input-field", { label: "Subject", value: this.emailSubject, onChange: this.handleChangeEmailSubject }),
                h("span", { class: "send-document-email-subject" }, "Email"),
                h("textarea", { class: "send-document-email", rows: 9, value: this.emailMessage, onChange: this.handleChangeEmailMessage })),
        ];
    }
    handleChangeEmailSubject(event) {
        this.emailSubject = event.detail;
        this.setEmailSubject.emit(event.detail);
    }
    handleChangeEmailMessage(event) {
        this.setEmailMessage.emit(event.target.value);
    }
    static get is() { return "create-email"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["create-email.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["create-email.css"]
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
    static get states() { return {
        "emailSubject": {},
        "emailMessage": {}
    }; }
    static get events() { return [{
            "method": "setEmailSubject",
            "name": "setEmailSubject",
            "bubbles": true,
            "cancelable": true,
            "composed": true,
            "docs": {
                "tags": [],
                "text": ""
            },
            "complexType": {
                "original": "any",
                "resolved": "any",
                "references": {}
            }
        }, {
            "method": "setEmailMessage",
            "name": "setEmailMessage",
            "bubbles": true,
            "cancelable": true,
            "composed": true,
            "docs": {
                "tags": [],
                "text": ""
            },
            "complexType": {
                "original": "any",
                "resolved": "any",
                "references": {}
            }
        }]; }
}
