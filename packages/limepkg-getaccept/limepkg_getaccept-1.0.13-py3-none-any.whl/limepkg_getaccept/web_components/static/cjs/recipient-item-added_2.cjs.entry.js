'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-60d4a812.js');

const recipientItemAddedCss = ".recipient-list-item{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;padding:0.5rem;cursor:pointer;border-bottom:1px solid #ccc}.recipient-list-item:hover{background-color:#f5f5f5}.recipient-list-item .recipient-icon{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;margin-right:1rem;padding:0.5em;border-radius:50%;background-color:#5b9bd1}.recipient-list-item .recipient-info-container{display:-ms-flexbox;display:flex;-ms-flex-direction:column;flex-direction:column;-ms-flex-positive:2;flex-grow:2;font-size:0.7rem}.recipient-list-item .recipient-info-container .recipient-info-contact-data{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap;overflow:hidden}.recipient-list-item .recipient-role-container{padding:0.5rem 1rem}.recipient-list-item .recipient-role-container .recipient-role-list{padding:0.5rem;border:none;background-color:transparent;outline:none;color:#212121}.recipient-list-item .recipient-remove-button{display:-ms-flexbox;display:flex;color:#f88987}";

const RecipientItemAdded = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.changeRecipientRole = index.createEvent(this, "changeRecipientRole", 7);
        this.removeRecipient = index.createEvent(this, "removeRecipient", 7);
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
        return (index.h("li", { class: "recipient-list-item" }, index.h("div", { class: "recipient-info-container" }, index.h("span", null, name), index.h("div", { class: "recipient-info-contact-data" }, index.h("span", null, email))), index.h("div", { class: "recipient-role-container" }, index.h("select", { class: "recipient-role-list", onInput: event => this.handleChangeRole(event) }, this.roles.map(role => {
            return (index.h("option", { value: role.value, selected: this.selectedRole(role) }, role.label));
        }))), index.h("div", { class: "recipient-remove-button", onClick: this.handleRemoveRecipient }, index.h("limel-icon", { name: "trash", size: "small" }))));
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
};
RecipientItemAdded.style = recipientItemAddedCss;

const selectedRecipientListCss = ".recipient-list{list-style-type:none;padding:0;margin:0}";

const SelectedRecipientList = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
    }
    render() {
        if (!this.recipients.length) {
            return (index.h("empty-state", { icon: "user", text: "No recipients added. Find and add recipients to the left!" }));
        }
        return (index.h("ul", { class: "recipient-list" }, this.recipients.map(selectedRecipient => {
            return (index.h("recipient-item-added", { recipient: selectedRecipient, isSigning: this.document.is_signing }));
        })));
    }
};
SelectedRecipientList.style = selectedRecipientListCss;

exports.recipient_item_added = RecipientItemAdded;
exports.selected_recipient_list = SelectedRecipientList;
