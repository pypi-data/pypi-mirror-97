import { r as registerInstance, c as createEvent, h } from './index-570406ba.js';
var sendDocumentButtonGroupCss = ".send-document-button-group{margin-top:0.5rem}.send-document-button-group .send-document-button-open-in-ga{margin-left:0.5rem}limel-button{--lime-primary-color:#f49132}";
var SendDocumentButtonGroup = /** @class */ (function () {
    function SendDocumentButtonGroup(hostRef) {
        registerInstance(this, hostRef);
        this.validateDocument = createEvent(this, "validateDocument", 7);
        this.disabled = false;
        this.loading = false;
        this.handleOnClickSendButton = this.handleOnClickSendButton.bind(this);
    }
    SendDocumentButtonGroup.prototype.render = function () {
        return [
            h("div", { class: "send-document-button-group" }, h("limel-button", { label: "Prepare for sendout", primary: true, loading: this.loading, disabled: this.disabled, onClick: this.handleOnClickSendButton })),
        ];
    };
    SendDocumentButtonGroup.prototype.handleOnClickSendButton = function () {
        this.validateDocument.emit();
    };
    return SendDocumentButtonGroup;
}());
SendDocumentButtonGroup.style = sendDocumentButtonGroupCss;
export { SendDocumentButtonGroup as send_document_button_group };
