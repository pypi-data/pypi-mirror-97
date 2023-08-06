'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-60d4a812.js');

const sendDocumentButtonGroupCss = ".send-document-button-group{margin-top:0.5rem}.send-document-button-group .send-document-button-open-in-ga{margin-left:0.5rem}limel-button{--lime-primary-color:#f49132}";

const SendDocumentButtonGroup = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.validateDocument = index.createEvent(this, "validateDocument", 7);
        this.disabled = false;
        this.loading = false;
        this.handleOnClickSendButton = this.handleOnClickSendButton.bind(this);
    }
    render() {
        return [
            index.h("div", { class: "send-document-button-group" }, index.h("limel-button", { label: "Prepare for sendout", primary: true, loading: this.loading, disabled: this.disabled, onClick: this.handleOnClickSendButton })),
        ];
    }
    handleOnClickSendButton() {
        this.validateDocument.emit();
    }
};
SendDocumentButtonGroup.style = sendDocumentButtonGroupCss;

exports.send_document_button_group = SendDocumentButtonGroup;
