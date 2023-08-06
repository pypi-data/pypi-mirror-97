import { r as registerInstance, h } from './index-570406ba.js';

const documentPageInfoCss = ".page-info-container{display:-ms-flexbox;display:flex}.page-info-container .page-number{display:-ms-inline-flexbox;display:inline-flex;-ms-flex-align:center;align-items:center;-ms-flex-pack:center;justify-content:center;height:1.5rem;width:1.5rem;margin-right:1rem;border-radius:50%;-webkit-border-radius:50%;-moz-border-radius:50%;-ms-border-radius:50%;-o-border-radius:50%;background-color:#f49132;color:#fff}.page-info-container .page-thumb{width:4rem;height:6rem;background-color:#ccc;-o-object-fit:contain;object-fit:contain}.page-info-container .page-time-spent{margin-left:1rem}.page-info-container .page-time-spent .page-time-spent-text{display:block;font-size:0.6rem;font-weight:bold;text-transform:uppercase}.page-info-percent{margin-bottom:1rem}";

const DocumentPageInfo = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
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
            h("div", { class: "page-info-container" }, h("div", { class: "page-number" }, this.page.page_num), h("img", { class: "page-thumb", src: this.getThumbUrl(this.page.thumb_url) }), h("div", { class: "page-time-spent" }, h("span", { class: "page-time-spent-text" }, "Time spent"), h("span", null, this.page.page_time, "s"))),
            h("div", { class: "page-info-percent" }, h("span", null, this.valuePercent, "%"), h("limel-linear-progress", { value: this.value })),
        ];
    }
};
DocumentPageInfo.style = documentPageInfoCss;

export { DocumentPageInfo as document_page_info };
