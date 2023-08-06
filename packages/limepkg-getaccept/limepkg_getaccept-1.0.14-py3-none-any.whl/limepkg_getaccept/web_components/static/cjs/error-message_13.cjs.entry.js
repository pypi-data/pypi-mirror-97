'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const index = require('./index-60d4a812.js');
const EnumViews = require('./EnumViews-bbc19da7.js');
const index$1 = require('./index-2fa8f133.js');
const workflowSteps = require('./workflow-steps-8ef19e00.js');
const EnumDocumentStatuses = require('./EnumDocumentStatuses-66de00d1.js');

const ErrorMessage = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.timeout = 10000;
        this.error = '';
        this.message = '';
        this.triggerSnackbar = this.triggerSnackbar.bind(this);
    }
    componentDidUpdate() {
        if (this.error) {
            this.message = this.error;
            this.triggerSnackbar();
        }
    }
    render() {
        return [
            index.h("limel-snackbar", { message: this.message, timeout: this.timeout, actionText: "Ok" }),
        ];
    }
    triggerSnackbar() {
        const snackbar = this.host.shadowRoot.querySelector('limel-snackbar');
        snackbar.show();
    }
    get host() { return index.getElement(this); }
};

const layoutDocumentDetailsCss = ".document-details-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap;max-height:50vh;overflow:auto}.document-details-container .document-details-info-list{padding:0;margin:0;list-style-type:none}.document-details-container .document-details-info-list .document-detail-title{font-weight:bold}.document-details-container .document-details-action-buttons{margin-top:1rem}.document-details-container .document-details-action-buttons .document-details-action-button-remove{margin-left:1rem}@media (min-width: 1074px){.document-details-container .document-details-info{width:65%}.document-details-container .document-details-pages{width:33%}}@media (max-width: 1075px){.document-details-container .document-details-info{width:100%}.document-details-container .document-details-pages{width:100%}}limel-button{--lime-primary-color:#f49132}";

const LayoutDocumentDetails = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.changeView = index.createEvent(this, "changeView", 7);
        this.documentData = {};
        this.isLoading = false;
        this.removeDocumentHandler = this.removeDocumentHandler.bind(this);
        this.openDocumentIntGetAcceptHandler = this.openDocumentIntGetAcceptHandler.bind(this);
    }
    componentWillLoad() {
        this.loadDocumentDetails();
    }
    render() {
        return [
            index.h("div", null, index.h("h3", null, "Document Details"), (() => {
                if (this.isLoading) {
                    return index.h("ga-loader", null);
                }
                else {
                    return (index.h("div", { class: "document-details-container" }, index.h("div", { class: "document-details-info" }, index.h("ul", { class: "document-details-info-list" }, index.h("li", null, index.h("span", { class: "document-detail-title" }, "Document name:"), ' ', this.documentData.name), index.h("li", null, index.h("span", { class: "document-detail-title" }, "Status:"), ' ', this.documentData.status), index.h("li", null, index.h("span", { class: "document-detail-title" }, "Deal value:"), ' ', this.documentData.value), index.h("li", null, index.h("span", { class: "document-detail-title" }, "Expiration date:"), ' ', this.documentData.expiration_date), index.h("li", null, index.h("span", { class: "document-detail-title" }, "Send date:"), ' ', this.documentData.send_date)), index.h("div", { class: "document-details-action-buttons" }, index.h("limel-button", { primary: true, label: "Open in GetAccept", onClick: this
                            .openDocumentIntGetAcceptHandler }), index.h("limel-button", { class: "document-details-action-button-remove", primary: false, label: "Remove document", onClick: this.removeDocumentHandler }))), index.h("div", { class: "document-details-pages" }, index.h("ul", null, this.documentData.pages.map(page => {
                        return (index.h("document-page-info", { documentId: this.documentData.id, session: this.session, page: page, totalTime: this.totalPageViewTime }));
                    })))));
                }
            })()),
        ];
    }
    async loadDocumentDetails() {
        //should load document details. Replace hard coded id with id from this.document.
        this.isLoading = true;
        const rawDocument = await index$1.fetchDocumentDetails(this.platform, this.session, this.documentId);
        this.documentData = {
            id: rawDocument.id,
            name: rawDocument.name,
            page_count: rawDocument.page_count,
            status: rawDocument.status,
            value: rawDocument.value,
            expiration_date: EnumDocumentStatuses.moment(rawDocument.expiration_date).format('YYYY-MM-DD'),
            send_date: this.getSendDate(rawDocument),
            pages: this.getDocumentPages(rawDocument),
        };
        this.totalPageViewTime = this.getTotalPageViewTime(rawDocument);
        this.isLoading = false;
    }
    getSendDate(rawDocument) {
        return ((rawDocument.send_date &&
            EnumDocumentStatuses.moment(rawDocument.send_date).format('YYYY-MM-DD')) ||
            '');
    }
    getDocumentPages(rawDocument) {
        return ((rawDocument.pages &&
            rawDocument.pages.map((page) => {
                return {
                    page_id: page.page_id,
                    thumb_url: page.thumb_url,
                    page_time: page.page_time,
                    order_num: page.order_num,
                    page_num: page.page_num,
                };
            })) ||
            []);
    }
    getTotalPageViewTime(rawDocument) {
        return ((rawDocument.pages &&
            rawDocument.pages.reduce((acc, page) => acc + page.page_time, 0)) ||
            0);
    }
    async removeDocumentHandler() {
        this.isLoading = true;
        const result = await index$1.removeDocument(this.platform, this.session, this.documentId);
        this.isLoading = false;
        if (result) {
            this.changeView.emit(EnumViews.EnumViews.home);
        }
    }
    openDocumentIntGetAcceptHandler() {
        const page = this.documentData.status === EnumDocumentStatuses.EnumDocumentStatuses.draft
            ? 'edit'
            : 'view';
        window.open(`https://app.getaccept.com/document/${page}/${this.documentData.id}`, '_blank');
    }
};
LayoutDocumentDetails.style = layoutDocumentDetailsCss;

