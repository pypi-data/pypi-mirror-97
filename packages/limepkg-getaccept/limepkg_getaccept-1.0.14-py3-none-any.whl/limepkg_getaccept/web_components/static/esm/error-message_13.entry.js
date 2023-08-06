import { r as registerInstance, h, g as getElement, c as createEvent } from './index-570406ba.js';
import { E as EnumViews } from './EnumViews-26a35d6d.js';
import { c as fetchDocumentDetails, d as removeDocument, e as fetchTemplates, g as fetchLimeDocuments, h as fetchTemplateFields, P as PlatformServiceName, s as switchEntity, u as uploadDocument, i as createDocument, j as sealDocument, k as fetchVideos } from './index-20a727f3.js';
import { w as workflowSteps } from './workflow-steps-d9a63ffd.js';
import { m as moment, E as EnumDocumentStatuses } from './EnumDocumentStatuses-a9bc0ab7.js';

const ErrorMessage = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
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
            h("limel-snackbar", { message: this.message, timeout: this.timeout, actionText: "Ok" }),
        ];
    }
    triggerSnackbar() {
        const snackbar = this.host.shadowRoot.querySelector('limel-snackbar');
        snackbar.show();
    }
    get host() { return getElement(this); }
};

const layoutDocumentDetailsCss = ".document-details-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap;max-height:50vh;overflow:auto}.document-details-container .document-details-info-list{padding:0;margin:0;list-style-type:none}.document-details-container .document-details-info-list .document-detail-title{font-weight:bold}.document-details-container .document-details-action-buttons{margin-top:1rem}.document-details-container .document-details-action-buttons .document-details-action-button-remove{margin-left:1rem}@media (min-width: 1074px){.document-details-container .document-details-info{width:65%}.document-details-container .document-details-pages{width:33%}}@media (max-width: 1075px){.document-details-container .document-details-info{width:100%}.document-details-container .document-details-pages{width:100%}}limel-button{--lime-primary-color:#f49132}";

const LayoutDocumentDetails = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.changeView = createEvent(this, "changeView", 7);
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
            h("div", null, h("h3", null, "Document Details"), (() => {
                if (this.isLoading) {
                    return h("ga-loader", null);
                }
                else {
                    return (h("div", { class: "document-details-container" }, h("div", { class: "document-details-info" }, h("ul", { class: "document-details-info-list" }, h("li", null, h("span", { class: "document-detail-title" }, "Document name:"), ' ', this.documentData.name), h("li", null, h("span", { class: "document-detail-title" }, "Status:"), ' ', this.documentData.status), h("li", null, h("span", { class: "document-detail-title" }, "Deal value:"), ' ', this.documentData.value), h("li", null, h("span", { class: "document-detail-title" }, "Expiration date:"), ' ', this.documentData.expiration_date), h("li", null, h("span", { class: "document-detail-title" }, "Send date:"), ' ', this.documentData.send_date)), h("div", { class: "document-details-action-buttons" }, h("limel-button", { primary: true, label: "Open in GetAccept", onClick: this
                            .openDocumentIntGetAcceptHandler }), h("limel-button", { class: "document-details-action-button-remove", primary: false, label: "Remove document", onClick: this.removeDocumentHandler }))), h("div", { class: "document-details-pages" }, h("ul", null, this.documentData.pages.map(page => {
                        return (h("document-page-info", { documentId: this.documentData.id, session: this.session, page: page, totalTime: this.totalPageViewTime }));
                    })))));
                }
            })()),
        ];
    }
    async loadDocumentDetails() {
        //should load document details. Replace hard coded id with id from this.document.
        this.isLoading = true;
        const rawDocument = await fetchDocumentDetails(this.platform, this.session, this.documentId);
        this.documentData = {
            id: rawDocument.id,
            name: rawDocument.name,
            page_count: rawDocument.page_count,
            status: rawDocument.status,
            value: rawDocument.value,
            expiration_date: moment(rawDocument.expiration_date).format('YYYY-MM-DD'),
            send_date: this.getSendDate(rawDocument),
            pages: this.getDocumentPages(rawDocument),
        };
        this.totalPageViewTime = this.getTotalPageViewTime(rawDocument);
        this.isLoading = false;
    }
    getSendDate(rawDocument) {
        return ((rawDocument.send_date &&
            moment(rawDocument.send_date).format('YYYY-MM-DD')) ||
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
        const result = await removeDocument(this.platform, this.session, this.documentId);
        this.isLoading = false;
        if (result) {
            this.changeView.emit(EnumViews.home);
        }
    }
    openDocumentIntGetAcceptHandler() {
        const page = this.documentData.status === EnumDocumentStatuses.draft
            ? 'edit'
            : 'view';
        window.open(`https://app.getaccept.com/document/${page}/${this.documentData.id}`, '_blank');
    }
};
LayoutDocumentDetails.style = layoutDocumentDetailsCss;

