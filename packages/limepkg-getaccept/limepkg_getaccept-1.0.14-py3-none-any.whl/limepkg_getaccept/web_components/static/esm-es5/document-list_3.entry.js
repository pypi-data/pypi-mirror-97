import { r as registerInstance, h, c as createEvent } from './index-570406ba.js';
import { E as EnumViews } from './EnumViews-26a35d6d.js';
import { m as moment, E as EnumDocumentStatuses } from './EnumDocumentStatuses-a9bc0ab7.js';
var documentListCss = ".document-list{padding:0;margin:0;height:50vh;overflow:auto}";
var DocumentList = /** @class */ (function () {
    function DocumentList(hostRef) {
        registerInstance(this, hostRef);
        this.documents = [];
    }
    DocumentList.prototype.render = function () {
        if (!this.documents.length) {
            return h("empty-state", { text: "No documents were found!" });
        }
        return [
            h("ul", { class: "document-list" }, this.documents.map(function (document) {
                return h("document-list-item", { document: document });
            })),
        ];
    };
    return DocumentList;
}());
DocumentList.style = documentListCss;
var documentListItemCss = ".document-list-item{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;padding:0.5rem;border-bottom:1px solid #ccc;cursor:pointer}.document-list-item:hover{background-color:#ccc}.document-list-item .document-icon{display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;margin-right:1rem;padding:0.5rem;border-radius:50%;background-color:#5b9bd1;color:#fff}.document-list-item .document-icon.sent{background-color:#2dc990}.document-list-item .document-icon.hardbounced{background-color:#f88987}.document-list-item .document-icon.sealed{background-color:#f49132}.document-list-item .document-icon.draft{background-color:#737373}.document-list-item .document-info-container{display:-ms-flexbox;display:flex;-ms-flex-direction:column;flex-direction:column;font-size:0.8rem}.document-list-item .document-info-container .document-created-date{margin-left:0.5rem}.document-list-item .document-info-container .document-created-date::before{content:\"|\";margin-right:0.5rem}";
var DocumentListItem = /** @class */ (function () {
    function DocumentListItem(hostRef) {
        registerInstance(this, hostRef);
        this.openDocument = createEvent(this, "openDocument", 7);
        this.handleOpenDocument = this.handleOpenDocument.bind(this);
    }
    DocumentListItem.prototype.render = function () {
        var documentIcon = this.document.status.toLowerCase() + ' document-icon';
        return (h("li", { class: "document-list-item", onClick: this.handleOpenDocument }, h("div", { class: documentIcon }, h("limel-icon", { name: this.getDocumentIcon(this.document.status), size: "small" })), h("div", { class: "document-info-container" }, h("div", { class: "document-name" }, this.document.name), h("div", { class: "document-status" }, h("span", null, this.document.status), h("span", { class: "document-created-date" }, moment(this.document.created_at).format('YYYY-MM-DD'))))));
    };
    DocumentListItem.prototype.handleOpenDocument = function () {
        this.openDocument.emit(this.document);
    };
    DocumentListItem.prototype.getDocumentIcon = function (status) {
        switch (status) {
            case EnumDocumentStatuses.draft:
                return 'no_edit';
            case EnumDocumentStatuses.hardbounced:
                return 'error';
            case EnumDocumentStatuses.importing:
                return 'import';
            case EnumDocumentStatuses.lost:
                return 'drama';
            case EnumDocumentStatuses.processing:
                return 'submit_progress';
            case EnumDocumentStatuses.recalled:
                return 'double_left';
            case EnumDocumentStatuses.rejected:
                return 'private';
            case EnumDocumentStatuses.reviewed:
                return 'preview_pane';
            case EnumDocumentStatuses.scheduled:
                return 'overtime';
            case EnumDocumentStatuses.sealed:
                return 'lock';
            case EnumDocumentStatuses.sent:
                return 'wedding_gift';
            case EnumDocumentStatuses.signed:
                return 'autograph';
            case EnumDocumentStatuses.signedwithoutverification:
                return 'autograph';
            case EnumDocumentStatuses.viewed:
                return 'visible';
            default:
                return 'dancing_party';
        }
    };
    return DocumentListItem;
}());
DocumentListItem.style = documentListItemCss;
var sendNewDocumentButtonCss = ".new-document-button-container{display:-ms-flexbox;display:flex;-ms-flex-direction:column;flex-direction:column;-ms-flex-wrap:wrap;flex-wrap:wrap;-ms-flex-align:center;align-items:center;text-align:center;margin:0.5rem 0;border-radius:0.2rem;overflow:hidden}.new-document-button-container .new-document-icon{margin-bottom:1rem}limel-button{--lime-primary-color:#f49132}@media (min-width: 1074px){.new-document-button-container{width:13rem}}@media (max-width: 1075px){.new-document-button-container{width:100%;background-color:#f5f5f5}}";
var Root = /** @class */ (function () {
    function Root(hostRef) {
        registerInstance(this, hostRef);
        this.changeView = createEvent(this, "changeView", 7);
        this.setDocumentType = createEvent(this, "setDocumentType", 7);
        this.changeViewHandler = this.changeViewHandler.bind(this);
    }
    Root.prototype.buttonData = function () {
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
    };
    Root.prototype.render = function () {
        var buttonContainer = 'new-document-button-container';
        buttonContainer += !this.isSigning ? ' tracking' : '';
        var _a = this.buttonData(), icon = _a.icon, label = _a.label, buttonText = _a.buttonText, description = _a.description;
        return [
            h("div", { class: buttonContainer }, h("h4", null, label), h("limel-icon", { class: "new-document-icon", name: icon, size: "large" }), h("limel-button", { primary: true, label: buttonText, onClick: this.changeViewHandler }), h("p", null, description)),
        ];
    };
    Root.prototype.changeViewHandler = function () {
        this.changeView.emit(EnumViews.recipient);
        this.setDocumentType.emit(this.isSigning);
    };
    return Root;
}());
Root.style = sendNewDocumentButtonCss;
export { DocumentList as document_list, DocumentListItem as document_list_item, Root as send_new_document_button };