const layoutHelpCss = ".help-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}.help-container .help-support{width:100%}.help-container .help-support .help-support-link{text-decoration:none;color:#212121}.help-container .help-support .support-links-list{list-style-type:none;padding:0;margin-top:1rem}.help-container .help-support .support-links-list li{display:-ms-flexbox;display:flex;margin-top:0.5rem}.help-container .help-support .support-links-list li a{text-decoration:none;color:#212121;margin-left:0.5rem}";

const LayoutHelp = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
    }
    render() {
        return [
            index.h("div", null, index.h("h3", null, "Help"), index.h("div", { class: "help-container" }, index.h("div", { class: "help-support" }, index.h("a", { class: "help-support-link", href: "https://www.getaccept.com/support" }, "Have any questions or just looking for someone to talk to. Our support are always there for you"), index.h("ul", { class: "support-links-list" }, index.h("li", null, index.h("limel-icon", { class: "support", name: "phone", size: "small" }), index.h("a", { href: "tel:+46406688158" }, "+46 40-668-81-58")), index.h("li", null, index.h("limel-icon", { class: "support", name: "email", size: "small" }), index.h("a", { href: "mailto:support@getaccept.com" }, "support@getaccept.com")))))),
        ];
    }
};
LayoutHelp.style = layoutHelpCss;

const layoutLoginCss = ".auth-container{display:-ms-flexbox;display:flex;height:100%;width:100%}.auth-container .login-container{width:25%;padding:1rem;border-right:1px solid #ccc}.auth-container .login-container.active{width:60%}.auth-container .signup-container{width:40%;padding:1rem}.auth-container .signup-container.active{width:75%}";

const LayoutLogin = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.isSignup = false;
        this.toggleSignupContainer = this.toggleSignupContainer.bind(this);
    }
    render() {
        const loginClass = this.isSignup
            ? 'login-container'
            : 'login-container active';
        const signupClass = this.isSignup
            ? 'signup-container active'
            : 'signup-container';
        return [
            index.h("div", { class: "auth-container" }, index.h("div", { class: loginClass, onClick: () => this.toggleSignupContainer(false) }, index.h("h3", null, "Welcome Back"), index.h("ga-login", { platform: this.platform })), index.h("div", { class: signupClass, onClick: () => this.toggleSignupContainer(true) }, index.h("h3", null, "Create Account"), (() => {
                if (this.isSignup) {
                    return index.h("ga-signup", { platform: this.platform });
                }
                else {
                    return (index.h("limel-input-field", { label: "Email address", type: "email", value: "", trailingIcon: "filled_message" }));
                }
            })())),
        ];
    }
    toggleSignupContainer(value) {
        this.isSignup = value;
    }
};
LayoutLogin.style = layoutLoginCss;

const layoutMenuCss = ".ga-menu{position:absolute;top:1rem;right:1rem}limel-button{--lime-primary-color:#f49132}";

const LayoutMenu = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.changeView = index.createEvent(this, "changeView", 7);
        this.menuItems = [
            {
                text: 'Help',
                icon: 'ask_question',
                value: EnumViews.EnumViews.help,
            },
            {
                text: 'Settings',
                icon: 'settings',
                value: EnumViews.EnumViews.settings,
            },
            {
                text: 'Logout',
                icon: 'exit',
                value: EnumViews.EnumViews.logout,
            },
        ];
        this.isOpen = false;
        this.toggleMenu = this.toggleMenu.bind(this);
        this.handleBack = this.handleBack.bind(this);
        this.showBackButton = this.showBackButton.bind(this);
        this.previousViewOnClose = this.previousViewOnClose.bind(this);
        this.onNavigate = this.onNavigate.bind(this);
        this.onCancelMenu = this.onCancelMenu.bind(this);
    }
    render() {
        if (this.isSending) {
            return [];
        }
        if (this.showBackButton()) {
            return (index.h("limel-button", { class: "ga-menu", onClick: this.handleBack, label: "Back" }));
        }
        return (index.h("limel-menu", { class: "ga-menu", label: "Menu", items: this.menuItems, onCancel: this.onCancelMenu, onSelect: this.onNavigate, open: this.isOpen }, index.h("div", { slot: "trigger" }, index.h("limel-icon-button", { icon: "menu", onClick: this.toggleMenu }))));
    }
    toggleMenu() {
        this.isOpen = !this.isOpen;
    }
    handleBack() {
        this.changeView.emit(this.previousViewOnClose());
    }
    onNavigate(event) {
        this.changeView.emit(event.detail.value);
        this.isOpen = false;
    }
    onCancelMenu() {
        this.isOpen = false;
    }
    previousViewOnClose() {
        switch (this.activeView) {
            case EnumViews.EnumViews.videoLibrary:
                return EnumViews.EnumViews.sendDocument;
            case EnumViews.EnumViews.invite:
                return EnumViews.EnumViews.home;
            case EnumViews.EnumViews.help:
                return EnumViews.EnumViews.home;
            case EnumViews.EnumViews.settings:
                return EnumViews.EnumViews.home;
            case EnumViews.EnumViews.documentDetail:
                return EnumViews.EnumViews.home;
            case EnumViews.EnumViews.documentValidation:
                return EnumViews.EnumViews.sendDocument;
            default:
                return this.activeView;
        }
    }
    showBackButton() {
        switch (this.activeView) {
            case EnumViews.EnumViews.videoLibrary:
                return true;
            case EnumViews.EnumViews.invite:
                return true;
            case EnumViews.EnumViews.help:
                return true;
            case EnumViews.EnumViews.settings:
                return true;
            case EnumViews.EnumViews.documentDetail:
                return true;
            case EnumViews.EnumViews.documentValidation:
                return false;
            default:
                return false;
        }
    }
};
LayoutMenu.style = layoutMenuCss;

