import { Component, h, State, Event } from '@stencil/core';
export class SendDocumentButtonGroup {
    constructor() {
        this.disabled = false;
        this.loading = false;
        this.handleOnClickSendButton = this.handleOnClickSendButton.bind(this);
    }
    render() {
        return [
            h("div", { class: "send-document-button-group" },
                h("limel-button", { label: "Prepare for sendout", primary: true, loading: this.loading, disabled: this.disabled, onClick: this.handleOnClickSendButton })),
        ];
    }
    handleOnClickSendButton() {
        this.validateDocument.emit();
    }
    static get is() { return "send-document-button-group"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["send-document-button-group.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["send-document-button-group.css"]
    }; }
    static get states() { return {
        "disabled": {},
        "loading": {}
    }; }
    static get events() { return [{
            "method": "validateDocument",
            "name": "validateDocument",
            "bubbles": true,
            "cancelable": true,
            "composed": true,
            "docs": {
                "tags": [],
                "text": ""
            },
            "complexType": {
                "original": "boolean",
                "resolved": "boolean",
                "references": {}
            }
        }]; }
}
