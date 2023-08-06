import { r as registerInstance, c as createEvent, h } from './index-570406ba.js';

const customFieldsCss = "";

const CustomFields = class {
    constructor(hostRef) { registerInstance(this, hostRef); this.updateFieldValue = createEvent(this, "updateFieldValue", 7); }
    render() {
        if (this.isLoading) {
            return h("ga-loader", null);
        }
        else if (!this.template) {
            return [];
        }
        if (!this.customFields.length) {
            return [
                h("h4", null, "Fields"),
                h("empty-state", { text: "This template has no fields", icon: "text_box" }),
            ];
        }
        return [
            h("h4", null, "Fields"),
            this.customFields.map(field => (h("limel-input-field", { label: field.label, value: field.value, disabled: !field.is_editable, onChange: event => this.onChangeField(event, field.id) }))),
        ];
    }
    onChangeField(event, id) {
        this.updateFieldValue.emit({ id, value: event.detail });
    }
};
CustomFields.style = customFieldsCss;

const limeDocumentListCss = ".accordion-content{max-height:25rem;overflow-y:auto}limel-list{--lime-primary-color:#f49132}";

const LimeDocumentList = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.setLimeDocument = createEvent(this, "setLimeDocument", 7);
        this.documents = [];
        this.selectDocument = this.selectDocument.bind(this);
    }
    render() {
        if (this.isLoading) {
            return h("ga-loader", null);
        }
        else if (!this.documents.length) {
            return h("empty-state", { text: "No documents were found!" });
        }
        return (h("limel-list", { class: "accordion-content", items: this.documents, type: "radio", onChange: this.selectDocument }));
    }
    selectDocument(event) {
        this.setLimeDocument.emit(event.detail);
    }
};
LimeDocumentList.style = limeDocumentListCss;

const templateListCss = ".accordion-content{max-height:25rem;overflow-y:auto}limel-list{--lime-primary-color:#f49132}";

const TemplateList = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.setTemplate = createEvent(this, "setTemplate", 7);
        this.selectTemplate = this.selectTemplate.bind(this);
    }
    render() {
        if (this.isLoading) {
            return h("ga-loader", null);
        }
        if (!this.templates.length) {
            return h("empty-state", { text: "No templates were found!" });
        }
        return (h("limel-list", { class: "accordion-content", items: this.templates, type: "radio", onChange: this.selectTemplate }));
    }
    selectTemplate(event) {
        this.setTemplate.emit(event.detail);
    }
};
TemplateList.style = templateListCss;

const templatePreviewCss = ".page-info-container{display:-ms-flexbox;display:flex;-ms-flex-pack:center;justify-content:center}.page-info-container .page-thumb{width:9rem;height:12rem;background-color:#ccc;-o-object-fit:contain;object-fit:contain}";

const TemplatePreview = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.getThumbUrl = this.getThumbUrl.bind(this);
    }
    getThumbUrl() {
        const path = `${this.session.entity_id}/${this.template.value}`;
        return `getaccept/preview_proxy/${path}`;
    }
    render() {
        if (!this.template || this.isLoading) {
            return [];
        }
        return (h("div", { class: "page-info-container" }, h("img", { class: "page-thumb", src: this.getThumbUrl() })));
    }
};
TemplatePreview.style = templatePreviewCss;

export { CustomFields as custom_fields, LimeDocumentList as lime_document_list, TemplateList as template_list, TemplatePreview as template_preview };