const layoutOverviewCss = ".main-layout{display:-ms-flexbox;display:flex;-ms-flex-direction:row;flex-direction:row;-ms-flex-wrap:wrap;flex-wrap:wrap;-ms-flex-pack:distribute;justify-content:space-around}@media (min-width: 1074px){.main-layout .send-new-document-container{width:65%}.main-layout .send-new-document-container .send-new-document-buttons{display:-ms-flexbox;display:flex;overflow:hidden;width:100%;-ms-flex-pack:distribute;justify-content:space-around;-ms-flex-wrap:wrap;flex-wrap:wrap}.main-layout .related-documents{margin-right:1rem;width:33%}}@media (max-width: 1075px){.main-layout .send-new-document-container{width:100%}.main-layout .related-documents{width:100%}}";

const LayoutOverview = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.documents = [];
    }
    render() {
        return [
            index.h("div", { class: "main-layout" }, index.h("div", { class: "send-new-document-container" }, index.h("h3", null, "Send new document"), index.h("div", { class: "send-new-document-buttons" }, index.h("send-new-document-button", { isSigning: true }), index.h("send-new-document-button", { isSigning: false }))), index.h("div", { class: "related-documents" }, index.h("h3", null, "Related documents"), this.isLoadingDocuments ? (index.h("ga-loader", null)) : (index.h("document-list", { documents: this.documents })))),
        ];
    }
};
LayoutOverview.style = layoutOverviewCss;

const layoutSelectFileCss = ".layout-select-file-container{max-height:60vh;overflow:auto}.layout-select-file-container .select-file-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}@media (min-width: 1074px){.layout-select-file-container .select-file-container .file-column{width:45%;padding:1rem}}@media (max-width: 1075px){.layout-select-file-container .select-file-container .file-column{width:100%}}";

var EnumSections;
(function (EnumSections) {
    EnumSections["None"] = "none";
    EnumSections["Template"] = "template";
    EnumSections["LimeDocuments"] = "limeDocuments";
})(EnumSections || (EnumSections = {}));
const LayoutSelectFile = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.setCustomFields = index.createEvent(this, "setCustomFields", 7);
        this.errorHandler = index.createEvent(this, "errorHandler", 7);
        this.customFields = [];
        this.isLoadingTemplates = false;
        this.templates = [];
        this.isLoadingFields = false;
        this.openSection = EnumSections.Template;
        this.loadTemplates = this.loadTemplates.bind(this);
        this.loadTemplateFields = this.loadTemplateFields.bind(this);
        this.loadLimeDocuments = this.loadLimeDocuments.bind(this);
        this.onChangeSection = this.onChangeSection.bind(this);
        this.setTemplates = this.setTemplates.bind(this);
        this.setLimeDocuments = this.setLimeDocuments.bind(this);
        this.setFields = this.setFields.bind(this);
    }
    render() {
        return [
            index.h("div", { class: "layout-select-file-container" }, index.h("h3", null, "Select file to send"), ",", index.h("div", { class: "select-file-container" }, index.h("div", { class: "file-column" }, index.h("limel-collapsible-section", { header: "Templates", isOpen: this.openSection === EnumSections.Template, onOpen: event => this.onChangeSection(event, EnumSections.Template), onClose: event => this.onChangeSection(event, EnumSections.None) }, index.h("template-list", { templates: this.templates, selectedTemplate: this.selectedTemplate, isLoading: this.isLoadingTemplates })), index.h("limel-collapsible-section", { header: "Lime documents", isOpen: this.openSection === EnumSections.LimeDocuments, onOpen: event => this.onChangeSection(event, EnumSections.LimeDocuments), onClose: event => this.onChangeSection(event, EnumSections.None) }, index.h("lime-document-list", { documents: this.limeDocuments, isLoading: this.isLoadingLimeDocuments }))), index.h("div", { class: "file-column" }, index.h("template-preview", { template: this.selectedTemplate, isLoading: this.isLoadingFields, session: this.session }), index.h("custom-fields", { template: this.selectedTemplate, customFields: this.customFields, isLoading: this.isLoadingFields }))), ","),
        ];
    }
    componentWillLoad() {
        this.loadTemplates();
        this.loadLimeDocuments();
    }
    onChangeSection(event, section) {
        event.stopPropagation();
        this.openSection = section;
    }
    async loadTemplates() {
        this.isLoadingTemplates = true;
        try {
            this.templates = await index$1.fetchTemplates(this.platform, this.session, this.selectedTemplate);
        }
        catch (e) {
            this.errorHandler.emit('Could not load templates from GetAccept...');
        }
        this.isLoadingTemplates = false;
    }
    async loadLimeDocuments() {
        this.isLoadingLimeDocuments = true;
        const { id: record_id, limetype } = this.context;
        try {
            this.limeDocuments = await index$1.fetchLimeDocuments(this.platform, limetype, record_id, this.selectedLimeDocument);
        }
        catch (e) {
            this.errorHandler.emit('Could not load related Lime documents...');
        }
        this.isLoadingLimeDocuments = false;
    }
    async loadTemplateFields() {
        if (!this.selectedTemplate) {
            this.customFields = [];
            this.setCustomFields.emit(this.customFields);
            return;
        }
        this.isLoadingFields = true;
        const { id: record_id, limetype } = this.context;
        try {
            const fields = await index$1.fetchTemplateFields(this.platform, this.session, limetype, record_id, this.selectedTemplate);
            this.setFields(fields);
        }
        catch (e) {
            this.errorHandler.emit('Could not fetch template fields from GetAccept...');
        }
        this.isLoadingFields = false;
    }
    setFields(fields) {
        const customFields = fields.map(this.mapField);
        this.setCustomFields.emit(customFields);
    }
    onChangeTemplate(data) {
        this.setTemplates(data);
        if (data) {
            this.loadTemplateFields();
        }
    }
    setTemplates(template) {
        this.templates = this.getSelectedListItems(this.templates, template);
    }
    onChangeDocument(data) {
        this.setLimeDocuments(data);
    }
    mapField(field) {
        return {
            value: field.field_value,
            id: field.field_id,
            label: field.field_label || field.field_value,
            is_editable: !!field.is_editable,
        };
    }
    setLimeDocuments(document) {
        this.limeDocuments = this.getSelectedListItems(this.limeDocuments, document);
    }
    getSelectedListItems(items, selectedItem) {
        return items.map((item) => {
            if (selectedItem && item.value === selectedItem.value) {
                return selectedItem;
            }
            return Object.assign(Object.assign({}, item), { selected: false });
        });
    }
    updateFieldValue(event) {
        const { id, value } = event.detail;
        const customFields = this.customFields.map(field => {
            return field.id === id ? Object.assign(Object.assign({}, field), { value }) : field;
        });
        this.setCustomFields.emit(customFields);
    }
    static get watchers() { return {
        "selectedTemplate": ["onChangeTemplate"],
        "selectedLimeDocument": ["onChangeDocument"]
    }; }
};
LayoutSelectFile.style = layoutSelectFileCss;

