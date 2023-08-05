import { Component, h, Prop, Event } from '@stencil/core';
export class DocumentError {
    constructor() {
        this.onClick = this.onClick.bind(this);
    }
    render() {
        return [
            h("li", { class: "document-error", onClick: this.onClick },
                h("div", { class: "document-error-icon" },
                    h("limel-icon", { name: this.error.icon, size: "small" })),
                h("div", { class: "document-error-info" },
                    h("h4", { class: "document-error-header" }, this.error.header),
                    h("span", null, this.error.title))),
        ];
    }
    onClick() {
        this.changeView.emit(this.error.view);
    }
    static get is() { return "document-error"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["document-error.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["document-error.css"]
    }; }
    static get properties() { return {
        "error": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "IError",
                "resolved": "IError",
                "references": {
                    "IError": {
                        "location": "import",
                        "path": "../../types/Error"
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
            "method": "changeView",
            "name": "changeView",
            "bubbles": true,
            "cancelable": true,
            "composed": true,
            "docs": {
                "tags": [],
                "text": ""
            },
            "complexType": {
                "original": "EnumViews",
                "resolved": "EnumViews.documentDetail | EnumViews.documentValidation | EnumViews.help | EnumViews.home | EnumViews.invite | EnumViews.login | EnumViews.logout | EnumViews.recipient | EnumViews.selectFile | EnumViews.sendDocument | EnumViews.settings | EnumViews.videoLibrary",
                "references": {
                    "EnumViews": {
                        "location": "import",
                        "path": "../../models/EnumViews"
                    }
                }
            }
        }]; }
}
