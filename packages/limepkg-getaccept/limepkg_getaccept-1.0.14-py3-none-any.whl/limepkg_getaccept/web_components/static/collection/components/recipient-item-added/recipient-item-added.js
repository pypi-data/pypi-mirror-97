import { Component, h, Prop, Event } from '@stencil/core';
export class RecipientItemAdded {
    constructor() {
        this.roles = [];
        this.handleChangeRole = this.handleChangeRole.bind(this);
        this.handleRemoveRecipient = this.handleRemoveRecipient.bind(this);
        this.selectedRole = this.selectedRole.bind(this);
    }
    componentWillLoad() {
        this.addRecipientRoles();
    }
    addRecipientRoles() {
        if (this.isSigning) {
            this.roles.push({
                value: 'signer',
                label: 'Signer',
            });
        }
        this.roles.push({
            value: 'cc',
            label: 'Only view',
        }, {
            value: 'approver',
            label: 'Approver',
        });
        if (!this.recipient.role) {
            this.recipient.role = this.roles[0].value;
            this.changeRecipientRole.emit(this.recipient);
        }
    }
    render() {
        const { name, email } = this.recipient;
        return (h("li", { class: "recipient-list-item" },
            h("div", { class: "recipient-info-container" },
                h("span", null, name),
                h("div", { class: "recipient-info-contact-data" },
                    h("span", null, email))),
            h("div", { class: "recipient-role-container" },
                h("select", { class: "recipient-role-list", onInput: event => this.handleChangeRole(event) }, this.roles.map(role => {
                    return (h("option", { value: role.value, selected: this.selectedRole(role) }, role.label));
                }))),
            h("div", { class: "recipient-remove-button", onClick: this.handleRemoveRecipient },
                h("limel-icon", { name: "trash", size: "small" }))));
    }
    handleChangeRole(event) {
        this.recipient.role = event.target.value;
        this.changeRecipientRole.emit(this.recipient);
    }
    handleRemoveRecipient() {
        this.removeRecipient.emit(this.recipient);
    }
    selectedRole(role) {
        return this.recipient.role === role.value;
    }
    static get is() { return "recipient-item-added"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["recipient-item-added.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["recipient-item-added.css"]
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
            "method": "changeRecipientRole",
            "name": "changeRecipientRole",
            "bubbles": true,
            "cancelable": true,
            "composed": true,
            "docs": {
                "tags": [],
                "text": ""
            },
            "complexType": {
                "original": "IRecipient",
                "resolved": "IRecipient",
                "references": {
                    "IRecipient": {
                        "location": "import",
                        "path": "../../types/Recipient"
                    }
                }
            }
        }, {
            "method": "removeRecipient",
            "name": "removeRecipient",
            "bubbles": true,
            "cancelable": true,
            "composed": true,
            "docs": {
                "tags": [],
                "text": ""
            },
            "complexType": {
                "original": "IRecipient",
                "resolved": "IRecipient",
                "references": {
                    "IRecipient": {
                        "location": "import",
                        "path": "../../types/Recipient"
                    }
                }
            }
        }]; }
}
