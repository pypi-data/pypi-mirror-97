import { r as registerInstance, c as createEvent, h, g as getElement } from './index-570406ba.js';
import { E as EnumViews } from './EnumViews-26a35d6d.js';
import { f as fetchMe, a as fetchEntity, b as fetchSentDocuments, r as refreshToken } from './index-20a727f3.js';
import { w as workflowSteps } from './workflow-steps-d9a63ffd.js';

const lwcGetacceptRootCss = "limel-dialog{--dialog-heading-icon-background-color:#f49132}limel-dialog .ga-body{overflow:auto;min-height:-webkit-min-content;min-height:-moz-min-content;min-height:min-content;margin-top:1rem}limel-dialog .ga-top-bar{position:-webkit-sticky;position:sticky;top:0;height:5rem;background-color:#fff;z-index:4;display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;z-index:9}@media (min-width: 1074px){limel-dialog{--dialog-width:65rem;--dialog-height:40rem}}@media (max-width: 1075px){limel-dialog{--dialog-width:55rem;--dialog-height:40rem}}@media (min-width: 1800px){limel-dialog{--dialog-width:70rem;--dialog-height:60rem}}limel-button{--lime-primary-color:#f49132}.logo-container{height:2.2rem;width:10rem;margin-bottom:1rem;cursor:pointer;-webkit-transition:width 0.5s;transition:width 0.5s;overflow:hidden}.logo-container.compact{width:2.8rem}.logo-container:hover{opacity:0.8}.logo-container .logo{height:2.2rem}.close{display:block;position:absolute;right:-1rem;top:0rem;cursor:pointer}.close:hover{color:#eee}.actionpad-container{width:100%}.getaccept-button{width:100%;display:-ms-flexbox;display:flex;-ms-flex-pack:start;justify-content:start;-ms-flex-align:center;align-items:center;padding:0.425rem 0.875rem 0.425rem 0.875rem;border:none;border-radius:2rem;cursor:pointer;-webkit-transition:background 0.8s;transition:background 0.8s;background-position:center;font-size:0.8rem;font-weight:bold;color:#444;background:#eee}.getaccept-button:focus{outline:0}.getaccept-button:hover{background:#f5f5f5 radial-gradient(circle, transparent 1%, #f5f5f5 1%) center/15000%}.getaccept-button:active{background-color:white;background-size:100%;-webkit-transition:background 0s;transition:background 0s}.getaccept-button img{height:2rem;-ms-flex:0;flex:0}.getaccept-button .button-text{margin-left:0.5rem;-ms-flex:2;flex:2;text-align:left}.getaccept-button .document-count{margin-left:auto;display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center}.getaccept-button .document-count limel-icon{margin-right:0.3rem}workflow-progress-bar{position:absolute;top:1.5rem;left:4rem;right:4rem}";

const Root = class {
    constructor(hostRef) {
        registerInstance(this, hostRef);
        this.errorHandler = createEvent(this, "errorHandler", 7);
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
            h("limel-flex-container", { class: "actionpad-container" }, h("button", { class: "getaccept-button", onClick: this.openDialog }, h("img", { src: "getaccept/logos/logo_only" }), h("span", { class: "button-text" }, "Send document"), this.renderDocumentCount(!!this.session))),
            h("limel-dialog", { open: this.isOpen, closingActions: { escapeKey: true, scrimClick: false }, onClose: () => {
                    this.isOpen = false;
                } }, h("div", { class: "ga-top-bar" }, this.renderLogo(this.showWorkflow()), (() => {
                if (this.activeView !== EnumViews.login) {
                    return [
                        h("limel-icon", { class: "close", name: 'cancel', size: "small", onClick: () => {
                                this.isOpen = false;
                            } }),
                        h("layout-menu", { activeView: this.activeView, isSending: this.isSending }),
                        h("workflow-progress-bar", { isVisible: this.showWorkflow(), activeView: this.activeView }),
                    ];
                }
            })()), h("div", { class: "ga-body" }, this.renderLayout()), h("limel-button-group", { slot: "button" }, h("limel-button", { label: "Cancel", onClick: () => {
                    this.isOpen = false;
                } })), h("error-message", { error: this.errorMessage })),
        ];
    }
    renderDocumentCount(hasSession) {
        if (hasSession) {
            return (h("span", { class: "document-count" }, h("limel-icon", { name: "file", size: "small" }), h("span", null, this.documents.length)));
        }
        return [];
    }
    renderLogo(compact) {
        const classes = `logo-container ${compact ? 'compact' : ''}`;
        return (h("div", { class: classes }, h("img", { onClick: this.handleLogoClick, src: "getaccept/logos/logo-inverted", class: "logo" })));
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
    get element() { return getElement(this); }
};
Root.style = lwcGetacceptRootCss;

export { Root as lwc_getaccept_root };
