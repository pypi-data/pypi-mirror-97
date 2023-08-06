import { Component, h, Element, Prop, State, Listen, Event, } from '@stencil/core';
import { EnumViews } from '../../models/EnumViews';
import { fetchMe, fetchEntity, refreshToken, fetchSentDocuments, } from '../../services';
import { workflowSteps } from '../workflow-progress-bar/workflow-steps';
export class Root {
    constructor() {
        this.isOpen = false;
        this.entities = [];
        this.activeView = EnumViews.login;
        this.errorMessage = '';
        this.documents = [];
        this.isSending = false;
        this.openDialog = this.openDialog.bind(this);
        this.handleLogoClick = this.handleLogoClick.bind(this);
        this.renderLayout = this.renderLayout.bind(this);
        this.loadInitialData = this.loadInitialData.bind(this);
        this.loadSentDocuments = this.loadSentDocuments.bind(this);
        this.showWorkflow = this.showWorkflow.bind(this);
    }
    componentWillLoad() {
        this.externalId = `${this.context.limetype}_${this.context.id}`;
        this.activeView = this.checkIfSessionExists
            ? EnumViews.home
            : EnumViews.login;
        if (this.session) {
            this.loadInitialData();
        }
        this.setDefaultDocumentData();
    }
    async loadInitialData() {
        this.loadSentDocuments();
        try {
            const { user, entities } = await fetchMe(this.platform, this.session);
            this.user = user;
            this.entities = entities;
        }
        catch (e) {
            this.errorHandler.emit('Could not load user session. Try relogging');
        }
        this.loadEntityDetails();
    }
    async loadEntityDetails() {
        try {
            const { entity } = await fetchEntity(this.platform, this.session);
            this.session.entity_id = entity.id;
            this.documentData.email_send_message =
                entity.email_send_message !== ''
                    ? entity.email_send_message
                    : entity.default_email_send_message;
            this.documentData.email_send_subject =
                entity.email_send_subject !== ''
                    ? entity.email_send_subject
                    : entity.default_email_send_subject;
        }
        catch (e) {
            this.errorHandler.emit('Could not load user session. Try relogging');
        }
    }
    render() {
        return [
            h("limel-flex-container", { class: "actionpad-container" },
                h("button", { class: "getaccept-button", onClick: this.openDialog },
                    h("img", { src: "getaccept/logos/logo_only" }),
                    h("span", { class: "button-text" }, "Send document"),
                    this.renderDocumentCount(!!this.session))),
            h("limel-dialog", { open: this.isOpen, closingActions: { escapeKey: true, scrimClick: false }, onClose: () => {
                    this.isOpen = false;
                } },
                h("div", { class: "ga-top-bar" },
                    this.renderLogo(this.showWorkflow()),
                    (() => {
                        if (this.activeView !== EnumViews.login) {
                            return [
                                h("limel-icon", { class: "close", name: 'cancel', size: "small", onClick: () => {
                                        this.isOpen = false;
                                    } }),
                                h("layout-menu", { activeView: this.activeView, isSending: this.isSending }),
                                h("workflow-progress-bar", { isVisible: this.showWorkflow(), activeView: this.activeView }),
                            ];
                        }
                    })()),
                h("div", { class: "ga-body" }, this.renderLayout()),
                h("limel-button-group", { slot: "button" },
                    h("limel-button", { label: "Cancel", onClick: () => {
                            this.isOpen = false;
                        } })),
                h("error-message", { error: this.errorMessage })),
        ];
    }
    renderDocumentCount(hasSession) {
        if (hasSession) {
            return (h("span", { class: "document-count" },
                h("limel-icon", { name: "file", size: "small" }),
                h("span", null, this.documents.length)));
        }
        return [];
    }
    renderLogo(compact) {
        const classes = `logo-container ${compact ? 'compact' : ''}`;
        return (h("div", { class: classes },
            h("img", { onClick: this.handleLogoClick, src: "getaccept/logos/logo-inverted", class: "logo" })));
    }
    showWorkflow() {
        if (this.isSending || this.isSealed) {
            return false;
        }
        return workflowSteps.some(view => view.currentView === this.activeView);
    }
    renderLayout() {
        switch (this.activeView) {
            case EnumViews.home:
                return (h("layout-overview", { platform: this.platform, session: this.session, externalId: this.externalId, documents: this.documents }));
            case EnumViews.login:
                return h("layout-login", { platform: this.platform });
            case EnumViews.selectFile:
                return (h("layout-select-file", { platform: this.platform, session: this.session, context: this.context, selectedLimeDocument: this.limeDocument, selectedTemplate: this.template, customFields: this.templateFields }));
            case EnumViews.recipient:
                return (h("layout-select-recipient", { platform: this.platform, document: this.documentData }));
            case EnumViews.settings:
                return (h("layout-settings", { user: this.user, entities: this.entities, session: this.session, platform: this.platform }));
            case EnumViews.help:
                return h("layout-help", null);
            case EnumViews.sendDocument:
                return (h("layout-send-document", { document: this.documentData, limeDocument: this.limeDocument, template: this.template }));
            case EnumViews.videoLibrary:
                return (h("layout-video-library", { platform: this.platform, session: this.session }));
            case EnumViews.documentDetail:
                return (h("layout-document-details", { platform: this.platform, session: this.session, documentId: this.documentId }));
            case EnumViews.documentValidation:
                return (h("layout-validate-document", { platform: this.platform, session: this.session, document: this.documentData, limeDocument: this.limeDocument, template: this.template, fields: this.templateFields, isSealed: this.isSealed, isSending: this.isSending }));
            default:
                return h("layout-overview", null);
        }
    }
    logout() {
        localStorage.removeItem('getaccept_session');
        this.documents = [];
        this.activeView = EnumViews.login;
    }
    openDialog() {
        this.isOpen = true;
    }
    handleLogoClick() {
        this.activeView = this.checkIfSessionExists
            ? EnumViews.home
            : EnumViews.login;
    }
    async loadSentDocuments() {
        this.isLoadingDocuments = true;
        try {
            this.documents = await fetchSentDocuments(this.platform, this.externalId, this.session);
        }
        catch (e) {
            this.errorHandler.emit('Something went wrong while documents from GetAccept...');
        }
        this.isLoadingDocuments = false;
    }
    changeViewHandler(view) {
        if (view.detail === EnumViews.logout) {
            this.logout();
        }
        else if (this.isSealed) {
            this.activeView = EnumViews.home;
            this.setDefaultDocumentData();
        }
        else {
            this.activeView = view.detail;
        }
    }
    setTemplate(event) {
        this.template = event.detail;
        this.documentData.name = event.detail.text;
        this.limeDocument = null;
        this.templateFields = [];
    }
    setLimeDocument(event) {
        this.limeDocument = event.detail;
        this.template = null;
        this.templateFields = [];
    }
    setCustomFields(event) {
        this.templateFields = event.detail;
    }
    updateDocumentRecipientHandler(recipients) {
        this.documentData.recipients = recipients.detail;
    }
    documentTypeHandler(isSigning) {
        this.documentData.is_signing = isSigning.detail;
    }
    setSessionHandler(sessionData) {
        this.setSessionData(sessionData.detail);
        this.activeView = EnumViews.home;
        this.loadInitialData();
    }
    setDocumentName(documentName) {
        this.documentData = Object.assign(Object.assign({}, this.documentData), { name: documentName.detail });
    }
    setDocumentValue(value) {
        this.documentData = Object.assign(Object.assign({}, this.documentData), { value: value.detail });
    }
    setDocumentSmartReminder(smartReminder) {
        this.documentData.is_reminder_sending = smartReminder.detail;
    }
    setDocumentIsSmsSending(isSmsSending) {
        this.documentData.is_sms_sending = isSmsSending.detail;
    }
    setDocumentEmailSubject(emailSendSubject) {
        this.documentData.email_send_subject = emailSendSubject.detail;
    }
    setDocumentEmailMessage(emailSendMessage) {
        this.documentData.email_send_message = emailSendMessage.detail;
    }
    validateDocumentHandler() {
        this.activeView = EnumViews.documentValidation;
    }
    openDocumentDetails(document) {
        this.activeView = EnumViews.documentDetail;
        this.documentId = document.detail.id;
    }
    setDocumentVideo(videoId) {
        this.documentData.video_id = videoId.detail;
        this.documentData.is_video = true;
    }
    removeDocumentVideo() {
        this.documentData.video_id = '';
        this.documentData.is_video = false;
    }
    setIsSending(isSending) {
        this.isSending = isSending.detail;
    }
    documentCompleted(isSealed) {
        this.setDefaultDocumentData();
        this.loadEntityDetails();
        this.isSealed = isSealed.detail;
        if (!this.isSealed) {
            this.activeView = EnumViews.home;
        }
        this.loadSentDocuments();
    }
    onError(event) {
        this.errorMessage = event.detail;
        setTimeout(() => (this.errorMessage = ''), 100); // Needed for same consecutive error message
    }
    get checkIfSessionExists() {
        let storedSession = window.localStorage.getItem('getaccept_session');
        if (!!storedSession) {
            const sessionObj = JSON.parse(storedSession);
            //used to check if token should be refreshed or not.
            this.validateToken(sessionObj);
            this.session = sessionObj;
        }
        return !!storedSession;
    }
    async validateToken(session) {
        const { data, success } = await refreshToken(this.platform, session);
        if (success) {
            let storedSession = window.localStorage.getItem('getaccept_session');
            if (!!storedSession) {
                const sessionObj = JSON.parse(storedSession);
                sessionObj.expires_in = data.expires_in;
                sessionObj.access_token = data.access_token;
                this.setSessionData(sessionObj);
            }
        }
        else {
            this.errorMessage = 'Could not refresh token.';
            setTimeout(() => (this.errorMessage = ''));
        }
        return true;
    }
    setSessionData(session) {
        window.localStorage.setItem('getaccept_session', JSON.stringify(session));
        this.session = session;
    }
    setDefaultDocumentData() {
        this.documentData = {
            is_signing: false,
            name: '',
            recipients: [],
            template_id: '',
            custom_fields: [],
            is_reminder_sending: false,
            is_sms_sending: false,
            email_send_subject: '',
            email_send_message: '',
            video_id: '',
            is_video: false,
            external_id: this.externalId,
            value: 0,
        };
        this.templateFields = [];
        this.isSealed = false;
        this.template = null;
        this.limeDocument = null;
    }
    static get is() { return "lwc-getaccept-root"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["lwc-getaccept-root.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["lwc-getaccept-root.css"]
    }; }
    static get properties() { return {
        "platform": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "LimeWebComponentPlatform",
                "resolved": "LimeWebComponentPlatform",
                "references": {
                    "LimeWebComponentPlatform": {
                        "location": "import",
                        "path": "@limetech/lime-web-components-interfaces"
                    }
                }
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": "Reference to the platform"
            }
        },
        "context": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "LimeWebComponentContext",
                "resolved": "LimeWebComponentContext",
                "references": {
                    "LimeWebComponentContext": {
                        "location": "import",
                        "path": "@limetech/lime-web-components-interfaces"
                    }
                }
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": "The context this component belongs to"
            }
        }
    }; }
    static get states() { return {
        "externalId": {},
        "isOpen": {},
        "session": {},
        "user": {},
        "entities": {},
        "documentId": {},
        "activeView": {},
        "documentData": {},
        "isSealed": {},
        "template": {},
        "limeDocument": {},
        "templateFields": {},
        "errorMessage": {},
        "documents": {},
        "isLoadingDocuments": {},
        "isSending": {}
    }; }
    static get events() { return [{
            "method": "errorHandler",
            "name": "errorHandler",
            "bubbles": true,
            "cancelable": true,
            "composed": true,
            "docs": {
                "tags": [],
                "text": ""
            },
            "complexType": {
                "original": "string",
                "resolved": "string",
                "references": {}
            }
        }]; }
    static get elementRef() { return "element"; }
    static get listeners() { return [{
            "name": "changeView",
            "method": "changeViewHandler",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "setTemplate",
            "method": "setTemplate",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "setLimeDocument",
            "method": "setLimeDocument",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "setCustomFields",
            "method": "setCustomFields",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "updateDocumentRecipient",
            "method": "updateDocumentRecipientHandler",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "setDocumentType",
            "method": "documentTypeHandler",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "setSession",
            "method": "setSessionHandler",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "setNewDocumentName",
            "method": "setDocumentName",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "setDocumentValue",
            "method": "setDocumentValue",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "setSmartReminder",
            "method": "setDocumentSmartReminder",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "setIsSmsSending",
            "method": "setDocumentIsSmsSending",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "setEmailSubject",
            "method": "setDocumentEmailSubject",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "setEmailMessage",
            "method": "setDocumentEmailMessage",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "validateDocument",
            "method": "validateDocumentHandler",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "openDocument",
            "method": "openDocumentDetails",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "setVideo",
            "method": "setDocumentVideo",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "removeVideo",
            "method": "removeDocumentVideo",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "isSendingDocument",
            "method": "setIsSending",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "documentCompleted",
            "method": "documentCompleted",
            "target": undefined,
            "capture": false,
            "passive": false
        }, {
            "name": "errorHandler",
            "method": "onError",
            "target": undefined,
            "capture": false,
            "passive": false
        }]; }
}
