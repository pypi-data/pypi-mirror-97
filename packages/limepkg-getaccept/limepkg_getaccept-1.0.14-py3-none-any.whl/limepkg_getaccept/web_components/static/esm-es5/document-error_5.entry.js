import { r as registerInstance, c as createEvent, h } from './index-570406ba.js';
var documentErrorCss = ".document-error{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;padding:1rem 1rem;cursor:pointer}.document-error .document-error-icon{display:inherit;padding:0.5rem;margin-right:1.5rem;border-radius:50%;background-color:#f88987;color:#fff}.document-error .document-error-info{display:-ms-flexbox;display:flex;-ms-flex-direction:column;flex-direction:column}.document-error .document-error-info .document-error-header{-webkit-margin-after:0;margin-block-end:0;-webkit-margin-before:0;margin-block-start:0}.document-error:hover{background-color:#f5f5f5}@media (min-width: 1074px){.document-error{width:50%}}@media (max-width: 1075px){.document-error{width:100%}}";
var DocumentError = /** @class */ (function () {
    function DocumentError(hostRef) {
        registerInstance(this, hostRef);
        this.changeView = createEvent(this, "changeView", 7);
        this.onClick = this.onClick.bind(this);
    }
    DocumentError.prototype.render = function () {
        return [
            h("li", { class: "document-error", onClick: this.onClick }, h("div", { class: "document-error-icon" }, h("limel-icon", { name: this.error.icon, size: "small" })), h("div", { class: "document-error-info" }, h("h4", { class: "document-error-header" }, this.error.header), h("span", null, this.error.title))),
        ];
    };
    DocumentError.prototype.onClick = function () {
        this.changeView.emit(this.error.view);
    };
    return DocumentError;
}());
DocumentError.style = documentErrorCss;
var documentErrorFeedbackCss = ".document-error-list{padding:0}";
var DocumentErrorFeedback = /** @class */ (function () {
    function DocumentErrorFeedback(hostRef) {
        registerInstance(this, hostRef);
        this.errorList = [];
    }
    DocumentErrorFeedback.prototype.render = function () {
        return [
            h("div", null, h("h3", null, "You need to fix following tasks to send:"), h("ul", { class: "document-error-list" }, this.errorList.map(function (error) {
                return h("document-error", { error: error });
            })))
        ];
    };
    return DocumentErrorFeedback;
}());
DocumentErrorFeedback.style = documentErrorFeedbackCss;
var documentValidateInfoCss = ".validate-document-success{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}@media (min-width: 768px){.validate-document-success .validate-document-summary{width:50%}.validate-document-success .validate-document-recipients{width:50%}}@media (max-width: 769px){.validate-document-success .validate-document-summary{width:100%}.validate-document-success .validate-document-recipients{width:100%}}.validate-document-success .validate-document-property-list{list-style-type:none;margin:0;padding:0rem;width:100%}.validate-document-success .validate-document-property-list .document-property{font-weight:bold}.validate-document-success .document-recipient-list{margin:0 0 1rem 0;width:100%;padding:0rem}limel-button{--lime-primary-color:#f49132}";
var DocumentValidateInfo = /** @class */ (function () {
    function DocumentValidateInfo(hostRef) {
        registerInstance(this, hostRef);
        this.hasProperty = this.hasProperty.bind(this);
    }
    DocumentValidateInfo.prototype.render = function () {
        return [
            h("div", { class: "validate-document-success" }, h("div", { class: "validate-document-summary" }, h("h3", null, "Summary"), h("ul", { class: "validate-document-property-list" }, h("li", null, h("span", { class: "document-property" }, "Name: "), h("span", null, this.document.name)), h("li", null, h("span", { class: "document-property" }, "Value: "), h("span", null, this.document.value)), h("li", null, h("span", { class: "document-property" }, "Document is for signing:", ' '), h("span", null, this.hasProperty(this.document.is_signing))), h("li", null, h("span", { class: "document-property" }, "Video is added:", ' '), h("span", null, this.hasProperty(this.document.is_video))), h("li", null, h("span", { class: "document-property" }, "Send smart reminders:", ' '), h("span", null, this.hasProperty(this.document.is_reminder_sending))), h("li", null, h("span", { class: "document-property" }, "Send link by SMS:", ' '), h("span", null, this.hasProperty(this.document.is_sms_sending))))), h("div", { class: "validate-document-recipients" }, h("h3", null, "Recipients"), h("ul", { class: "document-recipient-list" }, this.document.recipients.map(function (recipient) {
                return (h("recipient-item", { recipient: recipient, showAdd: false }));
            })))),
        ];
    };
    DocumentValidateInfo.prototype.hasProperty = function (value) {
        return value ? 'Yes' : 'No';
    };
    return DocumentValidateInfo;
}());
DocumentValidateInfo.style = documentValidateInfoCss;
var gaLoaderWithTextCss = "limel-spinner{margin:2rem 0;color:#f49132}.share-document-loading-container{text-align:center;margin-top:3rem}";
var GALoaderWithText = /** @class */ (function () {
    function GALoaderWithText(hostRef) {
        registerInstance(this, hostRef);
        this.showText = false;
    }
    GALoaderWithText.prototype.render = function () {
        var _this = this;
        return (h("div", { class: "share-document-loading-container" }, (function () {
            if (_this.showText) {
                return (h("div", null, h("h3", null, _this.text)));
            }
        })(), h("ga-loader", null)));
    };
    return GALoaderWithText;
}());
GALoaderWithText.style = gaLoaderWithTextCss;
var shareDocumentLinkCss = ".share-document-list-item{margin:0.5rem 0;padding:0.5rem 1rem}.share-document-list-item .recipient-info-container{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;padding-left:1rem}.share-document-list-item .recipient-info-container .recipient-icon{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;margin-right:1rem;padding:0.5em;border-radius:50%;background-color:#5b9bd1;color:#fff}.share-document-list-item .recipient-info-container .recipient-info{display:-ms-flexbox;display:flex;-ms-flex-direction:column;flex-direction:column}.share-document-list-item .recipient-info-container .recipient-info .recipient-info-name{text-transform:capitalize;font-weight:bold}.share-document-list-item .recipient-info-container .recipient-info .recipient-info{text-transform:capitalize}";
var ShareDocumentLink = /** @class */ (function () {
    function ShareDocumentLink(hostRef) {
        registerInstance(this, hostRef);
        this.handleCopyLink = this.handleCopyLink.bind(this);
    }
    ShareDocumentLink.prototype.render = function () {
        return (h("li", { class: "share-document-list-item" }, h("div", { class: "recipient-info-container" }, h("div", { class: "recipient-icon" }, h("limel-icon", { name: "user", size: "small" })), h("div", { class: "recipient-info" }, h("span", { class: "recipient-info-name" }, this.recipient.name), h("span", { class: "recipient-info-role" }, this.recipient.role))), h("div", null, h("limel-input-field", { label: "Signing link", type: "email", value: this.recipient.document_url, trailingIcon: "copy_link", onAction: this.handleCopyLink }))));
    };
    ShareDocumentLink.prototype.handleCopyLink = function () {
        var copyText = document.createElement('textarea');
        copyText.value = this.recipient.document_url;
        document.body.appendChild(copyText);
        copyText.select();
        document.execCommand('copy');
        document.body.removeChild(copyText);
    };
    return ShareDocumentLink;
}());
ShareDocumentLink.style = shareDocumentLinkCss;
export { DocumentError as document_error, DocumentErrorFeedback as document_error_feedback, DocumentValidateInfo as document_validate_info, GALoaderWithText as ga_loader_with_text, ShareDocumentLink as share_document_link };
