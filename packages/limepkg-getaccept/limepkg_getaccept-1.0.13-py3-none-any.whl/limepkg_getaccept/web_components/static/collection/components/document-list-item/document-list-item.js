import { Component, h, Prop, Event } from '@stencil/core';
import { EnumDocumentStatuses } from '../../models/EnumDocumentStatuses';
import moment from 'moment/moment';
export class DocumentListItem {
    constructor() {
        this.handleOpenDocument = this.handleOpenDocument.bind(this);
    }
    render() {
        let documentIcon = this.document.status.toLowerCase() + ' document-icon';
        return (h("li", { class: "document-list-item", onClick: this.handleOpenDocument },
            h("div", { class: documentIcon },
                h("limel-icon", { name: this.getDocumentIcon(this.document.status), size: "small" })),
            h("div", { class: "document-info-container" },
                h("div", { class: "document-name" }, this.document.name),
                h("div", { class: "document-status" },
                    h("span", null, this.document.status),
                    h("span", { class: "document-created-date" }, moment(this.document.created_at).format('YYYY-MM-DD'))))));
    }
    handleOpenDocument() {
        this.openDocument.emit(this.document);
    }
    getDocumentIcon(status) {
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
    }
    static get is() { return "document-list-item"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["document-list-item.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["document-list-item.css"]
    }; }
    static get properties() { return {
        "document": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "IDocument",
                "resolved": "IDocument",
                "references": {
                    "IDocument": {
                        "location": "import",
                        "path": "../../types/Document"
                    }
                }
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": ""
            }
        }
    }; }
    static get events() { return [{
            "method": "openDocument",
            "name": "openDocument",
            "bubbles": true,
            "cancelable": true,
            "composed": true,
            "docs": {
                "tags": [],
                "text": ""
            },
            "complexType": {
                "original": "IDocument",
                "resolved": "IDocument",
                "references": {
                    "IDocument": {
                        "location": "import",
                        "path": "../../types/Document"
                    }
                }
            }
        }]; }
}
