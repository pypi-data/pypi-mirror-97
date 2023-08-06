'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-60d4a812.js');

const recipientItemCss = ".recipient-list-item{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;padding:0.5rem;cursor:pointer;overflow:hidden;border-bottom:1px solid #ccc}.recipient-list-item:hover{background-color:#f5f5f5}.recipient-list-item.disabled{opacity:0.7;filter:grayscale(1);-webkit-filter:grayscale(1)}.recipient-list-item .recipient-icon{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;margin-right:1rem;padding:0.5em;border-radius:50%;background-color:#5b9bd1;color:#fff}.recipient-list-item .recipient-icon.coworker{background-color:#f49132}.recipient-list-item .recipient-info-container{display:-ms-flexbox;display:flex;-ms-flex-direction:column;flex-direction:column;font-size:0.7rem;-ms-flex-positive:2;flex-grow:2}.recipient-list-item .recipient-info-container .recipient-info-contact-data{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap;overflow:hidden}.recipient-list-item .recipient-info-container .recipient-info-contact-data .recipient-phone:empty{display:none}.recipient-list-item .recipient-info-container .recipient-info-contact-data.contact--email .recipient-phone::before{content:\"|\";margin:0 0.5rem}.recipient-list-item .recipient-add-button{color:#f49132}";

const RecipientItem = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.showAdd = true;
    }
    render() {
        const { name, email, mobile, limetype, company } = this.recipient;
        const icon = this.getIcon(limetype);
        const recipientList = `recipient-list-item ${this.isDisabled()}`;
        const contactInfoClasses = `recipient-info-contact-data${email ? ' contact--email' : ''}${mobile ? ' contact--phone' : ''}`;
        return (index.h("li", { class: recipientList }, index.h("div", { class: `recipient-icon ${limetype}` }, index.h("limel-icon", { name: icon, size: "small" })), index.h("div", { class: "recipient-info-container" }, index.h("span", null, name), index.h("div", null, index.h("span", null, company)), index.h("div", { class: contactInfoClasses }, index.h("span", { class: "recipient-email" }, email), index.h("span", { class: "recipient-phone" }, mobile))), this.renderAddIcon(this.showAdd)));
    }
    renderAddIcon(show) {
        return show ? (index.h("div", { class: "recipient-add-button" }, index.h("limel-icon", { name: "add", size: "medium" }))) : ([]);
    }
    getIcon(limetype) {
        return limetype === 'coworker' ? 'school_director' : 'guest_male';
    }
    isDisabled() {
        return !this.recipient.email && !this.recipient.mobile
            ? 'disabled'
            : '';
    }
};
RecipientItem.style = recipientItemCss;

exports.recipient_item = RecipientItem;
