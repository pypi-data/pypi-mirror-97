'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-60d4a812.js');

const createEmailCss = ".send-document-email{width:calc(100% - 1.2rem);border-color:rgba(0, 0, 0, 0.12);font-size:0.875rem;line-height:1.125rem;font-weight:400;padding:0.5rem}.send-document-email:focus{outline:none;border-color:#26a69a}.send-document-email-subject{margin-top:1rem;display:block;margin-left:1rem;font-size:0.675rem}";

const CreateEmail = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.setEmailSubject = index.createEvent(this, "setEmailSubject", 7);
        this.setEmailMessage = index.createEvent(this, "setEmailMessage", 7);
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
            index.h("div", null, index.h("h3", null, "Write your email"), index.h("limel-input-field", { label: "Subject", value: this.emailSubject, onChange: this.handleChangeEmailSubject }), index.h("span", { class: "send-document-email-subject" }, "Email"), index.h("textarea", { class: "send-document-email", rows: 9, value: this.emailMessage, onChange: this.handleChangeEmailMessage })),
        ];
    }
    handleChangeEmailSubject(event) {
        this.emailSubject = event.detail;
        this.setEmailSubject.emit(event.detail);
    }
    handleChangeEmailMessage(event) {
        this.setEmailMessage.emit(event.target.value);
    }
};
CreateEmail.style = createEmailCss;

exports.create_email = CreateEmail;
