import { r as registerInstance, c as createEvent, h } from './index-570406ba.js';
var customFieldsCss = "";
var CustomFields = /** @class */ (function () {
    function CustomFields(hostRef) {
        registerInstance(this, hostRef);
        this.updateFieldValue = createEvent(this, "updateFieldValue", 7);
    }
    CustomFields.prototype.render = function () {
        var _this = this;
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
            this.customFields.map(function (field) { return (h("limel-input-field", { label: field.label, value: field.value, disabled: !field.is_editable, onChange: function (event) { return _this.onChangeField(event, field.id); } })); }),
        ];
    };
    CustomFields.prototype.onChangeField = function (event, id) {
        this.updateFieldValue.emit({ id: id, value: event.detail });
    };
    return CustomFields;
}());
CustomFields.style = customFieldsCss;
var limeDocumentListCss = ".accordion-content{max-height:25rem;overflow-y:auto}limel-list{--lime-primary-color:#f49132}";
var LimeDocumentList = /** @class */ (function () {
    function LimeDocumentList(hostRef) {
        registerInstance(this, hostRef);
        this.setLimeDocument = createEvent(this, "setLimeDocument", 7);
        this.documents = [];
        this.selectDocument = this.selectDocument.bind(this);
    }
    LimeDocumentList.prototype.render = function () {
        if (this.isLoading) {
            return h("ga-loader", null);
        }
        else if (!this.documents.length) {
            return h("empty-state", { text: "No documents were found!" });
        }
        return (h("limel-list", { class: "accordion-content", items: this.documents, type: "radio", onChange: this.selectDocument }));
    };
    LimeDocumentList.prototype.selectDocument = function (event) {
        this.setLimeDocument.emit(event.detail);
    };
    return LimeDocumentList;
}());
LimeDocumentList.style = limeDocumentListCss;
var templateListCss = ".accordion-content{max-height:25rem;overflow-y:auto}limel-list{--lime-primary-color:#f49132}";
var TemplateList = /** @class */ (function () {
    function TemplateList(hostRef) {
        registerInstance(this, hostRef);
        this.setTemplate = createEvent(this, "setTemplate", 7);
        this.selectTemplate = this.selectTemplate.bind(this);
    }
    TemplateList.prototype.render = function () {
        if (this.isLoading) {
            return h("ga-loader", null);
        }
        if (!this.templates.length) {
            return h("empty-state", { text: "No templates were found!" });
        }
        return (h("limel-list", { class: "accordion-content", items: this.templates, type: "radio", onChange: this.selectTemplate }));
    };
    TemplateList.prototype.selectTemplate = function (event) {
        this.setTemplate.emit(event.detail);
    };
    return TemplateList;
}());
TemplateList.style = templateListCss;
var templatePreviewCss = ".page-info-container{display:-ms-flexbox;display:flex;-ms-flex-pack:center;justify-content:center}.page-info-container .page-thumb{width:9rem;height:12rem;background-color:#ccc;-o-object-fit:contain;object-fit:contain}";
var TemplatePreview = /** @class */ (function () {
    function TemplatePreview(hostRef) {
        registerInstance(this, hostRef);
        this.getThumbUrl = this.getThumbUrl.bind(this);
    }
    TemplatePreview.prototype.getThumbUrl = function () {
        var path = this.session.entity_id + "/" + this.template.value;
        return "getaccept/preview_proxy/" + path;
    };
    TemplatePreview.prototype.render = function () {
        if (!this.template || this.isLoading) {
            return [];
        }
        return (h("div", { class: "page-info-container" }, h("img", { class: "page-thumb", src: this.getThumbUrl() })));
    };
    return TemplatePreview;
}());
TemplatePreview.style = templatePreviewCss;
export { CustomFields as custom_fields, LimeDocumentList as lime_document_list, TemplateList as template_list, TemplatePreview as template_preview };