const layoutSelectRecipientCss = ".select-recipient-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap;max-height:60vh;overflow:auto}@media (min-width: 1074px){.select-recipient-container .recipient-container{width:45%;padding:1rem}.select-recipient-container .selected-recipient-container{width:45%;padding:1rem}}@media (max-width: 1075px){.select-recipient-container .recipient-container{width:100%}.select-recipient-container .selected-recipient-container{width:100%}}.recipient-list{list-style-type:none;padding:0;margin:0;max-height:50vh;overflow:auto}.recipient-toolbar{display:-ms-flexbox;display:flex;-ms-flex-pack:justify;justify-content:space-between;-ms-flex-align:center;align-items:center}.recipient-toolbar :first-child{-ms-flex-positive:1;flex-grow:1;margin-right:1.5rem}limel-switch{--lime-primary-color:#f49132}";

const LayoutSelectRecipient = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.updateDocumentRecipient = index.createEvent(this, "updateDocumentRecipient", 7);
        this.errorHandler = index.createEvent(this, "errorHandler", 7);
        this.selectedRecipientList = [];
        this.includeCoworkers = false;
        this.recipientList = [];
        this.selectRecipientHandler = this.selectRecipientHandler.bind(this);
        this.isAdded = this.isAdded.bind(this);
        this.onSearch = this.onSearch.bind(this);
        this.toggleIncludeCoworkers = this.toggleIncludeCoworkers.bind(this);
        this.fetchRecipients = this.fetchRecipients.bind(this);
    }
    componentWillLoad() {
        this.selectedRecipientList = this.document.recipients;
    }
    render() {
        return [
            index.h("div", { class: "select-recipient-container" }, index.h("div", { class: "recipient-container" }, index.h("h3", null, "Search Recipient"), index.h("div", { class: "recipient-toolbar" }, index.h("limel-input-field", { label: "Search recipient", value: this.searchTerm, onChange: this.onSearch }), index.h("limel-switch", { label: "Include coworkers", value: this.includeCoworkers, onChange: this.toggleIncludeCoworkers })), index.h("ul", { class: "recipient-list" }, this.recipientList.map(recipient => {
                if (!this.isAdded(recipient.lime_id)) {
                    return (index.h("recipient-item", { recipient: recipient, showAdd: true, onClick: () => {
                            this.selectRecipientHandler(recipient);
                        } }));
                }
            }))), index.h("div", { class: "selected-recipient-container" }, index.h("h3", null, "Added recipients"), index.h("selected-recipient-list", { recipients: this.selectedRecipientList, document: this.document }))),
        ];
    }
    selectRecipientHandler(recipient) {
        if (!!recipient.mobile || !!recipient.email) {
            this.selectedRecipientList = [
                ...this.selectedRecipientList,
                recipient,
            ];
            this.updateDocumentRecipient.emit(this
                .selectedRecipientList);
        }
        else {
            this.errorHandler.emit('A recipient needs to have a mobile number or an email address');
        }
    }
    removeRecipientHandler(recipient) {
        let rec = recipient.detail;
        this.selectedRecipientList = this.selectedRecipientList.filter(recipientData => {
            return recipientData.lime_id != rec.lime_id;
        });
        this.updateDocumentRecipient.emit(this
            .selectedRecipientList);
    }
    changeRecipientRoleHandler(recipient) {
        const recipientData = recipient.detail;
        const index = this.selectedRecipientList.findIndex(rec => rec.lime_id === recipientData.lime_id);
        this.selectedRecipientList[index] = recipientData;
        this.updateDocumentRecipient.emit(this
            .selectedRecipientList);
    }
    isAdded(recipientId) {
        return !!this.selectedRecipientList.find(recipient => recipient.lime_id === recipientId);
    }
    toggleIncludeCoworkers() {
        this.includeCoworkers = !this.includeCoworkers;
        this.fetchRecipients();
    }
    async onSearch(event) {
        this.searchTerm = event.detail;
        this.fetchRecipients();
    }
    async fetchRecipients() {
        const options = {
            params: {
                search: this.searchTerm,
                limit: '10',
                offset: '0',
            },
        };
        try {
            const persons = await this.fetchPersons(options);
            const coworkers = await this.fetchCoworkers(options, this.includeCoworkers);
            this.recipientList = [...persons, ...coworkers];
        }
        catch (e) {
            this.errorHandler.emit('Something went wrong while communicating with the server...');
        }
    }
    async fetchPersons(options) {
        const persons = await this.platform
            .get(index$1.PlatformServiceName.Http)
            .get('getaccept/persons', options);
        return persons.map(person => ({
            email: person.email,
            name: person.name,
            mobile: person.mobilephone || person.phone,
            limetype: 'person',
            lime_id: person.id,
            company: person.company,
        }));
    }
    async fetchCoworkers(options, includeCoworkers) {
        if (!includeCoworkers) {
            return [];
        }
        const coworkers = await this.platform
            .get(index$1.PlatformServiceName.Http)
            .get('getaccept/coworkers', options);
        return coworkers.map(coworker => ({
            mobile: coworker.mobilephone || coworker.phone,
            name: coworker.name,
            email: coworker.email,
            limetype: 'coworker',
            lime_id: coworker.id,
            company: coworker.company,
        }));
    }
};
LayoutSelectRecipient.style = layoutSelectRecipientCss;

