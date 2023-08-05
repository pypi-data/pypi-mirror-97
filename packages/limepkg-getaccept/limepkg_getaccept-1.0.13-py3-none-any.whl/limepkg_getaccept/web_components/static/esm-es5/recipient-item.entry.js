import { r as registerInstance, h } from './index-570406ba.js';
var recipientItemCss = ".recipient-list-item{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;padding:0.5rem;cursor:pointer;overflow:hidden;border-bottom:1px solid #ccc}.recipient-list-item:hover{background-color:#f5f5f5}.recipient-list-item.disabled{opacity:0.7;filter:grayscale(1);-webkit-filter:grayscale(1)}.recipient-list-item .recipient-icon{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;margin-right:1rem;padding:0.5em;border-radius:50%;background-color:#5b9bd1;color:#fff}.recipient-list-item .recipient-icon.coworker{background-color:#f49132}.recipient-list-item .recipient-info-container{display:-ms-flexbox;display:flex;-ms-flex-direction:column;flex-direction:column;font-size:0.7rem;-ms-flex-positive:2;flex-grow:2}.recipient-list-item .recipient-info-container .recipient-info-contact-data{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap;overflow:hidden}.recipient-list-item .recipient-info-container .recipient-info-contact-data .recipient-phone:empty{display:none}.recipient-list-item .recipient-info-container .recipient-info-contact-data.contact--email .recipient-phone::before{content:\"|\";margin:0 0.5rem}.recipient-list-item .recipient-add-button{color:#f49132}";
var RecipientItem = /** @class */ (function () {
    function RecipientItem(hostRef) {
        registerInstance(this, hostRef);
        this.showAdd = true;
    }
    RecipientItem.prototype.render = function () {
        var _a = this.recipient, name = _a.name, email = _a.email, mobile = _a.mobile, limetype = _a.limetype, company = _a.company;
        var icon = this.getIcon(limetype);
        var recipientList = "recipient-list-item " + this.isDisabled();
        var contactInfoClasses = "recipient-info-contact-data" + (email ? ' contact--email' : '') + (mobile ? ' contact--phone' : '');
        return (h("li", { class: recipientList }, h("div", { class: "recipient-icon " + limetype }, h("limel-icon", { name: icon, size: "small" })), h("div", { class: "recipient-info-container" }, h("span", null, name), h("div", null, h("span", null, company)), h("div", { class: contactInfoClasses }, h("span", { class: "recipient-email" }, email), h("span", { class: "recipient-phone" }, mobile))), this.renderAddIcon(this.showAdd)));
    };
    RecipientItem.prototype.renderAddIcon = function (show) {
        return show ? (h("div", { class: "recipient-add-button" }, h("limel-icon", { name: "add", size: "medium" }))) : ([]);
    };
    RecipientItem.prototype.getIcon = function (limetype) {
        return limetype === 'coworker' ? 'school_director' : 'guest_male';
    };
    RecipientItem.prototype.isDisabled = function () {
        return !this.recipient.email && !this.recipient.mobile
            ? 'disabled'
            : '';
    };
    return RecipientItem;
}());
RecipientItem.style = recipientItemCss;
export { RecipientItem as recipient_item };