const layoutHelpCss = ".help-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}.help-container .help-support{width:100%}.help-container .help-support .help-support-link{text-decoration:none;color:#212121}.help-container .help-support .support-links-list{list-style-type:none;padding:0;margin-top:1rem}.help-container .help-support .support-links-list li{display:-ms-flexbox;display:flex;margin-top:0.5rem}.help-container .help-support .support-links-list li a{text-decoration:none;color:#212121;margin-left:0.5rem}";

const LayoutHelp = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
    }
    render() {
        return [
            h("div", null, h("h3", null, "Help"), h("div", { class: "help-container" }, h("div", { class: "help-support" }, h("a", { class: "help-support-link", href: "https://www.getaccept.com/support" }, "Have any questions or just looking for someone to talk to. Our support are always there for you"), h("ul", { class: "support-links-list" }, h("li", null, h("limel-icon", { class: "support", name: "phone", size: "small" }), h("a", { href: "tel:+46406688158" }, "+46 40-668-81-58")), h("li", null, h("limel-icon", { class: "support", name: "email", size: "small" }), h("a", { href: "mailto:support@getaccept.com" }, "support@getaccept.com")))))),
        ];
    }
};
LayoutHelp.style = layoutHelpCss;

const layoutLoginCss = ".auth-container{display:-ms-flexbox;display:flex;height:100%;width:100%}.auth-container .login-container{width:25%;padding:1rem;border-right:1px solid #ccc}.auth-container .login-container.active{width:60%}.auth-container .signup-container{width:40%;padding:1rem}.auth-container .signup-container.active{width:75%}";

