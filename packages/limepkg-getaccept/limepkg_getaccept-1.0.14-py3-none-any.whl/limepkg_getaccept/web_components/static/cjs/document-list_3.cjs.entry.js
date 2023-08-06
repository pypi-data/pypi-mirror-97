'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-60d4a812.js');
const EnumViews = require('./EnumViews-bbc19da7.js');
const EnumDocumentStatuses = require('./EnumDocumentStatuses-66de00d1.js');

const documentListCss = ".document-list{padding:0;margin:0;height:50vh;overflow:auto}";

const DocumentList = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.documents = [];
    }
    render() {
        if (!this.documents.length) {
            return index.h("empty-state", { text: "No documents were found!" });
        }
        return [
            index.h("ul", { class: "document-list" }, this.documents.map(document => {
                return index.h("document-list-item", { document: document });
            })),
        ];
    }
};
DocumentList.style = documentListCss;

const documentListItemCss = ".document-list-item{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;padding:0.5rem;border-bottom:1px solid #ccc;cursor:pointer}.document-list-item:hover{background-color:#ccc}.document-list-item .document-icon{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;margin-right:1rem;padding:0.5rem;border-radius:50%;background-color:#5b9bd1;color:#fff}.document-list-item .document-icon.sent{background-color:#2dc990}.document-list-item .document-icon.hardbounced{background-color:#f88987}.document-list-item .document-icon.sealed{background-color:#f49132}.document-list-item .document-icon.draft{background-color:#737373}.document-list-item .document-info-container{display:-ms-flexbox;display:flex;-ms-flex-direction:column;flex-direction:column;font-size:0.8rem}.document-list-item .document-info-container .document-created-date{margin-left:0.5rem}.document-list-item .document-info-container .document-created-date::before{content:\"|\";margin-right:0.5rem}";

const DocumentListItem = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.openDocument = index.createEvent(this, "openDocument", 7);
        this.handleOpenDocument = this.handleOpenDocument.bind(this);
    }
    render() {
        let documentIcon = this.document.status.toLowerCase() + ' document-icon';
        return (index.h("li", { class: "document-list-item", onClick: this.handleOpenDocument }, index.h("div", { class: documentIcon }, index.h("limel-icon", { name: this.getDocumentIcon(this.document.status), size: "small" })), index.h("div", { class: "document-info-container" }, index.h("div", { class: "document-name" }, this.document.name), index.h("div", { class: "document-status" }, index.h("span", null, this.document.status), index.h("span", { class: "document-created-date" }, EnumDocumentStatuses.moment(this.document.created_at).format('YYYY-MM-DD'))))));
    }
    handleOpenDocument() {
        this.openDocument.emit(this.document);
    }
    getDocumentIcon(status) {
        switch (status) {
            case EnumDocumentStatuses.EnumDocumentStatuses.draft:
                return 'no_edit';
            case EnumDocumentStatuses.EnumDocumentStatuses.hardbounced:
                return 'error';
            case EnumDocumentStatuses.EnumDocumentStatuses.importing:
                return 'import';
            case EnumDocumentStatuses.EnumDocumentStatuses.lost:
                return 'drama';
            case EnumDocumentStatuses.EnumDocumentStatuses.processing:
                return 'submit_progress';
            case EnumDocumentStatuses.EnumDocumentStatuses.recalled:
                return 'double_left';
            case EnumDocumentStatuses.EnumDocumentStatuses.rejected:
                return 'private';
            case EnumDocumentStatuses.EnumDocumentStatuses.reviewed:
                return 'preview_pane';
            case EnumDocumentStatuses.EnumDocumentStatuses.scheduled:
                return 'overtime';
            case EnumDocumentStatuses.EnumDocumentStatuses.sealed:
                return 'lock';
            case EnumDocumentStatuses.EnumDocumentStatuses.sent:
                return 'wedding_gift';
            case EnumDocumentStatuses.EnumDocumentStatuses.signed:
                return 'autograph';
            case EnumDocumentStatuses.EnumDocumentStatuses.signedwithoutverification:
                return 'autograph';
            case EnumDocumentStatuses.EnumDocumentStatuses.viewed:
                return 'visible';
            default:
                return 'dancing_party';
        }
    }
};
DocumentListItem.style = documentListItemCss;

const sendNewDocumentButtonCss = ".new-document-button-container{display:-ms-flexbox;display:flex;-ms-flex-direction:column;flex-direction:column;-ms-flex-wrap:wrap;flex-wrap:wrap;-ms-flex-align:center;align-items:center;text-align:center;margin:0.5rem 0;border-radius:0.2rem;overflow:hidden}.new-document-button-container .new-document-icon{margin-bottom:1rem}limel-button{--lime-primary-color:#f49132}@media (min-width: 1074px){.new-document-button-container{width:13rem}}@media (max-width: 1075px){.new-document-button-container{width:100%;background-color:#f5f5f5}}";

const Root = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.changeView = index.createEvent(this, "changeView", 7);
        this.setDocumentType = index.createEvent(this, "setDocumentType", 7);
        this.changeViewHandler = this.changeViewHandler.bind(this);
    }
    buttonData() {
        if (this.isSigning) {
            return {
                label: 'Document for signing',
                icon: 'edit',
                description: 'Used for signing sales related documents.',
                buttonText: 'For signing',
            };
        }
        return {
            label: 'Document for tracking',
            icon: 'search',
            description: 'Used when no signing is required.',
            buttonText: 'For tracking',
        };
    }
    render() {
        let buttonContainer = 'new-document-button-container';
        buttonContainer += !this.isSigning ? ' tracking' : '';
        const { icon, label, buttonText, description } = this.buttonData();
        return [
            index.h("div", { class: buttonContainer }, index.h("h4", null, label), index.h("limel-icon", { class: "new-document-icon", name: icon, size: "large" }), index.h("limel-button", { primary: true, label: buttonText, onClick: this.changeViewHandler }), index.h("p", null, description)),
        ];
    }
    changeViewHandler() {
        this.changeView.emit(EnumViews.EnumViews.recipient);
        this.setDocumentType.emit(this.isSigning);
    }
};
Root.style = sendNewDocumentButtonCss;

exports.document_list = DocumentList;
exports.document_list_item = DocumentListItem;
exports.send_new_document_button = Root;
