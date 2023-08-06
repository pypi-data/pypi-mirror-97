var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
import { r as registerInstance, c as createEvent, h, g as getElement } from './index-570406ba.js';
import { E as EnumViews } from './EnumViews-26a35d6d.js';
import { f as fetchMe, a as fetchEntity, b as fetchSentDocuments, r as refreshToken } from './index-20a727f3.js';
import { w as workflowSteps } from './workflow-steps-d9a63ffd.js';
var lwcGetacceptRootCss = "limel-dialog{--dialog-heading-icon-background-color:#f49132}limel-dialog .ga-body{overflow:auto;min-height:-webkit-min-content;min-height:-moz-min-content;min-height:min-content;margin-top:1rem}limel-dialog .ga-top-bar{position:-webkit-sticky;position:sticky;top:0;height:5rem;background-color:#fff;z-index:4;display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center;z-index:9}@media (min-width: 1074px){limel-dialog{--dialog-width:65rem;--dialog-height:40rem}}@media (max-width: 1075px){limel-dialog{--dialog-width:55rem;--dialog-height:40rem}}@media (min-width: 1800px){limel-dialog{--dialog-width:70rem;--dialog-height:60rem}}limel-button{--lime-primary-color:#f49132}.logo-container{height:2.2rem;width:10rem;margin-bottom:1rem;cursor:pointer;-webkit-transition:width 0.5s;transition:width 0.5s;overflow:hidden}.logo-container.compact{width:2.8rem}.logo-container:hover{opacity:0.8}.logo-container .logo{height:2.2rem}.close{display:block;position:absolute;right:-1rem;top:0rem;cursor:pointer}.close:hover{color:#eee}.actionpad-container{width:100%}.getaccept-button{width:100%;display:-ms-flexbox;display:flex;-ms-flex-pack:start;justify-content:start;-ms-flex-align:center;align-items:center;padding:0.425rem 0.875rem 0.425rem 0.875rem;border:none;border-radius:2rem;cursor:pointer;-webkit-transition:background 0.8s;transition:background 0.8s;background-position:center;font-size:0.8rem;font-weight:bold;color:#444;background:#eee}.getaccept-button:focus{outline:0}.getaccept-button:hover{background:#f5f5f5 radial-gradient(circle, transparent 1%, #f5f5f5 1%) center/15000%}.getaccept-button:active{background-color:white;background-size:100%;-webkit-transition:background 0s;transition:background 0s}.getaccept-button img{height:2rem;-ms-flex:0;flex:0}.getaccept-button .button-text{margin-left:0.5rem;-ms-flex:2;flex:2;text-align:left}.getaccept-button .document-count{margin-left:auto;display:-ms-flexbox;display:flex;-ms-flex-align:center;align-items:center}.getaccept-button .document-count limel-icon{margin-right:0.3rem}workflow-progress-bar{position:absolute;top:1.5rem;left:4rem;right:4rem}";
var Root = /** @class */ (function () {
    function class_1(hostRef) {
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
    class_1.prototype.componentWillLoad = function () {
        this.externalId = this.context.limetype + "_" + this.context.id;
        this.activeView = this.checkIfSessionExists
            ? EnumViews.home
            : EnumViews.login;
        if (this.session) {
            this.loadInitialData();
        }
        this.setDefaultDocumentData();
    };
    class_1.prototype.loadInitialData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, user, entities, e_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.loadSentDocuments();
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchMe(this.platform, this.session)];
                    case 2:
                        _a = _b.sent(), user = _a.user, entities = _a.entities;
                        this.user = user;
                        this.entities = entities;
                        return [3 /*break*/, 4];
                    case 3:
                        e_1 = _b.sent();
                        this.errorHandler.emit('Could not load user session. Try relogging');
                        return [3 /*break*/, 4];
                    case 4:
                        this.loadEntityDetails();
                        return [2 /*return*/];
                }
            });
        });
    };
    class_1.prototype.loadEntityDetails = function () {
        return __awaiter(this, void 0, void 0, function () {
            var entity, e_2;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, fetchEntity(this.platform, this.session)];
                    case 1:
                        entity = (_a.sent()).entity;
                        this.session.entity_id = entity.id;
                        this.documentData.email_send_message =
                            entity.email_send_message !== ''
                                ? entity.email_send_message
                                : entity.default_email_send_message;
                        this.documentData.email_send_subject =
                            entity.email_send_subject !== ''
                                ? entity.email_send_subject
                                : entity.default_email_send_subject;
                        return [3 /*break*/, 3];
                    case 2:
                        e_2 = _a.sent();
                        this.errorHandler.emit('Could not load user session. Try relogging');
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    class_1.prototype.render = function () {
        var _this = this;
        return [
            h("limel-flex-container", { class: "actionpad-container" }, h("button", { class: "getaccept-button", onClick: this.openDialog }, h("img", { src: "getaccept/logos/logo_only" }), h("span", { class: "button-text" }, "Send document"), this.renderDocumentCount(!!this.session))),
            h("limel-dialog", { open: this.isOpen, closingActions: { escapeKey: true, scrimClick: false }, onClose: function () {
                    _this.isOpen = false;
                } }, h("div", { class: "ga-top-bar" }, this.renderLogo(this.showWorkflow()), (function () {
                if (_this.activeView !== EnumViews.login) {
                    return [
                        h("limel-icon", { class: "close", name: 'cancel', size: "small", onClick: function () {
                                _this.isOpen = false;
                            } }),
                        h("layout-menu", { activeView: _this.activeView, isSending: _this.isSending }),
                        h("workflow-progress-bar", { isVisible: _this.showWorkflow(), activeView: _this.activeView }),
                    ];
                }
            })()), h("div", { class: "ga-body" }, this.renderLayout()), h("limel-button-group", { slot: "button" }, h("limel-button", { label: "Cancel", onClick: function () {
                    _this.isOpen = false;
                } })), h("error-message", { error: this.errorMessage })),
        ];
    };
    class_1.prototype.renderDocumentCount = function (hasSession) {
        if (hasSession) {
            return (h("span", { class: "document-count" }, h("limel-icon", { name: "file", size: "small" }), h("span", null, this.documents.length)));
        }
        return [];
    };
    class_1.prototype.renderLogo = function (compact) {
        var classes = "logo-container " + (compact ? 'compact' : '');
        return (h("div", { class: classes }, h("img", { onClick: this.handleLogoClick, src: "getaccept/logos/logo-inverted", class: "logo" })));
    };
    class_1.prototype.showWorkflow = function () {
        var _this = this;
        if (this.isSending || this.isSealed) {
            return false;
        }
        return workflowSteps.some(function (view) { return view.currentView === _this.activeView; });
    };
    class_1.prototype.renderLayout = function () {
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
    };
    class_1.prototype.logout = function () {
        localStorage.removeItem('getaccept_session');
        this.documents = [];
        this.activeView = EnumViews.login;
    };
    class_1.prototype.openDialog = function () {
        this.isOpen = true;
    };
    class_1.prototype.handleLogoClick = function () {
        this.activeView = this.checkIfSessionExists
            ? EnumViews.home
            : EnumViews.login;
    };
    class_1.prototype.loadSentDocuments = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, e_3;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.isLoadingDocuments = true;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        _a = this;
                        return [4 /*yield*/, fetchSentDocuments(this.platform, this.externalId, this.session)];
                    case 2:
                        _a.documents = _b.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        e_3 = _b.sent();
                        this.errorHandler.emit('Something went wrong while documents from GetAccept...');
                        return [3 /*break*/, 4];
                    case 4:
                        this.isLoadingDocuments = false;
                        return [2 /*return*/];
                }
            });
        });
    };
    class_1.prototype.changeViewHandler = function (view) {
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
    };
    class_1.prototype.setTemplate = function (event) {
        this.template = event.detail;
        this.documentData.name = event.detail.text;
        this.limeDocument = null;
        this.templateFields = [];
    };
    class_1.prototype.setLimeDocument = function (event) {
        this.limeDocument = event.detail;
        this.template = null;
        this.templateFields = [];
    };
    class_1.prototype.setCustomFields = function (event) {
        this.templateFields = event.detail;
    };
    class_1.prototype.updateDocumentRecipientHandler = function (recipients) {
        this.documentData.recipients = recipients.detail;
    };
    class_1.prototype.documentTypeHandler = function (isSigning) {
        this.documentData.is_signing = isSigning.detail;
    };
    class_1.prototype.setSessionHandler = function (sessionData) {
        this.setSessionData(sessionData.detail);
        this.activeView = EnumViews.home;
        this.loadInitialData();
    };
    class_1.prototype.setDocumentName = function (documentName) {
        this.documentData = Object.assign(Object.assign({}, this.documentData), { name: documentName.detail });
    };
    class_1.prototype.setDocumentValue = function (value) {
        this.documentData = Object.assign(Object.assign({}, this.documentData), { value: value.detail });
    };
    class_1.prototype.setDocumentSmartReminder = function (smartReminder) {
        this.documentData.is_reminder_sending = smartReminder.detail;
    };
    class_1.prototype.setDocumentIsSmsSending = function (isSmsSending) {
        this.documentData.is_sms_sending = isSmsSending.detail;
    };
    class_1.prototype.setDocumentEmailSubject = function (emailSendSubject) {
        this.documentData.email_send_subject = emailSendSubject.detail;
    };
    class_1.prototype.setDocumentEmailMessage = function (emailSendMessage) {
        this.documentData.email_send_message = emailSendMessage.detail;
    };
    class_1.prototype.validateDocumentHandler = function () {
        this.activeView = EnumViews.documentValidation;
    };
    class_1.prototype.openDocumentDetails = function (document) {
        this.activeView = EnumViews.documentDetail;
        this.documentId = document.detail.id;
    };
    class_1.prototype.setDocumentVideo = function (videoId) {
        this.documentData.video_id = videoId.detail;
        this.documentData.is_video = true;
    };
    class_1.prototype.removeDocumentVideo = function () {
        this.documentData.video_id = '';
        this.documentData.is_video = false;
    };
    class_1.prototype.setIsSending = function (isSending) {
        this.isSending = isSending.detail;
    };
    class_1.prototype.documentCompleted = function (isSealed) {
        this.setDefaultDocumentData();
        this.loadEntityDetails();
        this.isSealed = isSealed.detail;
        if (!this.isSealed) {
            this.activeView = EnumViews.home;
        }
        this.loadSentDocuments();
    };
    class_1.prototype.onError = function (event) {
        var _this = this;
        this.errorMessage = event.detail;
        setTimeout(function () { return (_this.errorMessage = ''); }, 100); // Needed for same consecutive error message
    };
    Object.defineProperty(class_1.prototype, "checkIfSessionExists", {
        get: function () {
            var storedSession = window.localStorage.getItem('getaccept_session');
            if (!!storedSession) {
                var sessionObj = JSON.parse(storedSession);
                //used to check if token should be refreshed or not.
                this.validateToken(sessionObj);
                this.session = sessionObj;
            }
            return !!storedSession;
        },
        enumerable: false,
        configurable: true
    });
    class_1.prototype.validateToken = function (session) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, data, success, storedSession, sessionObj;
            var _this = this;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0: return [4 /*yield*/, refreshToken(this.platform, session)];
                    case 1:
                        _a = _b.sent(), data = _a.data, success = _a.success;
                        if (success) {
                            storedSession = window.localStorage.getItem('getaccept_session');
                            if (!!storedSession) {
                                sessionObj = JSON.parse(storedSession);
                                sessionObj.expires_in = data.expires_in;
                                sessionObj.access_token = data.access_token;
                                this.setSessionData(sessionObj);
                            }
                        }
                        else {
                            this.errorMessage = 'Could not refresh token.';
                            setTimeout(function () { return (_this.errorMessage = ''); });
                        }
                        return [2 /*return*/, true];
                }
            });
        });
    };
    class_1.prototype.setSessionData = function (session) {
        window.localStorage.setItem('getaccept_session', JSON.stringify(session));
        this.session = session;
    };
    class_1.prototype.setDefaultDocumentData = function () {
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
    };
    Object.defineProperty(class_1.prototype, "element", {
        get: function () { return getElement(this); },
        enumerable: false,
        configurable: true
    });
    return class_1;
}());
Root.style = lwcGetacceptRootCss;
export { Root as lwc_getaccept_root };