const layoutSendDocumentCss = ".send-document-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}@media (min-width: 1074px){.send-document-container .send-document-prepare-container{width:calc(50% - 0.5rem);padding-right:0.5rem}.send-document-container .send-document-email-container{width:calc(50% - 0.5rem);padding-left:0.5rem}}@media (max-width: 1075px){.send-document-container .send-document-prepare-container{width:100%}.send-document-container .send-document-email-container{margin-top:1.5rem;width:100%}}.send-document-container .add-video-button{margin-bottom:0.5rem}.send-document-container .video-is-added{display:-ms-inline-flexbox;display:inline-flex;-ms-flex-align:center;align-items:center;margin-left:0.5rem;border-radius:1rem;cursor:pointer;background-color:#f5f5f5}.send-document-container .video-is-added .video-is-added-icon{padding:0.1rem;margin-right:0.5rem;background-color:#2dc990;color:#fff}.send-document-container .video-is-added .video-remove-icon{margin-left:0.5rem;padding:0.1rem;color:#ccc}.send-document-container .video-is-added:hover{background-color:#ccc}.send-document-container .video-is-added:hover .video-remove-icon{color:#212121}.send-document-container .video-remove-container{display:-ms-flexbox;display:flex;cursor:pointer}limel-button{--lime-primary-color:#f49132}limel-checkbox{--lime-primary-color:#f49132}limel-flex-container limel-input-field:first-child{-ms-flex:2;flex:2;margin-right:0.5rem}limel-flex-container limel-input-field:last-child{-ms-flex:1;flex:1;margin-left:0.5rem}";

const LayoutSendDocument = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.setNewDocumentName = index.createEvent(this, "setNewDocumentName", 7);
        this.setDocumentValue = index.createEvent(this, "setDocumentValue", 7);
        this.setIsSmsSending = index.createEvent(this, "setIsSmsSending", 7);
        this.setSmartReminder = index.createEvent(this, "setSmartReminder", 7);
        this.changeView = index.createEvent(this, "changeView", 7);
        this.removeVideo = index.createEvent(this, "removeVideo", 7);
        this.documentName = '';
        this.value = 0;
        this.smartReminder = false;
        this.sendLinkBySms = false;
        this.documentVideo = false;
        this.handleChangeDocumentName = this.handleChangeDocumentName.bind(this);
        this.handleChangeValue = this.handleChangeValue.bind(this);
        this.handleChangeSmartReminder = this.handleChangeSmartReminder.bind(this);
        this.handleChangeSendLinkBySms = this.handleChangeSendLinkBySms.bind(this);
        this.handleAddVideo = this.handleAddVideo.bind(this);
        this.handleRemoveVideo = this.handleRemoveVideo.bind(this);
    }
    componentWillLoad() {
        this.documentName = this.fileName();
        this.setNewDocumentName.emit(this.documentName);
        this.value = this.document.value || 0;
        this.smartReminder = this.document.is_reminder_sending;
        this.sendLinkBySms = this.document.is_sms_sending;
        this.documentVideo = this.document.video_id !== '';
    }
    componentDidUpdate() {
        this.value = this.document.value;
        this.documentName = this.document.name || this.fileName();
    }
    render() {
        return [
            index.h("div", { class: "send-document-container" }, index.h("div", { class: "send-document-prepare-container" }, index.h("h3", null, "Prepare sending"), index.h("limel-flex-container", { align: "stretch" }, index.h("limel-input-field", { label: "Document Name", value: this.documentName, onChange: this.handleChangeDocumentName }), index.h("limel-input-field", { label: "Value", value: this.value.toString(), onChange: this.handleChangeValue })), index.h("div", null, index.h("h4", null, "Document engagement"), this.documentVideo ? (index.h("div", null, index.h("div", { class: "video-is-added" }, index.h("limel-icon", { name: "tv_show", size: "large", class: "video-is-added-icon" }), index.h("span", null, "Video is added"), index.h("limel-icon", { class: "video-remove-icon", name: "multiply", size: "small", onClick: this.handleRemoveVideo })))) : (index.h("limel-button", { class: "add-video-button", primary: true, label: "Add Video introduction", onClick: this.handleAddVideo })), index.h("limel-checkbox", { label: "Send smart reminders", id: "SmartReminder", checked: this.smartReminder, onChange: this.handleChangeSmartReminder }), index.h("limel-checkbox", { label: "Send link by SMS", id: "SendLinkBySMS", checked: this.sendLinkBySms, onChange: this.handleChangeSendLinkBySms }))), index.h("div", { class: "send-document-email-container" }, index.h("create-email", { document: this.document }))),
        ];
    }
    fileName() {
        if (this.limeDocument) {
            return this.limeDocument.text;
        }
        else if (this.template) {
            return this.template.text;
        }
        else {
            return '';
        }
    }
    handleChangeDocumentName(event) {
        this.setNewDocumentName.emit(event.detail);
    }
    handleChangeValue(event) {
        this.setDocumentValue.emit(event.detail);
    }
    handleChangeSmartReminder(event) {
        this.setSmartReminder.emit(event.detail);
    }
    handleChangeSendLinkBySms(event) {
        this.setIsSmsSending.emit(event.detail);
    }
    handleAddVideo() {
        //should open select video view
        this.changeView.emit(EnumViews.EnumViews.videoLibrary);
    }
    handleRemoveVideo() {
        this.removeVideo.emit();
        this.documentVideo = false;
    }
};
LayoutSendDocument.style = layoutSendDocumentCss;

