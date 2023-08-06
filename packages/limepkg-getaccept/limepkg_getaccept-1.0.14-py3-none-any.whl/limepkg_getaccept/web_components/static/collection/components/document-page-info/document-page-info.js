import { Component, h, Prop, State } from '@stencil/core';
export class DocumentPageInfo {
    constructor() {
        this.totalTime = 0;
        this.value = 0;
        this.valuePercent = 0;
    }
    componentWillLoad() {
        if (this.totalTime > 0 && this.page.page_time > 0) {
            this.value = this.page.page_time / this.totalTime;
            this.valuePercent = Math.round(this.value * 100);
        }
    }
    getThumbUrl(originalUrl = '') {
        const s3_credentials = originalUrl.split('?')[1];
        const bucket = this.getS3Bucket(originalUrl);
        return `getaccept/page_thumb_proxy/${bucket}/${this.session.entity_id}/${this.documentId}/${this.page.page_id}/${encodeURIComponent(s3_credentials)}`;
    }
    getS3Bucket(originalUrl) {
        return originalUrl.replace('https://', '').split('.s3.')[0] || '';
    }
    render() {
        return [
            h("div", { class: "page-info-container" },
                h("div", { class: "page-number" }, this.page.page_num),
                h("img", { class: "page-thumb", src: this.getThumbUrl(this.page.thumb_url) }),
                h("div", { class: "page-time-spent" },
                    h("span", { class: "page-time-spent-text" }, "Time spent"),
                    h("span", null,
                        this.page.page_time,
                        "s"))),
            h("div", { class: "page-info-percent" },
                h("span", null,
                    this.valuePercent,
                    "%"),
                h("limel-linear-progress", { value: this.value })),
        ];
    }
    static get is() { return "document-page-info"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["document-page-info.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["document-page-info.css"]
    }; }
    static get properties() { return {
        "page": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "IDocumentPage",
                "resolved": "IDocumentPage",
                "references": {
                    "IDocumentPage": {
                        "location": "import",
                        "path": "../../types/DocumentPage"
                    }
                }
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": ""
            }
        },
        "documentId": {
            "type": "string",
            "mutable": false,
            "complexType": {
                "original": "string",
                "resolved": "string",
                "references": {}
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": ""
            },
            "attribute": "document-id",
            "reflect": false
        },
        "session": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "ISession",
                "resolved": "ISession",
                "references": {
                    "ISession": {
                        "location": "import",
                        "path": "../../types/Session"
                    }
                }
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": ""
            }
        },
        "totalTime": {
            "type": "number",
            "mutable": false,
            "complexType": {
                "original": "number",
                "resolved": "number",
                "references": {}
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": ""
            },
            "attribute": "total-time",
            "reflect": false,
            "defaultValue": "0"
        }
    }; }
    static get states() { return {
        "value": {},
        "valuePercent": {}
    }; }
}
