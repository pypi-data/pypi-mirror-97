import { Component, h, Prop, Event } from '@stencil/core';
import { EnumViews } from '../../models/EnumViews';
export class Root {
    constructor() {
        this.changeViewHandler = this.changeViewHandler.bind(this);
    }
    buttonData() {
        if (this.isSigning) {
            return {
                label: 'Document for signing',
                icon: 'edit',
                description: 'Used for signing sales related documents.',
                buttonText: 'For signing',
            };
        }
        return {
            label: 'Document for tracking',
            icon: 'search',
            description: 'Used when no signing is required.',
            buttonText: 'For tracking',
        };
    }
    render() {
        let buttonContainer = 'new-document-button-container';
        buttonContainer += !this.isSigning ? ' tracking' : '';
        const { icon, label, buttonText, description } = this.buttonData();
        return [
            h("div", { class: buttonContainer },
                h("h4", null, label),
                h("limel-icon", { class: "new-document-icon", name: icon, size: "large" }),
                h("limel-button", { primary: true, label: buttonText, onClick: this.changeViewHandler }),
                h("p", null, description)),
        ];
    }
    changeViewHandler() {
        this.changeView.emit(EnumViews.recipient);
        this.setDocumentType.emit(this.isSigning);
    }
    static get is() { return "send-new-document-button"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["send-new-document-button.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["send-new-document-button.css"]
    }; }
    static get properties() { return {
        "isSigning": {
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
            "attribute": "is-signing",
            "reflect": false
        }
    }; }
    static get events() { return [{
            "method": "changeView",
            "name": "changeView",
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
            "method": "setDocumentType",
            "name": "setDocumentType",
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