const layoutSettingsCss = ".settings-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}.settings-container .error{display:block;color:#f88987;margin-top:1rem}@media (min-width: 1074px){.settings-container .settings-column{width:45%;padding:1rem}}@media (max-width: 1075px){.settings-container .settings-column{width:100%}}.full-width{width:100%}";

const LayoutSettings = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.setSession = index.createEvent(this, "setSession", 7);
        this.error = '';
        this.onChangeEntity = this.onChangeEntity.bind(this);
        this.renderContent = this.renderContent.bind(this);
    }
    componentWillLoad() {
        this.entityOptions = this.entities.map((entity) => ({
            value: entity.id,
            text: entity.name,
        }));
        this.selectedEntity = this.entityOptions.find((entity) => {
            return entity.value === this.user.entity_id;
        });
    }
    render() {
        return [
            index.h("h3", null, "Settings"),
            index.h("div", { class: "settings-container" }, this.isLoading ? this.renderLoader() : this.renderContent()),
        ];
    }
    renderLoader() {
        return index.h("ga-loader", { class: "full-width" });
    }
    renderContent() {
        return [
            index.h("div", { class: "settings-column" }, index.h("h4", null, "My profile"), index.h("limel-flex-container", { justify: "center" }, index.h("profile-picture", { thumbUrl: this.user.thumb_url })), index.h("limel-input-field", { label: "Name", value: `${this.user.first_name} ${this.user.last_name}`, disabled: true }), index.h("limel-input-field", { label: "Title", value: this.user.title, disabled: true }), index.h("limel-input-field", { label: "Email", value: this.user.email, disabled: true }), index.h("limel-input-field", { label: "Phone", value: this.user.mobile, disabled: true }), index.h("limel-input-field", { label: "Role", value: this.user.role, disabled: true })),
            index.h("div", { class: "settings-column" }, index.h("h4", null, "Change entity"), index.h("limel-select", { class: "entity-selector", label: "Entity", value: this.selectedEntity, options: this.entityOptions, onChange: this.onChangeEntity, required: true }), this.renderError(this.error)),
        ];
    }
    renderError(error) {
        return error ? index.h("span", { class: "error" }, error) : '';
    }
    async onChangeEntity(event) {
        if (event.detail.value == this.selectedEntity.value) {
            return;
        }
        this.isLoading = true;
        const originalEntity = this.selectedEntity;
        this.selectedEntity = event.detail;
        try {
            const session = await index$1.switchEntity(this.selectedEntity.value, this.platform, this.session);
            this.setSession.emit(session);
        }
        catch (e) {
            this.error =
                'Could not switch entity. Please try again at a later time.';
            setTimeout(() => {
                this.error = '';
            }, 3000);
            this.selectedEntity = originalEntity;
        }
        this.isLoading = false;
    }
};
LayoutSettings.style = layoutSettingsCss;

const layoutValidateDocumentCss = ".document-error-list{padding:0;margin:0}.share-document-recipient-list{list-style-type:none;padding:0;margin:0}.validate-document-button-container{display:-ms-flexbox;display:flex;margin:2rem 0}.validate-document-button-container .send-button{padding-right:1rem}.action-buttons{margin-top:2rem}.action-buttons limel-button{margin-right:1rem}limel-button{--lime-primary-color:#f49132}";

