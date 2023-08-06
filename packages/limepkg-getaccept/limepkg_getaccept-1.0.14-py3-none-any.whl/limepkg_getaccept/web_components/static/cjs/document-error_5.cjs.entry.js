'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-60d4a812.js');

const documentErrorCss = ".document-error{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;padding:1rem 1rem;cursor:pointer}.document-error .document-error-icon{display:inherit;padding:0.5rem;margin-right:1.5rem;border-radius:50%;background-color:#f88987;color:#fff}.document-error .document-error-info{display:-ms-flexbox;display:flex;-ms-flex-direction:column;flex-direction:column}.document-error .document-error-info .document-error-header{-webkit-margin-after:0;margin-block-end:0;-webkit-margin-before:0;margin-block-start:0}.document-error:hover{background-color:#f5f5f5}@media (min-width: 1074px){.document-error{width:50%}}@media (max-width: 1075px){.document-error{width:100%}}";

const DocumentError = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.changeView = index.createEvent(this, "changeView", 7);
        this.onClick = this.onClick.bind(this);
    }
    render() {
        return [
            index.h("li", { class: "document-error", onClick: this.onClick }, index.h("div", { class: "document-error-icon" }, index.h("limel-icon", { name: this.error.icon, size: "small" })), index.h("div", { class: "document-error-info" }, index.h("h4", { class: "document-error-header" }, this.error.header), index.h("span", null, this.error.title))),
        ];
    }
    onClick() {
        this.changeView.emit(this.error.view);
    }
};
DocumentError.style = documentErrorCss;

const documentErrorFeedbackCss = ".document-error-list{padding:0}";

const DocumentErrorFeedback = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.errorList = [];
    }
    render() {
        return [
            index.h("div", null, index.h("h3", null, "You need to fix following tasks to send:"), index.h("ul", { class: "document-error-list" }, this.errorList.map((error) => {
                return index.h("document-error", { error: error });
            })))
        ];
    }
};
DocumentErrorFeedback.style = documentErrorFeedbackCss;

const documentValidateInfoCss = ".validate-document-success{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}@media (min-width: 768px){.validate-document-success .validate-document-summary{width:50%}.validate-document-success .validate-document-recipients{width:50%}}@media (max-width: 769px){.validate-document-success .validate-document-summary{width:100%}.validate-document-success .validate-document-recipients{width:100%}}.validate-document-success .validate-document-property-list{list-style-type:none;margin:0;padding:0rem;width:100%}.validate-document-success .validate-document-property-list .document-property{font-weight:bold}.validate-document-success .document-recipient-list{margin:0 0 1rem 0;width:100%;padding:0rem}limel-button{--lime-primary-color:#f49132}";

const DocumentValidateInfo = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.hasProperty = this.hasProperty.bind(this);
    }
    render() {
        return [
            index.h("div", { class: "validate-document-success" }, index.h("div", { class: "validate-document-summary" }, index.h("h3", null, "Summary"), index.h("ul", { class: "validate-document-property-list" }, index.h("li", null, index.h("span", { class: "document-property" }, "Name: "), index.h("span", null, this.document.name)), index.h("li", null, index.h("span", { class: "document-property" }, "Value: "), index.h("span", null, this.document.value)), index.h("li", null, index.h("span", { class: "document-property" }, "Document is for signing:", ' '), index.h("span", null, this.hasProperty(this.document.is_signing))), index.h("li", null, index.h("span", { class: "document-property" }, "Video is added:", ' '), index.h("span", null, this.hasProperty(this.document.is_video))), index.h("li", null, index.h("span", { class: "document-property" }, "Send smart reminders:", ' '), index.h("span", null, this.hasProperty(this.document.is_reminder_sending))), index.h("li", null, index.h("span", { class: "document-property" }, "Send link by SMS:", ' '), index.h("span", null, this.hasProperty(this.document.is_sms_sending))))), index.h("div", { class: "validate-document-recipients" }, index.h("h3", null, "Recipients"), index.h("ul", { class: "document-recipient-list" }, this.document.recipients.map(recipient => {
                return (index.h("recipient-item", { recipient: recipient, showAdd: false }));
            })))),
        ];
    }
    hasProperty(value) {
        return value ? 'Yes' : 'No';
    }
};
DocumentValidateInfo.style = documentValidateInfoCss;

const gaLoaderWithTextCss = "limel-spinner{margin:2rem 0;color:#f49132}.share-document-loading-container{text-align:center;margin-top:3rem}";

const GALoaderWithText = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.showText = false;
    }
    render() {
        return (index.h("div", { class: "share-document-loading-container" }, (() => {
            if (this.showText) {
                return (index.h("div", null, index.h("h3", null, this.text)));
            }
        })(), index.h("ga-loader", null)));
    }
};
GALoaderWithText.style = gaLoaderWithTextCss;

const shareDocumentLinkCss = ".share-document-list-item{margin:0.5rem 0;padding:0.5rem 1rem}.share-document-list-item .recipient-info-container{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;padding-left:1rem}.share-document-list-item .recipient-info-container .recipient-icon{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;margin-right:1rem;padding:0.5em;border-radius:50%;background-color:#5b9bd1;color:#fff}.share-document-list-item .recipient-info-container .recipient-info{display:-ms-flexbox;display:flex;-ms-flex-direction:column;flex-direction:column}.share-document-list-item .recipient-info-container .recipient-info .recipient-info-name{text-transform:capitalize;font-weight:bold}.share-document-list-item .recipient-info-container .recipient-info .recipient-info{text-transform:capitalize}";

const ShareDocumentLink = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.handleCopyLink = this.handleCopyLink.bind(this);
    }
    render() {
        return (index.h("li", { class: "share-document-list-item" }, index.h("div", { class: "recipient-info-container" }, index.h("div", { class: "recipient-icon" }, index.h("limel-icon", { name: "user", size: "small" })), index.h("div", { class: "recipient-info" }, index.h("span", { class: "recipient-info-name" }, this.recipient.name), index.h("span", { class: "recipient-info-role" }, this.recipient.role))), index.h("div", null, index.h("limel-input-field", { label: "Signing link", type: "email", value: this.recipient.document_url, trailingIcon: "copy_link", onAction: this.handleCopyLink }))));
    }
    handleCopyLink() {
        var copyText = document.createElement('textarea');
        copyText.value = this.recipient.document_url;
        document.body.appendChild(copyText);
        copyText.select();
        document.execCommand('copy');
        document.body.removeChild(copyText);
    }
};
ShareDocumentLink.style = shareDocumentLinkCss;

exports.document_error = DocumentError;
exports.document_error_feedback = DocumentErrorFeedback;
exports.document_validate_info = DocumentValidateInfo;
exports.ga_loader_with_text = GALoaderWithText;
exports.share_document_link = ShareDocumentLink;
