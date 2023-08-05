import { r as registerInstance, c as createEvent, h } from './index-570406ba.js';
var recipientItemAddedCss = ".recipient-list-item{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;padding:0.5rem;cursor:pointer;border-bottom:1px solid #ccc}.recipient-list-item:hover{background-color:#f5f5f5}.recipient-list-item .recipient-icon{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;margin-right:1rem;padding:0.5em;border-radius:50%;background-color:#5b9bd1}.recipient-list-item .recipient-info-container{display:-ms-flexbox;display:flex;-ms-flex-direction:column;flex-direction:column;-ms-flex-positive:2;flex-grow:2;font-size:0.7rem}.recipient-list-item .recipient-info-container .recipient-info-contact-data{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap;overflow:hidden}.recipient-list-item .recipient-role-container{padding:0.5rem 1rem}.recipient-list-item .recipient-role-container .recipient-role-list{padding:0.5rem;border:none;background-color:transparent;outline:none;color:#212121}.recipient-list-item .recipient-remove-button{display:-ms-flexbox;display:flex;color:#f88987}";
var RecipientItemAdded = /** @class */ (function () {
    function RecipientItemAdded(hostRef) {
        registerInstance(this, hostRef);
        this.changeRecipientRole = createEvent(this, "changeRecipientRole", 7);
        this.removeRecipient = createEvent(this, "removeRecipient", 7);
        this.roles = [];
        this.handleChangeRole = this.handleChangeRole.bind(this);
        this.handleRemoveRecipient = this.handleRemoveRecipient.bind(this);
        this.selectedRole = this.selectedRole.bind(this);
    }
    RecipientItemAdded.prototype.componentWillLoad = function () {
        this.addRecipientRoles();
    };
    RecipientItemAdded.prototype.addRecipientRoles = function () {
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
    };
    RecipientItemAdded.prototype.render = function () {
        var _this = this;
        var _a = this.recipient, name = _a.name, email = _a.email;
        return (h("li", { class: "recipient-list-item" }, h("div", { class: "recipient-info-container" }, h("span", null, name), h("div", { class: "recipient-info-contact-data" }, h("span", null, email))), h("div", { class: "recipient-role-container" }, h("select", { class: "recipient-role-list", onInput: function (event) { return _this.handleChangeRole(event); } }, this.roles.map(function (role) {
            return (h("option", { value: role.value, selected: _this.selectedRole(role) }, role.label));
        }))), h("div", { class: "recipient-remove-button", onClick: this.handleRemoveRecipient }, h("limel-icon", { name: "trash", size: "small" }))));
    };
    RecipientItemAdded.prototype.handleChangeRole = function (event) {
        this.recipient.role = event.target.value;
        this.changeRecipientRole.emit(this.recipient);
    };
    RecipientItemAdded.prototype.handleRemoveRecipient = function () {
        this.removeRecipient.emit(this.recipient);
    };
    RecipientItemAdded.prototype.selectedRole = function (role) {
        return this.recipient.role === role.value;
    };
    return RecipientItemAdded;
}());
RecipientItemAdded.style = recipientItemAddedCss;
var selectedRecipientListCss = ".recipient-list{list-style-type:none;padding:0;margin:0}";
var SelectedRecipientList = /** @class */ (function () {
    function SelectedRecipientList(hostRef) {
        registerInstance(this, hostRef);
    }
    SelectedRecipientList.prototype.render = function () {
        var _this = this;
        if (!this.recipients.length) {
            return (h("empty-state", { icon: "user", text: "No recipients added. Find and add recipients to the left!" }));
        }
        return (h("ul", { class: "recipient-list" }, this.recipients.map(function (selectedRecipient) {
            return (h("recipient-item-added", { recipient: selectedRecipient, isSigning: _this.document.is_signing }));
        })));
    };
    return SelectedRecipientList;
}());
SelectedRecipientList.style = selectedRecipientListCss;
export { RecipientItemAdded as recipient_item_added, SelectedRecipientList as selected_recipient_list };