const LayoutValidateDocument = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.documentCompleted = index.createEvent(this, "documentCompleted", 7);
        this.errorHandler = index.createEvent(this, "errorHandler", 7);
        this.isSendingDocument = index.createEvent(this, "isSendingDocument", 7);
        this.isSealed = false;
        this.isLoading = true;
        this.recipients = [];
        this.errorList = [];
        this.handleCreateDocument = this.handleCreateDocument.bind(this);
        this.sealDocument = this.sealDocument.bind(this);
        this.hasProperty = this.hasProperty.bind(this);
        this.openInNewTab = this.openInNewTab.bind(this);
        this.handleOpenGetAccept = this.handleOpenGetAccept.bind(this);
    }
    async componentWillLoad() {
        await this.validateDocument();
    }
    render() {
        return (index.h("div", null, (() => {
            if (this.isLoading) {
                return (index.h("ga-loader-with-text", { showText: this.isSending, text: "We are creating your document!" }));
            }
            else if (this.isSealed) {
                if (this.recipients.length > 0) {
                    return (index.h("div", { class: "share-document-container" }, index.h("h3", null, "Share document link:"), index.h("ul", { class: "share-document-recipient-list" }, this.recipients.map(recipient => {
                        return (index.h("share-document-link", { recipient: recipient }));
                    })), index.h("div", { class: "action-buttons" }, index.h("limel-button", { label: "Done", primary: true, onClick: () => {
                            this.documentCompleted.emit(false);
                        } }), index.h("limel-button", { label: "Open in GetAccept", primary: false, onClick: () => this.handleCreateDocument(false, true) }))));
                }
            }
            else {
                return (index.h("div", null, (() => {
                    if (this.errorList.length > 0) {
                        return (index.h("document-error-feedback", { document: this.document, errorList: this.errorList }));
                    }
                    else {
                        return (index.h("document-validate-info", { document: this.document }));
                    }
                })(), index.h("div", { class: "validate-document-button-container" }, (() => {
                    if (this.errorList.length === 0) {
                        return [
                            index.h("limel-button", { class: "send-button", label: "Send", primary: true, onClick: () => this.handleCreateDocument(true, false) }),
                            index.h("limel-button", { label: "Share document link", primary: false, onClick: () => this.handleCreateDocument(false, false) }),
                            index.h("limel-button", { label: "Open in GetAccept", primary: false, onClick: () => this.handleCreateDocument(false, true) }),
                        ];
                    }
                    else {
                        return (index.h("limel-button", { label: "Open in GetAccept", primary: false, onClick: () => this.handleCreateDocument(false, true) }));
                    }
                })())));
            }
        })()));
    }
    async hasTemplateRoles() {
        if (!this.template) {
            return false;
        }
        try {
            const data = await index$1.fetchDocumentDetails(this.platform, this.session, this.template.value);
            const roles = data.recipients.filter(recipient => recipient.status === '1');
            return roles.length > 0;
        }
        catch (e) {
            this.errorHandler.emit('Could not fetch template data from GetAccept');
            return false;
        }
    }
    async handleUploadDocument() {
        if (this.limeDocument) {
            const { data, success } = await index$1.uploadDocument(this.platform, this.session, this.limeDocument.value);
            if (success) {
                return data.file_id;
            }
            else {
                this.errorHandler.emit('Could not upload Lime document to GetAccept');
            }
        }
        return '';
    }
    async handleCreateDocument(send, openDocument) {
        this.toggleLoading(true);
        const file_ids = await this.handleUploadDocument();
        const documentData = Object.assign(Object.assign({}, this.document), { template_id: this.template ? this.template.value : '', custom_fields: this.template ? this.fields : [], file_ids, is_automatic_sending: send });
        const { data, success } = await index$1.createDocument(this.platform, this.session, documentData);
        if (!success) {
            this.errorHandler.emit('Could not create document. Make sure that all data is correctly supplied');
            this.toggleLoading(false);
            return;
        }
        if (openDocument) {
            const openUrl = `https://app.getaccept.com/document/edit/${data.id}`;
            this.openInNewTab(openUrl);
        }
        this.sentDocument = Object.assign({}, data);
        if (!send && !openDocument) {
            this.sealDocument(data.id);
        }
        else {
            this.toggleLoading(false);
            this.documentCompleted.emit(false);
        }
    }
    async sealDocument(documentId, attempt = 1) {
        const maxAttempts = 5;
        const timeout = 5000;
        const { data, success } = await index$1.sealDocument(this.platform, this.session, documentId);
        if (!success && attempt < maxAttempts) {
            return setTimeout(() => this.sealDocument(documentId, (attempt += 1)), timeout);
        }
        else if (!success && attempt >= maxAttempts) {
            this.errorHandler.emit('Could not seal document do to lengthy import. Try to open it in GetAccept and seal it from there.');
            this.toggleLoading(false);
            return;
        }
        this.toggleLoading(false);
        this.recipients = data.recipients.map(recipient => {
            return {
                name: recipient.fullname,
                document_url: recipient.document_url,
                role: recipient.role,
                email: recipient.email,
            };
        });
        this.documentCompleted.emit(true);
    }
    handleOpenGetAccept() {
        if (this.sentDocument) {
            const openUrl = `https://app.getaccept.com/document/view/${this.sentDocument.id}`;
            this.openInNewTab(openUrl);
        }
    }
    async validateDocument() {
        this.isLoading = true;
        if (!this.limeDocument && !this.template) {
            this.errorList.push({
                header: 'No document',
                title: 'You are missing a document.',
                icon: 'dog_tag',
                view: EnumViews.EnumViews.selectFile,
            });
        }
        if (this.document.recipients.length === 0) {
            this.errorList.push({
                header: 'No recipients',
                title: 'You need to add at least one recipient.',
                icon: 'user_male_circle',
                view: EnumViews.EnumViews.recipient,
            });
        }
        if (this.document.recipients.length > 0 &&
            this.document.is_signing &&
            !this.haveSigner()) {
            this.errorList.push({
                header: 'No signer',
                title: 'You need to add at least one signer when you are sending a documet for signing.',
                icon: 'autograph',
                view: EnumViews.EnumViews.recipient,
            });
        }
        if (this.document.recipients.length > 0 &&
            !this.document.is_sms_sending &&
            this.recipientsWithOnlyPhoneExists()) {
            this.errorList.push({
                header: 'Need to activate SMS sending',
                title: 'You need to activate SMS sendings due to recipients without email',
                icon: 'cell_phone',
                view: EnumViews.EnumViews.sendDocument,
            });
        }
        if (this.document.recipients.length > 0 &&
            this.recipientMissingEmailAndPhoneExists()) {
            this.errorList.push({
                header: 'Recipient missing contact information',
                title: 'One or many recipients are missing contact information',
                icon: 'about_us_male',
                view: EnumViews.EnumViews.recipient,
            });
        }
        if (await this.hasTemplateRoles()) {
            this.errorList.push({
                header: 'Template has unassigned roles',
                title: 'The process must be completed in GetAccept before sending.',
                icon: 'id_not_verified',
                view: EnumViews.EnumViews.selectFile,
            });
        }
        this.isLoading = false;
    }
    haveSigner() {
        let signers = this.document.recipients.filter(recipient => recipient.role === 'signer');
        return signers.length > 0;
    }
    recipientsWithOnlyPhoneExists() {
        return this.document.recipients.some(recipient => !recipient.email && recipient.mobile !== '');
    }
    recipientMissingEmailAndPhoneExists() {
        return this.document.recipients.some(recipient => !recipient.email && !recipient.mobile);
    }
    hasProperty(value) {
        return value ? 'Yes' : 'No';
    }
    openInNewTab(url) {
        this.toggleLoading(false);
        this.documentCompleted.emit();
        var win = window.open(url, '_blank');
        win.focus();
    }
    toggleLoading(value) {
        this.isLoading = value;
        this.isSendingDocument.emit(value);
    }
};
LayoutValidateDocument.style = layoutValidateDocumentCss;