const LayoutLogin = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
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
            h("div", { class: "auth-container" }, h("div", { class: loginClass, onClick: () => this.toggleSignupContainer(false) }, h("h3", null, "Welcome Back"), h("ga-login", { platform: this.platform })), h("div", { class: signupClass, onClick: () => this.toggleSignupContainer(true) }, h("h3", null, "Create Account"), (() => {
                if (this.isSignup) {
                    return h("ga-signup", { platform: this.platform });
                }
                else {
                    return (h("limel-input-field", { label: "Email address", type: "email", value: "", trailingIcon: "filled_message" }));
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
        registerInstance(this, hostRef);
        this.changeView = createEvent(this, "changeView", 7);
        this.menuItems = [
            {
                text: 'Help',
                icon: 'ask_question',
                value: EnumViews.help,
            },
            {
                text: 'Settings',
                icon: 'settings',
                value: EnumViews.settings,
            },
            {
                text: 'Logout',
                icon: 'exit',
                value: EnumViews.logout,
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
            return (h("limel-button", { class: "ga-menu", onClick: this.handleBack, label: "Back" }));
        }
        return (h("limel-menu", { class: "ga-menu", label: "Menu", items: this.menuItems, onCancel: this.onCancelMenu, onSelect: this.onNavigate, open: this.isOpen }, h("div", { slot: "trigger" }, h("limel-icon-button", { icon: "menu", onClick: this.toggleMenu }))));
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
            case EnumViews.videoLibrary:
                return EnumViews.sendDocument;
            case EnumViews.invite:
                return EnumViews.home;
            case EnumViews.help:
                return EnumViews.home;
            case EnumViews.settings:
                return EnumViews.home;
            case EnumViews.documentDetail:
                return EnumViews.home;
            case EnumViews.documentValidation:
                return EnumViews.sendDocument;
            default:
                return this.activeView;
        }
    }
    showBackButton() {
        switch (this.activeView) {
            case EnumViews.videoLibrary:
                return true;
            case EnumViews.invite:
                return true;
            case EnumViews.help:
                return true;
            case EnumViews.settings:
                return true;
            case EnumViews.documentDetail:
                return true;
            case EnumViews.documentValidation:
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
        registerInstance(this, hostRef);
        this.documents = [];
    }
    render() {
        return [
            h("div", { class: "main-layout" }, h("div", { class: "send-new-document-container" }, h("h3", null, "Send new document"), h("div", { class: "send-new-document-buttons" }, h("send-new-document-button", { isSigning: true }), h("send-new-document-button", { isSigning: false }))), h("div", { class: "related-documents" }, h("h3", null, "Related documents"), this.isLoadingDocuments ? (h("ga-loader", null)) : (h("document-list", { documents: this.documents })))),
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
        registerInstance(this, hostRef);
        this.setCustomFields = createEvent(this, "setCustomFields", 7);
        this.errorHandler = createEvent(this, "errorHandler", 7);
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
            h("div", { class: "layout-select-file-container" }, h("h3", null, "Select file to send"), ",", h("div", { class: "select-file-container" }, h("div", { class: "file-column" }, h("limel-collapsible-section", { header: "Templates", isOpen: this.openSection === EnumSections.Template, onOpen: event => this.onChangeSection(event, EnumSections.Template), onClose: event => this.onChangeSection(event, EnumSections.None) }, h("template-list", { templates: this.templates, selectedTemplate: this.selectedTemplate, isLoading: this.isLoadingTemplates })), h("limel-collapsible-section", { header: "Lime documents", isOpen: this.openSection === EnumSections.LimeDocuments, onOpen: event => this.onChangeSection(event, EnumSections.LimeDocuments), onClose: event => this.onChangeSection(event, EnumSections.None) }, h("lime-document-list", { documents: this.limeDocuments, isLoading: this.isLoadingLimeDocuments }))), h("div", { class: "file-column" }, h("template-preview", { template: this.selectedTemplate, isLoading: this.isLoadingFields, session: this.session }), h("custom-fields", { template: this.selectedTemplate, customFields: this.customFields, isLoading: this.isLoadingFields }))), ","),
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
            this.templates = await fetchTemplates(this.platform, this.session, this.selectedTemplate);
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
            this.limeDocuments = await fetchLimeDocuments(this.platform, limetype, record_id, this.selectedLimeDocument);
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
            const fields = await fetchTemplateFields(this.platform, this.session, limetype, record_id, this.selectedTemplate);
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
        registerInstance(this, hostRef);
        this.updateDocumentRecipient = createEvent(this, "updateDocumentRecipient", 7);
        this.errorHandler = createEvent(this, "errorHandler", 7);
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
            h("div", { class: "select-recipient-container" }, h("div", { class: "recipient-container" }, h("h3", null, "Search Recipient"), h("div", { class: "recipient-toolbar" }, h("limel-input-field", { label: "Search recipient", value: this.searchTerm, onChange: this.onSearch }), h("limel-switch", { label: "Include coworkers", value: this.includeCoworkers, onChange: this.toggleIncludeCoworkers })), h("ul", { class: "recipient-list" }, this.recipientList.map(recipient => {
                if (!this.isAdded(recipient.lime_id)) {
                    return (h("recipient-item", { recipient: recipient, showAdd: true, onClick: () => {
                            this.selectRecipientHandler(recipient);
                        } }));
                }
            }))), h("div", { class: "selected-recipient-container" }, h("h3", null, "Added recipients"), h("selected-recipient-list", { recipients: this.selectedRecipientList, document: this.document }))),
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
            .get(PlatformServiceName.Http)
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
            .get(PlatformServiceName.Http)
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
        registerInstance(this, hostRef);
        this.setNewDocumentName = createEvent(this, "setNewDocumentName", 7);
        this.setDocumentValue = createEvent(this, "setDocumentValue", 7);
        this.setIsSmsSending = createEvent(this, "setIsSmsSending", 7);
        this.setSmartReminder = createEvent(this, "setSmartReminder", 7);
        this.changeView = createEvent(this, "changeView", 7);
        this.removeVideo = createEvent(this, "removeVideo", 7);
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
            h("div", { class: "send-document-container" }, h("div", { class: "send-document-prepare-container" }, h("h3", null, "Prepare sending"), h("limel-flex-container", { align: "stretch" }, h("limel-input-field", { label: "Document Name", value: this.documentName, onChange: this.handleChangeDocumentName }), h("limel-input-field", { label: "Value", value: this.value.toString(), onChange: this.handleChangeValue })), h("div", null, h("h4", null, "Document engagement"), this.documentVideo ? (h("div", null, h("div", { class: "video-is-added" }, h("limel-icon", { name: "tv_show", size: "large", class: "video-is-added-icon" }), h("span", null, "Video is added"), h("limel-icon", { class: "video-remove-icon", name: "multiply", size: "small", onClick: this.handleRemoveVideo })))) : (h("limel-button", { class: "add-video-button", primary: true, label: "Add Video introduction", onClick: this.handleAddVideo })), h("limel-checkbox", { label: "Send smart reminders", id: "SmartReminder", checked: this.smartReminder, onChange: this.handleChangeSmartReminder }), h("limel-checkbox", { label: "Send link by SMS", id: "SendLinkBySMS", checked: this.sendLinkBySms, onChange: this.handleChangeSendLinkBySms }))), h("div", { class: "send-document-email-container" }, h("create-email", { document: this.document }))),
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
        this.changeView.emit(EnumViews.videoLibrary);
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
        registerInstance(this, hostRef);
        this.setSession = createEvent(this, "setSession", 7);
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
            h("h3", null, "Settings"),
            h("div", { class: "settings-container" }, this.isLoading ? this.renderLoader() : this.renderContent()),
        ];
    }
    renderLoader() {
        return h("ga-loader", { class: "full-width" });
    }
    renderContent() {
        return [
            h("div", { class: "settings-column" }, h("h4", null, "My profile"), h("limel-flex-container", { justify: "center" }, h("profile-picture", { thumbUrl: this.user.thumb_url })), h("limel-input-field", { label: "Name", value: `${this.user.first_name} ${this.user.last_name}`, disabled: true }), h("limel-input-field", { label: "Title", value: this.user.title, disabled: true }), h("limel-input-field", { label: "Email", value: this.user.email, disabled: true }), h("limel-input-field", { label: "Phone", value: this.user.mobile, disabled: true }), h("limel-input-field", { label: "Role", value: this.user.role, disabled: true })),
            h("div", { class: "settings-column" }, h("h4", null, "Change entity"), h("limel-select", { class: "entity-selector", label: "Entity", value: this.selectedEntity, options: this.entityOptions, onChange: this.onChangeEntity, required: true }), this.renderError(this.error)),
        ];
    }
    renderError(error) {
        return error ? h("span", { class: "error" }, error) : '';
    }
    async onChangeEntity(event) {
        if (event.detail.value == this.selectedEntity.value) {
            return;
        }
        this.isLoading = true;
        const originalEntity = this.selectedEntity;
        this.selectedEntity = event.detail;
        try {
            const session = await switchEntity(this.selectedEntity.value, this.platform, this.session);
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
        registerInstance(this, hostRef);
        this.documentCompleted = createEvent(this, "documentCompleted", 7);
        this.errorHandler = createEvent(this, "errorHandler", 7);
        this.isSendingDocument = createEvent(this, "isSendingDocument", 7);
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
        return (h("div", null, (() => {
            if (this.isLoading) {
                return (h("ga-loader-with-text", { showText: this.isSending, text: "We are creating your document!" }));
            }
            else if (this.isSealed) {
                if (this.recipients.length > 0) {
                    return (h("div", { class: "share-document-container" }, h("h3", null, "Share document link:"), h("ul", { class: "share-document-recipient-list" }, this.recipients.map(recipient => {
                        return (h("share-document-link", { recipient: recipient }));
                    })), h("div", { class: "action-buttons" }, h("limel-button", { label: "Done", primary: true, onClick: () => {
                            this.documentCompleted.emit(false);
                        } }), h("limel-button", { label: "Open in GetAccept", primary: false, onClick: () => this.handleCreateDocument(false, true) }))));
                }
            }
            else {
                return (h("div", null, (() => {
                    if (this.errorList.length > 0) {
                        return (h("document-error-feedback", { document: this.document, errorList: this.errorList }));
                    }
                    else {
                        return (h("document-validate-info", { document: this.document }));
                    }
                })(), h("div", { class: "validate-document-button-container" }, (() => {
                    if (this.errorList.length === 0) {
                        return [
                            h("limel-button", { class: "send-button", label: "Send", primary: true, onClick: () => this.handleCreateDocument(true, false) }),
                            h("limel-button", { label: "Share document link", primary: false, onClick: () => this.handleCreateDocument(false, false) }),
                            h("limel-button", { label: "Open in GetAccept", primary: false, onClick: () => this.handleCreateDocument(false, true) }),
                        ];
                    }
                    else {
                        return (h("limel-button", { label: "Open in GetAccept", primary: false, onClick: () => this.handleCreateDocument(false, true) }));
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
            const data = await fetchDocumentDetails(this.platform, this.session, this.template.value);
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
            const { data, success } = await uploadDocument(this.platform, this.session, this.limeDocument.value);
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
        const { data, success } = await createDocument(this.platform, this.session, documentData);
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
        const { data, success } = await sealDocument(this.platform, this.session, documentId);
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
                view: EnumViews.selectFile,
            });
        }
        if (this.document.recipients.length === 0) {
            this.errorList.push({
                header: 'No recipients',
                title: 'You need to add at least one recipient.',
                icon: 'user_male_circle',
                view: EnumViews.recipient,
            });
        }
        if (this.document.recipients.length > 0 &&
            this.document.is_signing &&
            !this.haveSigner()) {
            this.errorList.push({
                header: 'No signer',
                title: 'You need to add at least one signer when you are sending a documet for signing.',
                icon: 'autograph',
                view: EnumViews.recipient,
            });
        }
        if (this.document.recipients.length > 0 &&
            !this.document.is_sms_sending &&
            this.recipientsWithOnlyPhoneExists()) {
            this.errorList.push({
                header: 'Need to activate SMS sending',
                title: 'You need to activate SMS sendings due to recipients without email',
                icon: 'cell_phone',
                view: EnumViews.sendDocument,
            });
        }
        if (this.document.recipients.length > 0 &&
            this.recipientMissingEmailAndPhoneExists()) {
            this.errorList.push({
                header: 'Recipient missing contact information',
                title: 'One or many recipients are missing contact information',
                icon: 'about_us_male',
                view: EnumViews.recipient,
            });
        }
        if (await this.hasTemplateRoles()) {
            this.errorList.push({
                header: 'Template has unassigned roles',
                title: 'The process must be completed in GetAccept before sending.',
                icon: 'id_not_verified',
                view: EnumViews.selectFile,
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
        registerInstance(this, hostRef);
        this.changeView = createEvent(this, "changeView", 7);
        this.videos = [];
        this.isLoadingVideos = false;
        this.handelClose = this.handelClose.bind(this);
    }
    componentWillLoad() {
        this.loadVideos();
    }
    render() {
        return [
            h("div", { class: "video-library-container" }, h("h3", null, "Select a video"), h("p", null, "It will be present for the recipient when they open the document."), this.isLoadingVideos && h("ga-loader", null), h("ul", { class: "video-list" }, this.videos.map(video => {
                return h("video-thumb", { video: video });
            }))),
        ];
    }
    async loadVideos() {
        this.isLoadingVideos = true;
        const { videos } = await fetchVideos(this.platform, this.session);
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
        this.changeView.emit(EnumViews.sendDocument);
    }
};
LayoutVideoLibrary.style = layoutVideoLibraryCss;

const workflowProgressBarCss = ".progress-steps{display:-ms-flexbox;display:flex;-ms-flex-direction:row;flex-direction:row;list-style-type:none;padding:0;margin:0;-ms-flex-pack:center;justify-content:center}.progress-steps limel-icon{color:#f49132}.progress-steps .progress-action-button{margin:0 2.5rem;color:#f49132;font-size:0.7rem;text-transform:uppercase;font-weight:bolder;cursor:pointer}.progress-steps .progress-step{text-align:center;margin:0 1rem;text-align:center;margin:0 1rem;width:5rem;-ms-flex-wrap:wrap;flex-wrap:wrap;display:-ms-flexbox;display:flex;-ms-flex-pack:center;justify-content:center}.progress-steps .progress-step .progress-step-icon{display:-ms-flexbox;display:flex;-ms-flex-pack:center;justify-content:center;text-align:center;border-radius:50%;height:2em;width:2em;overflow:hidden;background-color:#f5f5f5;color:#f49132;cursor:pointer}.progress-steps .progress-step .progress-step-icon.active{background-color:#f49132;color:#fff}.progress-steps .progress-step .progress-step-text{font-size:0.55rem}";

const WorkflowProgressBar = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.changeView = createEvent(this, "changeView", 7);
        this.changeViewHandlerPrevious = this.changeViewHandlerPrevious.bind(this);
        this.changeViewHandlerNext = this.changeViewHandlerNext.bind(this);
        this.changeViewSelectedStep = this.changeViewSelectedStep.bind(this);
    }
    render() {
        return (() => {
            if (this.isVisible) {
                return (h("ul", { class: "progress-steps" }, h("li", { class: "progress-action-button", onClick: this.changeViewHandlerPrevious }, "Back"), workflowSteps.map((step, index) => {
                    let progessStep = 'progress-step-icon';
                    if (step.currentView === this.activeView) {
                        progessStep += ' active';
                    }
                    return (h("li", { class: "progress-step", onClick: () => this.changeViewSelectedStep(step.currentView) }, h("span", { class: progessStep }, index + 1), h("span", { class: "progress-step-text" }, step.label)));
                }), h("li", { class: "progress-action-button", onClick: this.changeViewHandlerNext }, "Next")));
            }
        })();
    }
    changeViewHandlerPrevious() {
        let viewData = workflowSteps.find(step => {
            return step.currentView === this.activeView;
        });
        this.changeView.emit(viewData.previousView);
    }
    changeViewHandlerNext() {
        let viewData = workflowSteps.find(step => {
            return step.currentView === this.activeView;
        });
        this.changeView.emit(viewData.nextView);
    }
    changeViewSelectedStep(currentView) {
        this.changeView.emit(currentView);
    }
};
WorkflowProgressBar.style = workflowProgressBarCss;

export { ErrorMessage as error_message, LayoutDocumentDetails as layout_document_details, LayoutHelp as layout_help, LayoutLogin as layout_login, LayoutMenu as layout_menu, LayoutOverview as layout_overview, LayoutSelectFile as layout_select_file, LayoutSelectRecipient as layout_select_recipient, LayoutSendDocument as layout_send_document, LayoutSettings as layout_settings, LayoutValidateDocument as layout_validate_document, LayoutVideoLibrary as layout_video_library, WorkflowProgressBar as workflow_progress_bar };