const layoutVideoLibraryCss = ".video-list{display:-ms-flexbox;display:flex;-ms-flex-flow:row wrap;flex-flow:row wrap;-ms-flex-pack:start;justify-content:flex-start;-ms-flex-item-align:start;align-self:flex-start;list-style-type:none;padding:0;margin:0;width:100%}";

const LayoutVideoLibrary = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.changeView = index.createEvent(this, "changeView", 7);
        this.videos = [];
        this.isLoadingVideos = false;
        this.handelClose = this.handelClose.bind(this);
    }
    componentWillLoad() {
        this.loadVideos();
    }
    render() {
        return [
            index.h("div", { class: "video-library-container" }, index.h("h3", null, "Select a video"), index.h("p", null, "It will be present for the recipient when they open the document."), this.isLoadingVideos && index.h("ga-loader", null), index.h("ul", { class: "video-list" }, this.videos.map(video => {
                return index.h("video-thumb", { video: video });
            }))),
        ];
    }
    async loadVideos() {
        this.isLoadingVideos = true;
        const { videos } = await index$1.fetchVideos(this.platform, this.session);
        this.videos = videos.map((video) => {
            return {
                thumb_url: video.thumb_url,
                video_id: video.video_id,
                video_title: video.video_title,
                video_type: video.video_type,
                video_url: video.video_url,
            };
        });
        this.isLoadingVideos = false;
    }
    handelClose() {
        this.changeView.emit(EnumViews.EnumViews.sendDocument);
    }
};
LayoutVideoLibrary.style = layoutVideoLibraryCss;

const workflowProgressBarCss = ".progress-steps{display:-ms-flexbox;display:flex;-ms-flex-direction:row;flex-direction:row;list-style-type:none;padding:0;margin:0;-ms-flex-pack:center;justify-content:center}.progress-steps limel-icon{color:#f49132}.progress-steps .progress-action-button{margin:0 2.5rem;color:#f49132;font-size:0.7rem;text-transform:uppercase;font-weight:bolder;cursor:pointer}.progress-steps .progress-step{text-align:center;margin:0 1rem;text-align:center;margin:0 1rem;width:5rem;-ms-flex-wrap:wrap;flex-wrap:wrap;display:-ms-flexbox;display:flex;-ms-flex-pack:center;justify-content:center}.progress-steps .progress-step .progress-step-icon{display:-ms-flexbox;display:flex;-ms-flex-pack:center;justify-content:center;text-align:center;border-radius:50%;height:2em;width:2em;overflow:hidden;background-color:#f5f5f5;color:#f49132;cursor:pointer}.progress-steps .progress-step .progress-step-icon.active{background-color:#f49132;color:#fff}.progress-steps .progress-step .progress-step-text{font-size:0.55rem}";

const WorkflowProgressBar = class {
    constructor(hostRef) {
        index.registerInstance(this, hostRef);
        this.changeView = index.createEvent(this, "changeView", 7);
        this.changeViewHandlerPrevious = this.changeViewHandlerPrevious.bind(this);
        this.changeViewHandlerNext = this.changeViewHandlerNext.bind(this);
        this.changeViewSelectedStep = this.changeViewSelectedStep.bind(this);
    }
    render() {
        return (() => {
            if (this.isVisible) {
                return (index.h("ul", { class: "progress-steps" }, index.h("li", { class: "progress-action-button", onClick: this.changeViewHandlerPrevious }, "Back"), workflowSteps.workflowSteps.map((step, index$1) => {
                    let progessStep = 'progress-step-icon';
                    if (step.currentView === this.activeView) {
                        progessStep += ' active';
                    }
                    return (index.h("li", { class: "progress-step", onClick: () => this.changeViewSelectedStep(step.currentView) }, index.h("span", { class: progessStep }, index$1 + 1), index.h("span", { class: "progress-step-text" }, step.label)));
                }), index.h("li", { class: "progress-action-button", onClick: this.changeViewHandlerNext }, "Next")));
            }
        })();
    }
    changeViewHandlerPrevious() {
        let viewData = workflowSteps.workflowSteps.find(step => {
            return step.currentView === this.activeView;
        });
        this.changeView.emit(viewData.previousView);
    }
    changeViewHandlerNext() {
        let viewData = workflowSteps.workflowSteps.find(step => {
            return step.currentView === this.activeView;
        });
        this.changeView.emit(viewData.nextView);
    }
    changeViewSelectedStep(currentView) {
        this.changeView.emit(currentView);
    }
};
WorkflowProgressBar.style = workflowProgressBarCss;

exports.error_message = ErrorMessage;
exports.layout_document_details = LayoutDocumentDetails;
exports.layout_help = LayoutHelp;
exports.layout_login = LayoutLogin;
exports.layout_menu = LayoutMenu;
exports.layout_overview = LayoutOverview;
exports.layout_select_file = LayoutSelectFile;
exports.layout_select_recipient = LayoutSelectRecipient;
exports.layout_send_document = LayoutSendDocument;
exports.layout_settings = LayoutSettings;
exports.layout_validate_document = LayoutValidateDocument;
exports.layout_video_library = LayoutVideoLibrary;
exports.workflow_progress_bar = WorkflowProgressBar;
