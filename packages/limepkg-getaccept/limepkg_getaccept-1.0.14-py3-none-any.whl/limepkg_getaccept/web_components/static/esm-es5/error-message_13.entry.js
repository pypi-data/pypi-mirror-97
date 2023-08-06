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
var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
import { r as registerInstance, h, g as getElement, c as createEvent } from './index-570406ba.js';
import { E as EnumViews } from './EnumViews-26a35d6d.js';
import { c as fetchDocumentDetails, d as removeDocument, e as fetchTemplates, g as fetchLimeDocuments, h as fetchTemplateFields, P as PlatformServiceName, s as switchEntity, u as uploadDocument, i as createDocument, j as sealDocument, k as fetchVideos } from './index-20a727f3.js';
import { w as workflowSteps } from './workflow-steps-d9a63ffd.js';
import { m as moment, E as EnumDocumentStatuses } from './EnumDocumentStatuses-a9bc0ab7.js';
var ErrorMessage = /** @class */ (function () {
    function ErrorMessage(hostRef) {
        registerInstance(this, hostRef);
        this.timeout = 10000;
        this.error = '';
        this.message = '';
        this.triggerSnackbar = this.triggerSnackbar.bind(this);
    }
    ErrorMessage.prototype.componentDidUpdate = function () {
        if (this.error) {
            this.message = this.error;
            this.triggerSnackbar();
        }
    };
    ErrorMessage.prototype.render = function () {
        return [
            h("limel-snackbar", { message: this.message, timeout: this.timeout, actionText: "Ok" }),
        ];
    };
    ErrorMessage.prototype.triggerSnackbar = function () {
        var snackbar = this.host.shadowRoot.querySelector('limel-snackbar');
        snackbar.show();
    };
    Object.defineProperty(ErrorMessage.prototype, "host", {
        get: function () { return getElement(this); },
        enumerable: false,
        configurable: true
    });
    return ErrorMessage;
}());
var layoutDocumentDetailsCss = ".document-details-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap;max-height:50vh;overflow:auto}.document-details-container .document-details-info-list{padding:0;margin:0;list-style-type:none}.document-details-container .document-details-info-list .document-detail-title{font-weight:bold}.document-details-container .document-details-action-buttons{margin-top:1rem}.document-details-container .document-details-action-buttons .document-details-action-button-remove{margin-left:1rem}@media (min-width: 1074px){.document-details-container .document-details-info{width:65%}.document-details-container .document-details-pages{width:33%}}@media (max-width: 1075px){.document-details-container .document-details-info{width:100%}.document-details-container .document-details-pages{width:100%}}limel-button{--lime-primary-color:#f49132}";
var LayoutDocumentDetails = /** @class */ (function () {
    function class_1(hostRef) {
        registerInstance(this, hostRef);
        this.changeView = createEvent(this, "changeView", 7);
        this.documentData = {};
        this.isLoading = false;
        this.removeDocumentHandler = this.removeDocumentHandler.bind(this);
        this.openDocumentIntGetAcceptHandler = this.openDocumentIntGetAcceptHandler.bind(this);
    }
    class_1.prototype.componentWillLoad = function () {
        this.loadDocumentDetails();
    };
    class_1.prototype.render = function () {
        var _this = this;
        return [
            h("div", null, h("h3", null, "Document Details"), (function () {
                if (_this.isLoading) {
                    return h("ga-loader", null);
                }
                else {
                    return (h("div", { class: "document-details-container" }, h("div", { class: "document-details-info" }, h("ul", { class: "document-details-info-list" }, h("li", null, h("span", { class: "document-detail-title" }, "Document name:"), ' ', _this.documentData.name), h("li", null, h("span", { class: "document-detail-title" }, "Status:"), ' ', _this.documentData.status), h("li", null, h("span", { class: "document-detail-title" }, "Deal value:"), ' ', _this.documentData.value), h("li", null, h("span", { class: "document-detail-title" }, "Expiration date:"), ' ', _this.documentData.expiration_date), h("li", null, h("span", { class: "document-detail-title" }, "Send date:"), ' ', _this.documentData.send_date)), h("div", { class: "document-details-action-buttons" }, h("limel-button", { primary: true, label: "Open in GetAccept", onClick: _this
                            .openDocumentIntGetAcceptHandler }), h("limel-button", { class: "document-details-action-button-remove", primary: false, label: "Remove document", onClick: _this.removeDocumentHandler }))), h("div", { class: "document-details-pages" }, h("ul", null, _this.documentData.pages.map(function (page) {
                        return (h("document-page-info", { documentId: _this.documentData.id, session: _this.session, page: page, totalTime: _this.totalPageViewTime }));
                    })))));
                }
            })()),
        ];
    };
    class_1.prototype.loadDocumentDetails = function () {
        return __awaiter(this, void 0, void 0, function () {
            var rawDocument;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        //should load document details. Replace hard coded id with id from this.document.
                        this.isLoading = true;
                        return [4 /*yield*/, fetchDocumentDetails(this.platform, this.session, this.documentId)];
                    case 1:
                        rawDocument = _a.sent();
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
                        return [2 /*return*/];
                }
            });
        });
    };
    class_1.prototype.getSendDate = function (rawDocument) {
        return ((rawDocument.send_date &&
            moment(rawDocument.send_date).format('YYYY-MM-DD')) ||
            '');
    };
    class_1.prototype.getDocumentPages = function (rawDocument) {
        return ((rawDocument.pages &&
            rawDocument.pages.map(function (page) {
                return {
                    page_id: page.page_id,
                    thumb_url: page.thumb_url,
                    page_time: page.page_time,
                    order_num: page.order_num,
                    page_num: page.page_num,
                };
            })) ||
            []);
    };
    class_1.prototype.getTotalPageViewTime = function (rawDocument) {
        return ((rawDocument.pages &&
            rawDocument.pages.reduce(function (acc, page) { return acc + page.page_time; }, 0)) ||
            0);
    };
    class_1.prototype.removeDocumentHandler = function () {
        return __awaiter(this, void 0, void 0, function () {
            var result;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.isLoading = true;
                        return [4 /*yield*/, removeDocument(this.platform, this.session, this.documentId)];
                    case 1:
                        result = _a.sent();
                        this.isLoading = false;
                        if (result) {
                            this.changeView.emit(EnumViews.home);
                        }
                        return [2 /*return*/];
                }
            });
        });
    };
    class_1.prototype.openDocumentIntGetAcceptHandler = function () {
        var page = this.documentData.status === EnumDocumentStatuses.draft
            ? 'edit'
            : 'view';
        window.open("https://app.getaccept.com/document/" + page + "/" + this.documentData.id, '_blank');
    };
    return class_1;
}());
LayoutDocumentDetails.style = layoutDocumentDetailsCss;
var layoutHelpCss = ".help-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}.help-container .help-support{width:100%}.help-container .help-support .help-support-link{text-decoration:none;color:#212121}.help-container .help-support .support-links-list{list-style-type:none;padding:0;margin-top:1rem}.help-container .help-support .support-links-list li{display:-ms-flexbox;display:flex;margin-top:0.5rem}.help-container .help-support .support-links-list li a{text-decoration:none;color:#212121;margin-left:0.5rem}";
var LayoutHelp = /** @class */ (function () {
    function LayoutHelp(hostRef) {
        registerInstance(this, hostRef);
    }
    LayoutHelp.prototype.render = function () {
        return [
            h("div", null, h("h3", null, "Help"), h("div", { class: "help-container" }, h("div", { class: "help-support" }, h("a", { class: "help-support-link", href: "https://www.getaccept.com/support" }, "Have any questions or just looking for someone to talk to. Our support are always there for you"), h("ul", { class: "support-links-list" }, h("li", null, h("limel-icon", { class: "support", name: "phone", size: "small" }), h("a", { href: "tel:+46406688158" }, "+46 40-668-81-58")), h("li", null, h("limel-icon", { class: "support", name: "email", size: "small" }), h("a", { href: "mailto:support@getaccept.com" }, "support@getaccept.com")))))),
        ];
    };
    return LayoutHelp;
}());
LayoutHelp.style = layoutHelpCss;
var layoutLoginCss = ".auth-container{display:-ms-flexbox;display:flex;height:100%;width:100%}.auth-container .login-container{width:25%;padding:1rem;border-right:1px solid #ccc}.auth-container .login-container.active{width:60%}.auth-container .signup-container{width:40%;padding:1rem}.auth-container .signup-container.active{width:75%}";
var LayoutLogin = /** @class */ (function () {
    function LayoutLogin(hostRef) {
        registerInstance(this, hostRef);
        this.isSignup = false;
        this.toggleSignupContainer = this.toggleSignupContainer.bind(this);
    }
    LayoutLogin.prototype.render = function () {
        var _this = this;
        var loginClass = this.isSignup
            ? 'login-container'
            : 'login-container active';
        var signupClass = this.isSignup
            ? 'signup-container active'
            : 'signup-container';
        return [
            h("div", { class: "auth-container" }, h("div", { class: loginClass, onClick: function () { return _this.toggleSignupContainer(false); } }, h("h3", null, "Welcome Back"), h("ga-login", { platform: this.platform })), h("div", { class: signupClass, onClick: function () { return _this.toggleSignupContainer(true); } }, h("h3", null, "Create Account"), (function () {
                if (_this.isSignup) {
                    return h("ga-signup", { platform: _this.platform });
                }
                else {
                    return (h("limel-input-field", { label: "Email address", type: "email", value: "", trailingIcon: "filled_message" }));
                }
            })())),
        ];
    };
    LayoutLogin.prototype.toggleSignupContainer = function (value) {
        this.isSignup = value;
    };
    return LayoutLogin;
}());
LayoutLogin.style = layoutLoginCss;
var layoutMenuCss = ".ga-menu{position:absolute;top:1rem;right:1rem}limel-button{--lime-primary-color:#f49132}";
var LayoutMenu = /** @class */ (function () {
    function LayoutMenu(hostRef) {
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
    LayoutMenu.prototype.render = function () {
        if (this.isSending) {
            return [];
        }
        if (this.showBackButton()) {
            return (h("limel-button", { class: "ga-menu", onClick: this.handleBack, label: "Back" }));
        }
        return (h("limel-menu", { class: "ga-menu", label: "Menu", items: this.menuItems, onCancel: this.onCancelMenu, onSelect: this.onNavigate, open: this.isOpen }, h("div", { slot: "trigger" }, h("limel-icon-button", { icon: "menu", onClick: this.toggleMenu }))));
    };
    LayoutMenu.prototype.toggleMenu = function () {
        this.isOpen = !this.isOpen;
    };
    LayoutMenu.prototype.handleBack = function () {
        this.changeView.emit(this.previousViewOnClose());
    };
    LayoutMenu.prototype.onNavigate = function (event) {
        this.changeView.emit(event.detail.value);
        this.isOpen = false;
    };
    LayoutMenu.prototype.onCancelMenu = function () {
        this.isOpen = false;
    };
    LayoutMenu.prototype.previousViewOnClose = function () {
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
    };
    LayoutMenu.prototype.showBackButton = function () {
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
    };
    return LayoutMenu;
}());
LayoutMenu.style = layoutMenuCss;
var layoutOverviewCss = ".main-layout{display:-ms-flexbox;display:flex;-ms-flex-direction:row;flex-direction:row;-ms-flex-wrap:wrap;flex-wrap:wrap;-ms-flex-pack:distribute;justify-content:space-around}@media (min-width: 1074px){.main-layout .send-new-document-container{width:65%}.main-layout .send-new-document-container .send-new-document-buttons{display:-ms-flexbox;display:flex;overflow:hidden;width:100%;-ms-flex-pack:distribute;justify-content:space-around;-ms-flex-wrap:wrap;flex-wrap:wrap}.main-layout .related-documents{margin-right:1rem;width:33%}}@media (max-width: 1075px){.main-layout .send-new-document-container{width:100%}.main-layout .related-documents{width:100%}}";
var LayoutOverview = /** @class */ (function () {
    function LayoutOverview(hostRef) {
        registerInstance(this, hostRef);
        this.documents = [];
    }
    LayoutOverview.prototype.render = function () {
        return [
            h("div", { class: "main-layout" }, h("div", { class: "send-new-document-container" }, h("h3", null, "Send new document"), h("div", { class: "send-new-document-buttons" }, h("send-new-document-button", { isSigning: true }), h("send-new-document-button", { isSigning: false }))), h("div", { class: "related-documents" }, h("h3", null, "Related documents"), this.isLoadingDocuments ? (h("ga-loader", null)) : (h("document-list", { documents: this.documents })))),
        ];
    };
    return LayoutOverview;
}());
LayoutOverview.style = layoutOverviewCss;
var layoutSelectFileCss = ".layout-select-file-container{max-height:60vh;overflow:auto}.layout-select-file-container .select-file-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}@media (min-width: 1074px){.layout-select-file-container .select-file-container .file-column{width:45%;padding:1rem}}@media (max-width: 1075px){.layout-select-file-container .select-file-container .file-column{width:100%}}";
var EnumSections;
(function (EnumSections) {
    EnumSections["None"] = "none";
    EnumSections["Template"] = "template";
    EnumSections["LimeDocuments"] = "limeDocuments";
})(EnumSections || (EnumSections = {}));
var LayoutSelectFile = /** @class */ (function () {
    function class_2(hostRef) {
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
    class_2.prototype.render = function () {
        var _this = this;
        return [
            h("div", { class: "layout-select-file-container" }, h("h3", null, "Select file to send"), ",", h("div", { class: "select-file-container" }, h("div", { class: "file-column" }, h("limel-collapsible-section", { header: "Templates", isOpen: this.openSection === EnumSections.Template, onOpen: function (event) { return _this.onChangeSection(event, EnumSections.Template); }, onClose: function (event) { return _this.onChangeSection(event, EnumSections.None); } }, h("template-list", { templates: this.templates, selectedTemplate: this.selectedTemplate, isLoading: this.isLoadingTemplates })), h("limel-collapsible-section", { header: "Lime documents", isOpen: this.openSection === EnumSections.LimeDocuments, onOpen: function (event) { return _this.onChangeSection(event, EnumSections.LimeDocuments); }, onClose: function (event) { return _this.onChangeSection(event, EnumSections.None); } }, h("lime-document-list", { documents: this.limeDocuments, isLoading: this.isLoadingLimeDocuments }))), h("div", { class: "file-column" }, h("template-preview", { template: this.selectedTemplate, isLoading: this.isLoadingFields, session: this.session }), h("custom-fields", { template: this.selectedTemplate, customFields: this.customFields, isLoading: this.isLoadingFields }))), ","),
        ];
    };
    class_2.prototype.componentWillLoad = function () {
        this.loadTemplates();
        this.loadLimeDocuments();
    };
    class_2.prototype.onChangeSection = function (event, section) {
        event.stopPropagation();
        this.openSection = section;
    };
    class_2.prototype.loadTemplates = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, e_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.isLoadingTemplates = true;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        _a = this;
                        return [4 /*yield*/, fetchTemplates(this.platform, this.session, this.selectedTemplate)];
                    case 2:
                        _a.templates = _b.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        e_1 = _b.sent();
                        this.errorHandler.emit('Could not load templates from GetAccept...');
                        return [3 /*break*/, 4];
                    case 4:
                        this.isLoadingTemplates = false;
                        return [2 /*return*/];
                }
            });
        });
    };
    class_2.prototype.loadLimeDocuments = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, record_id, limetype, _b, e_2;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        this.isLoadingLimeDocuments = true;
                        _a = this.context, record_id = _a.id, limetype = _a.limetype;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        _b = this;
                        return [4 /*yield*/, fetchLimeDocuments(this.platform, limetype, record_id, this.selectedLimeDocument)];
                    case 2:
                        _b.limeDocuments = _c.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        e_2 = _c.sent();
                        this.errorHandler.emit('Could not load related Lime documents...');
                        return [3 /*break*/, 4];
                    case 4:
                        this.isLoadingLimeDocuments = false;
                        return [2 /*return*/];
                }
            });
        });
    };
    class_2.prototype.loadTemplateFields = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, record_id, limetype, fields, e_3;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (!this.selectedTemplate) {
                            this.customFields = [];
                            this.setCustomFields.emit(this.customFields);
                            return [2 /*return*/];
                        }
                        this.isLoadingFields = true;
                        _a = this.context, record_id = _a.id, limetype = _a.limetype;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchTemplateFields(this.platform, this.session, limetype, record_id, this.selectedTemplate)];
                    case 2:
                        fields = _b.sent();
                        this.setFields(fields);
                        return [3 /*break*/, 4];
                    case 3:
                        e_3 = _b.sent();
                        this.errorHandler.emit('Could not fetch template fields from GetAccept...');
                        return [3 /*break*/, 4];
                    case 4:
                        this.isLoadingFields = false;
                        return [2 /*return*/];
                }
            });
        });
    };
    class_2.prototype.setFields = function (fields) {
        var customFields = fields.map(this.mapField);
        this.setCustomFields.emit(customFields);
    };
    class_2.prototype.onChangeTemplate = function (data) {
        this.setTemplates(data);
        if (data) {
            this.loadTemplateFields();
        }
    };
    class_2.prototype.setTemplates = function (template) {
        this.templates = this.getSelectedListItems(this.templates, template);
    };
    class_2.prototype.onChangeDocument = function (data) {
        this.setLimeDocuments(data);
    };
    class_2.prototype.mapField = function (field) {
        return {
            value: field.field_value,
            id: field.field_id,
            label: field.field_label || field.field_value,
            is_editable: !!field.is_editable,
        };
    };
    class_2.prototype.setLimeDocuments = function (document) {
        this.limeDocuments = this.getSelectedListItems(this.limeDocuments, document);
    };
    class_2.prototype.getSelectedListItems = function (items, selectedItem) {
        return items.map(function (item) {
            if (selectedItem && item.value === selectedItem.value) {
                return selectedItem;
            }
            return Object.assign(Object.assign({}, item), { selected: false });
        });
    };
    class_2.prototype.updateFieldValue = function (event) {
        var _a = event.detail, id = _a.id, value = _a.value;
        var customFields = this.customFields.map(function (field) {
            return field.id === id ? Object.assign(Object.assign({}, field), { value: value }) : field;
        });
        this.setCustomFields.emit(customFields);
    };
    Object.defineProperty(class_2, "watchers", {
        get: function () {
            return {
                "selectedTemplate": ["onChangeTemplate"],
                "selectedLimeDocument": ["onChangeDocument"]
            };
        },
        enumerable: false,
        configurable: true
    });
    return class_2;
}());
LayoutSelectFile.style = layoutSelectFileCss;
var layoutSelectRecipientCss = ".select-recipient-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap;max-height:60vh;overflow:auto}@media (min-width: 1074px){.select-recipient-container .recipient-container{width:45%;padding:1rem}.select-recipient-container .selected-recipient-container{width:45%;padding:1rem}}@media (max-width: 1075px){.select-recipient-container .recipient-container{width:100%}.select-recipient-container .selected-recipient-container{width:100%}}.recipient-list{list-style-type:none;padding:0;margin:0;max-height:50vh;overflow:auto}.recipient-toolbar{display:-ms-flexbox;display:flex;-ms-flex-pack:justify;justify-content:space-between;-ms-flex-align:center;align-items:center}.recipient-toolbar :first-child{-ms-flex-positive:1;flex-grow:1;margin-right:1.5rem}limel-switch{--lime-primary-color:#f49132}";
var LayoutSelectRecipient = /** @class */ (function () {
    function class_3(hostRef) {
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
    class_3.prototype.componentWillLoad = function () {
        this.selectedRecipientList = this.document.recipients;
    };
    class_3.prototype.render = function () {
        var _this = this;
        return [
            h("div", { class: "select-recipient-container" }, h("div", { class: "recipient-container" }, h("h3", null, "Search Recipient"), h("div", { class: "recipient-toolbar" }, h("limel-input-field", { label: "Search recipient", value: this.searchTerm, onChange: this.onSearch }), h("limel-switch", { label: "Include coworkers", value: this.includeCoworkers, onChange: this.toggleIncludeCoworkers })), h("ul", { class: "recipient-list" }, this.recipientList.map(function (recipient) {
                if (!_this.isAdded(recipient.lime_id)) {
                    return (h("recipient-item", { recipient: recipient, showAdd: true, onClick: function () {
                            _this.selectRecipientHandler(recipient);
                        } }));
                }
            }))), h("div", { class: "selected-recipient-container" }, h("h3", null, "Added recipients"), h("selected-recipient-list", { recipients: this.selectedRecipientList, document: this.document }))),
        ];
    };
    class_3.prototype.selectRecipientHandler = function (recipient) {
        if (!!recipient.mobile || !!recipient.email) {
            this.selectedRecipientList = __spreadArrays(this.selectedRecipientList, [
                recipient,
            ]);
            this.updateDocumentRecipient.emit(this
                .selectedRecipientList);
        }
        else {
            this.errorHandler.emit('A recipient needs to have a mobile number or an email address');
        }
    };
    class_3.prototype.removeRecipientHandler = function (recipient) {
        var rec = recipient.detail;
        this.selectedRecipientList = this.selectedRecipientList.filter(function (recipientData) {
            return recipientData.lime_id != rec.lime_id;
        });
        this.updateDocumentRecipient.emit(this
            .selectedRecipientList);
    };
    class_3.prototype.changeRecipientRoleHandler = function (recipient) {
        var recipientData = recipient.detail;
        var index = this.selectedRecipientList.findIndex(function (rec) { return rec.lime_id === recipientData.lime_id; });
        this.selectedRecipientList[index] = recipientData;
        this.updateDocumentRecipient.emit(this
            .selectedRecipientList);
    };
    class_3.prototype.isAdded = function (recipientId) {
        return !!this.selectedRecipientList.find(function (recipient) { return recipient.lime_id === recipientId; });
    };
    class_3.prototype.toggleIncludeCoworkers = function () {
        this.includeCoworkers = !this.includeCoworkers;
        this.fetchRecipients();
    };
    class_3.prototype.onSearch = function (event) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                this.searchTerm = event.detail;
                this.fetchRecipients();
                return [2 /*return*/];
            });
        });
    };
    class_3.prototype.fetchRecipients = function () {
        return __awaiter(this, void 0, void 0, function () {
            var options, persons, coworkers, e_4;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        options = {
                            params: {
                                search: this.searchTerm,
                                limit: '10',
                                offset: '0',
                            },
                        };
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 4, , 5]);
                        return [4 /*yield*/, this.fetchPersons(options)];
                    case 2:
                        persons = _a.sent();
                        return [4 /*yield*/, this.fetchCoworkers(options, this.includeCoworkers)];
                    case 3:
                        coworkers = _a.sent();
                        this.recipientList = __spreadArrays(persons, coworkers);
                        return [3 /*break*/, 5];
                    case 4:
                        e_4 = _a.sent();
                        this.errorHandler.emit('Something went wrong while communicating with the server...');
                        return [3 /*break*/, 5];
                    case 5: return [2 /*return*/];
                }
            });
        });
    };
    class_3.prototype.fetchPersons = function (options) {
        return __awaiter(this, void 0, void 0, function () {
            var persons;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.platform
                            .get(PlatformServiceName.Http)
                            .get('getaccept/persons', options)];
                    case 1:
                        persons = _a.sent();
                        return [2 /*return*/, persons.map(function (person) { return ({
                                email: person.email,
                                name: person.name,
                                mobile: person.mobilephone || person.phone,
                                limetype: 'person',
                                lime_id: person.id,
                                company: person.company,
                            }); })];
                }
            });
        });
    };
    class_3.prototype.fetchCoworkers = function (options, includeCoworkers) {
        return __awaiter(this, void 0, void 0, function () {
            var coworkers;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!includeCoworkers) {
                            return [2 /*return*/, []];
                        }
                        return [4 /*yield*/, this.platform
                                .get(PlatformServiceName.Http)
                                .get('getaccept/coworkers', options)];
                    case 1:
                        coworkers = _a.sent();
                        return [2 /*return*/, coworkers.map(function (coworker) { return ({
                                mobile: coworker.mobilephone || coworker.phone,
                                name: coworker.name,
                                email: coworker.email,
                                limetype: 'coworker',
                                lime_id: coworker.id,
                                company: coworker.company,
                            }); })];
                }
            });
        });
    };
    return class_3;
}());
LayoutSelectRecipient.style = layoutSelectRecipientCss;
var layoutSendDocumentCss = ".send-document-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}@media (min-width: 1074px){.send-document-container .send-document-prepare-container{width:calc(50% - 0.5rem);padding-right:0.5rem}.send-document-container .send-document-email-container{width:calc(50% - 0.5rem);padding-left:0.5rem}}@media (max-width: 1075px){.send-document-container .send-document-prepare-container{width:100%}.send-document-container .send-document-email-container{margin-top:1.5rem;width:100%}}.send-document-container .add-video-button{margin-bottom:0.5rem}.send-document-container .video-is-added{display:-ms-inline-flexbox;display:inline-flex;-ms-flex-align:center;align-items:center;margin-left:0.5rem;border-radius:1rem;cursor:pointer;background-color:#f5f5f5}.send-document-container .video-is-added .video-is-added-icon{padding:0.1rem;margin-right:0.5rem;background-color:#2dc990;color:#fff}.send-document-container .video-is-added .video-remove-icon{margin-left:0.5rem;padding:0.1rem;color:#ccc}.send-document-container .video-is-added:hover{background-color:#ccc}.send-document-container .video-is-added:hover .video-remove-icon{color:#212121}.send-document-container .video-remove-container{display:-ms-flexbox;display:flex;cursor:pointer}limel-button{--lime-primary-color:#f49132}limel-checkbox{--lime-primary-color:#f49132}limel-flex-container limel-input-field:first-child{-ms-flex:2;flex:2;margin-right:0.5rem}limel-flex-container limel-input-field:last-child{-ms-flex:1;flex:1;margin-left:0.5rem}";
var LayoutSendDocument = /** @class */ (function () {
    function LayoutSendDocument(hostRef) {
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
    LayoutSendDocument.prototype.componentWillLoad = function () {
        this.documentName = this.fileName();
        this.setNewDocumentName.emit(this.documentName);
        this.value = this.document.value || 0;
        this.smartReminder = this.document.is_reminder_sending;
        this.sendLinkBySms = this.document.is_sms_sending;
        this.documentVideo = this.document.video_id !== '';
    };
    LayoutSendDocument.prototype.componentDidUpdate = function () {
        this.value = this.document.value;
        this.documentName = this.document.name || this.fileName();
    };
    LayoutSendDocument.prototype.render = function () {
        return [
            h("div", { class: "send-document-container" }, h("div", { class: "send-document-prepare-container" }, h("h3", null, "Prepare sending"), h("limel-flex-container", { align: "stretch" }, h("limel-input-field", { label: "Document Name", value: this.documentName, onChange: this.handleChangeDocumentName }), h("limel-input-field", { label: "Value", value: this.value.toString(), onChange: this.handleChangeValue })), h("div", null, h("h4", null, "Document engagement"), this.documentVideo ? (h("div", null, h("div", { class: "video-is-added" }, h("limel-icon", { name: "tv_show", size: "large", class: "video-is-added-icon" }), h("span", null, "Video is added"), h("limel-icon", { class: "video-remove-icon", name: "multiply", size: "small", onClick: this.handleRemoveVideo })))) : (h("limel-button", { class: "add-video-button", primary: true, label: "Add Video introduction", onClick: this.handleAddVideo })), h("limel-checkbox", { label: "Send smart reminders", id: "SmartReminder", checked: this.smartReminder, onChange: this.handleChangeSmartReminder }), h("limel-checkbox", { label: "Send link by SMS", id: "SendLinkBySMS", checked: this.sendLinkBySms, onChange: this.handleChangeSendLinkBySms }))), h("div", { class: "send-document-email-container" }, h("create-email", { document: this.document }))),
        ];
    };
    LayoutSendDocument.prototype.fileName = function () {
        if (this.limeDocument) {
            return this.limeDocument.text;
        }
        else if (this.template) {
            return this.template.text;
        }
        else {
            return '';
        }
    };
    LayoutSendDocument.prototype.handleChangeDocumentName = function (event) {
        this.setNewDocumentName.emit(event.detail);
    };
    LayoutSendDocument.prototype.handleChangeValue = function (event) {
        this.setDocumentValue.emit(event.detail);
    };
    LayoutSendDocument.prototype.handleChangeSmartReminder = function (event) {
        this.setSmartReminder.emit(event.detail);
    };
    LayoutSendDocument.prototype.handleChangeSendLinkBySms = function (event) {
        this.setIsSmsSending.emit(event.detail);
    };
    LayoutSendDocument.prototype.handleAddVideo = function () {
        //should open select video view
        this.changeView.emit(EnumViews.videoLibrary);
    };
    LayoutSendDocument.prototype.handleRemoveVideo = function () {
        this.removeVideo.emit();
        this.documentVideo = false;
    };
    return LayoutSendDocument;
}());
LayoutSendDocument.style = layoutSendDocumentCss;
var layoutSettingsCss = ".settings-container{display:-ms-flexbox;display:flex;-ms-flex-wrap:wrap;flex-wrap:wrap}.settings-container .error{display:block;color:#f88987;margin-top:1rem}@media (min-width: 1074px){.settings-container .settings-column{width:45%;padding:1rem}}@media (max-width: 1075px){.settings-container .settings-column{width:100%}}.full-width{width:100%}";
var LayoutSettings = /** @class */ (function () {
    function class_4(hostRef) {
        registerInstance(this, hostRef);
        this.setSession = createEvent(this, "setSession", 7);
        this.error = '';
        this.onChangeEntity = this.onChangeEntity.bind(this);
        this.renderContent = this.renderContent.bind(this);
    }
    class_4.prototype.componentWillLoad = function () {
        var _this = this;
        this.entityOptions = this.entities.map(function (entity) { return ({
            value: entity.id,
            text: entity.name,
        }); });
        this.selectedEntity = this.entityOptions.find(function (entity) {
            return entity.value === _this.user.entity_id;
        });
    };
    class_4.prototype.render = function () {
        return [
            h("h3", null, "Settings"),
            h("div", { class: "settings-container" }, this.isLoading ? this.renderLoader() : this.renderContent()),
        ];
    };
    class_4.prototype.renderLoader = function () {
        return h("ga-loader", { class: "full-width" });
    };
    class_4.prototype.renderContent = function () {
        return [
            h("div", { class: "settings-column" }, h("h4", null, "My profile"), h("limel-flex-container", { justify: "center" }, h("profile-picture", { thumbUrl: this.user.thumb_url })), h("limel-input-field", { label: "Name", value: this.user.first_name + " " + this.user.last_name, disabled: true }), h("limel-input-field", { label: "Title", value: this.user.title, disabled: true }), h("limel-input-field", { label: "Email", value: this.user.email, disabled: true }), h("limel-input-field", { label: "Phone", value: this.user.mobile, disabled: true }), h("limel-input-field", { label: "Role", value: this.user.role, disabled: true })),
            h("div", { class: "settings-column" }, h("h4", null, "Change entity"), h("limel-select", { class: "entity-selector", label: "Entity", value: this.selectedEntity, options: this.entityOptions, onChange: this.onChangeEntity, required: true }), this.renderError(this.error)),
        ];
    };
    class_4.prototype.renderError = function (error) {
        return error ? h("span", { class: "error" }, error) : '';
    };
    class_4.prototype.onChangeEntity = function (event) {
        return __awaiter(this, void 0, void 0, function () {
            var originalEntity, session, e_5;
            var _this = this;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (event.detail.value == this.selectedEntity.value) {
                            return [2 /*return*/];
                        }
                        this.isLoading = true;
                        originalEntity = this.selectedEntity;
                        this.selectedEntity = event.detail;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, switchEntity(this.selectedEntity.value, this.platform, this.session)];
                    case 2:
                        session = _a.sent();
                        this.setSession.emit(session);
                        return [3 /*break*/, 4];
                    case 3:
                        e_5 = _a.sent();
                        this.error =
                            'Could not switch entity. Please try again at a later time.';
                        setTimeout(function () {
                            _this.error = '';
                        }, 3000);
                        this.selectedEntity = originalEntity;
                        return [3 /*break*/, 4];
                    case 4:
                        this.isLoading = false;
                        return [2 /*return*/];
                }
            });
        });
    };
    return class_4;
}());
LayoutSettings.style = layoutSettingsCss;
var layoutValidateDocumentCss = ".document-error-list{padding:0;margin:0}.share-document-recipient-list{list-style-type:none;padding:0;margin:0}.validate-document-button-container{display:-ms-flexbox;display:flex;margin:2rem 0}.validate-document-button-container .send-button{padding-right:1rem}.action-buttons{margin-top:2rem}.action-buttons limel-button{margin-right:1rem}limel-button{--lime-primary-color:#f49132}";
var LayoutValidateDocument = /** @class */ (function () {
    function class_5(hostRef) {
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
    class_5.prototype.componentWillLoad = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.validateDocument()];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        });
    };
    class_5.prototype.render = function () {
        var _this = this;
        return (h("div", null, (function () {
            if (_this.isLoading) {
                return (h("ga-loader-with-text", { showText: _this.isSending, text: "We are creating your document!" }));
            }
            else if (_this.isSealed) {
                if (_this.recipients.length > 0) {
                    return (h("div", { class: "share-document-container" }, h("h3", null, "Share document link:"), h("ul", { class: "share-document-recipient-list" }, _this.recipients.map(function (recipient) {
                        return (h("share-document-link", { recipient: recipient }));
                    })), h("div", { class: "action-buttons" }, h("limel-button", { label: "Done", primary: true, onClick: function () {
                            _this.documentCompleted.emit(false);
                        } }), h("limel-button", { label: "Open in GetAccept", primary: false, onClick: function () { return _this.handleCreateDocument(false, true); } }))));
                }
            }
            else {
                return (h("div", null, (function () {
                    if (_this.errorList.length > 0) {
                        return (h("document-error-feedback", { document: _this.document, errorList: _this.errorList }));
                    }
                    else {
                        return (h("document-validate-info", { document: _this.document }));
                    }
                })(), h("div", { class: "validate-document-button-container" }, (function () {
                    if (_this.errorList.length === 0) {
                        return [
                            h("limel-button", { class: "send-button", label: "Send", primary: true, onClick: function () { return _this.handleCreateDocument(true, false); } }),
                            h("limel-button", { label: "Share document link", primary: false, onClick: function () { return _this.handleCreateDocument(false, false); } }),
                            h("limel-button", { label: "Open in GetAccept", primary: false, onClick: function () { return _this.handleCreateDocument(false, true); } }),
                        ];
                    }
                    else {
                        return (h("limel-button", { label: "Open in GetAccept", primary: false, onClick: function () { return _this.handleCreateDocument(false, true); } }));
                    }
                })())));
            }
        })()));
    };
    class_5.prototype.hasTemplateRoles = function () {
        return __awaiter(this, void 0, void 0, function () {
            var data, roles, e_6;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!this.template) {
                            return [2 /*return*/, false];
                        }
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchDocumentDetails(this.platform, this.session, this.template.value)];
                    case 2:
                        data = _a.sent();
                        roles = data.recipients.filter(function (recipient) { return recipient.status === '1'; });
                        return [2 /*return*/, roles.length > 0];
                    case 3:
                        e_6 = _a.sent();
                        this.errorHandler.emit('Could not fetch template data from GetAccept');
                        return [2 /*return*/, false];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    class_5.prototype.handleUploadDocument = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, data, success;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (!this.limeDocument) return [3 /*break*/, 2];
                        return [4 /*yield*/, uploadDocument(this.platform, this.session, this.limeDocument.value)];
                    case 1:
                        _a = _b.sent(), data = _a.data, success = _a.success;
                        if (success) {
                            return [2 /*return*/, data.file_id];
                        }
                        else {
                            this.errorHandler.emit('Could not upload Lime document to GetAccept');
                        }
                        _b.label = 2;
                    case 2: return [2 /*return*/, ''];
                }
            });
        });
    };
    class_5.prototype.handleCreateDocument = function (send, openDocument) {
        return __awaiter(this, void 0, void 0, function () {
            var file_ids, documentData, _a, data, success, openUrl;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.toggleLoading(true);
                        return [4 /*yield*/, this.handleUploadDocument()];
                    case 1:
                        file_ids = _b.sent();
                        documentData = Object.assign(Object.assign({}, this.document), { template_id: this.template ? this.template.value : '', custom_fields: this.template ? this.fields : [], file_ids: file_ids, is_automatic_sending: send });
                        return [4 /*yield*/, createDocument(this.platform, this.session, documentData)];
                    case 2:
                        _a = _b.sent(), data = _a.data, success = _a.success;
                        if (!success) {
                            this.errorHandler.emit('Could not create document. Make sure that all data is correctly supplied');
                            this.toggleLoading(false);
                            return [2 /*return*/];
                        }
                        if (openDocument) {
                            openUrl = "https://app.getaccept.com/document/edit/" + data.id;
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
                        return [2 /*return*/];
                }
            });
        });
    };
    class_5.prototype.sealDocument = function (documentId, attempt) {
        if (attempt === void 0) { attempt = 1; }
        return __awaiter(this, void 0, void 0, function () {
            var maxAttempts, timeout, _a, data, success;
            var _this = this;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        maxAttempts = 5;
                        timeout = 5000;
                        return [4 /*yield*/, sealDocument(this.platform, this.session, documentId)];
                    case 1:
                        _a = _b.sent(), data = _a.data, success = _a.success;
                        if (!success && attempt < maxAttempts) {
                            return [2 /*return*/, setTimeout(function () { return _this.sealDocument(documentId, (attempt += 1)); }, timeout)];
                        }
                        else if (!success && attempt >= maxAttempts) {
                            this.errorHandler.emit('Could not seal document do to lengthy import. Try to open it in GetAccept and seal it from there.');
                            this.toggleLoading(false);
                            return [2 /*return*/];
                        }
                        this.toggleLoading(false);
                        this.recipients = data.recipients.map(function (recipient) {
                            return {
                                name: recipient.fullname,
                                document_url: recipient.document_url,
                                role: recipient.role,
                                email: recipient.email,
                            };
                        });
                        this.documentCompleted.emit(true);
                        return [2 /*return*/];
                }
            });
        });
    };
    class_5.prototype.handleOpenGetAccept = function () {
        if (this.sentDocument) {
            var openUrl = "https://app.getaccept.com/document/view/" + this.sentDocument.id;
            this.openInNewTab(openUrl);
        }
    };
    class_5.prototype.validateDocument = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
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
                        return [4 /*yield*/, this.hasTemplateRoles()];
                    case 1:
                        if (_a.sent()) {
                            this.errorList.push({
                                header: 'Template has unassigned roles',
                                title: 'The process must be completed in GetAccept before sending.',
                                icon: 'id_not_verified',
                                view: EnumViews.selectFile,
                            });
                        }
                        this.isLoading = false;
                        return [2 /*return*/];
                }
            });
        });
    };
    class_5.prototype.haveSigner = function () {
        var signers = this.document.recipients.filter(function (recipient) { return recipient.role === 'signer'; });
        return signers.length > 0;
    };
    class_5.prototype.recipientsWithOnlyPhoneExists = function () {
        return this.document.recipients.some(function (recipient) { return !recipient.email && recipient.mobile !== ''; });
    };
    class_5.prototype.recipientMissingEmailAndPhoneExists = function () {
        return this.document.recipients.some(function (recipient) { return !recipient.email && !recipient.mobile; });
    };
    class_5.prototype.hasProperty = function (value) {
        return value ? 'Yes' : 'No';
    };
    class_5.prototype.openInNewTab = function (url) {
        this.toggleLoading(false);
        this.documentCompleted.emit();
        var win = window.open(url, '_blank');
        win.focus();
    };
    class_5.prototype.toggleLoading = function (value) {
        this.isLoading = value;
        this.isSendingDocument.emit(value);
    };
    return class_5;
}());
LayoutValidateDocument.style = layoutValidateDocumentCss;
var layoutVideoLibraryCss = ".video-list{display:-ms-flexbox;display:flex;-ms-flex-flow:row wrap;flex-flow:row wrap;-ms-flex-pack:start;justify-content:flex-start;-ms-flex-item-align:start;align-self:flex-start;list-style-type:none;padding:0;margin:0;width:100%}";
var LayoutVideoLibrary = /** @class */ (function () {
    function class_6(hostRef) {
        registerInstance(this, hostRef);
        this.changeView = createEvent(this, "changeView", 7);
        this.videos = [];
        this.isLoadingVideos = false;
        this.handelClose = this.handelClose.bind(this);
    }
    class_6.prototype.componentWillLoad = function () {
        this.loadVideos();
    };
    class_6.prototype.render = function () {
        return [
            h("div", { class: "video-library-container" }, h("h3", null, "Select a video"), h("p", null, "It will be present for the recipient when they open the document."), this.isLoadingVideos && h("ga-loader", null), h("ul", { class: "video-list" }, this.videos.map(function (video) {
                return h("video-thumb", { video: video });
            }))),
        ];
    };
    class_6.prototype.loadVideos = function () {
        return __awaiter(this, void 0, void 0, function () {
            var videos;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.isLoadingVideos = true;
                        return [4 /*yield*/, fetchVideos(this.platform, this.session)];
                    case 1:
                        videos = (_a.sent()).videos;
                        this.videos = videos.map(function (video) {
                            return {
                                thumb_url: video.thumb_url,
                                video_id: video.video_id,
                                video_title: video.video_title,
                                video_type: video.video_type,
                                video_url: video.video_url,
                            };
                        });
                        this.isLoadingVideos = false;
                        return [2 /*return*/];
                }
            });
        });
    };
    class_6.prototype.handelClose = function () {
        this.changeView.emit(EnumViews.sendDocument);
    };
    return class_6;
}());
LayoutVideoLibrary.style = layoutVideoLibraryCss;
var workflowProgressBarCss = ".progress-steps{display:-ms-flexbox;display:flex;-ms-flex-direction:row;flex-direction:row;list-style-type:none;padding:0;margin:0;-ms-flex-pack:center;justify-content:center}.progress-steps limel-icon{color:#f49132}.progress-steps .progress-action-button{margin:0 2.5rem;color:#f49132;font-size:0.7rem;text-transform:uppercase;font-weight:bolder;cursor:pointer}.progress-steps .progress-step{text-align:center;margin:0 1rem;text-align:center;margin:0 1rem;width:5rem;-ms-flex-wrap:wrap;flex-wrap:wrap;display:-ms-flexbox;display:flex;-ms-flex-pack:center;justify-content:center}.progress-steps .progress-step .progress-step-icon{display:-ms-flexbox;display:flex;-ms-flex-pack:center;justify-content:center;text-align:center;border-radius:50%;height:2em;width:2em;overflow:hidden;background-color:#f5f5f5;color:#f49132;cursor:pointer}.progress-steps .progress-step .progress-step-icon.active{background-color:#f49132;color:#fff}.progress-steps .progress-step .progress-step-text{font-size:0.55rem}";
var WorkflowProgressBar = /** @class */ (function () {
    function WorkflowProgressBar(hostRef) {
        registerInstance(this, hostRef);
        this.changeView = createEvent(this, "changeView", 7);
        this.changeViewHandlerPrevious = this.changeViewHandlerPrevious.bind(this);
        this.changeViewHandlerNext = this.changeViewHandlerNext.bind(this);
        this.changeViewSelectedStep = this.changeViewSelectedStep.bind(this);
    }
    WorkflowProgressBar.prototype.render = function () {
        var _this = this;
        return (function () {
            if (_this.isVisible) {
                return (h("ul", { class: "progress-steps" }, h("li", { class: "progress-action-button", onClick: _this.changeViewHandlerPrevious }, "Back"), workflowSteps.map(function (step, index) {
                    var progessStep = 'progress-step-icon';
                    if (step.currentView === _this.activeView) {
                        progessStep += ' active';
                    }
                    return (h("li", { class: "progress-step", onClick: function () { return _this.changeViewSelectedStep(step.currentView); } }, h("span", { class: progessStep }, index + 1), h("span", { class: "progress-step-text" }, step.label)));
                }), h("li", { class: "progress-action-button", onClick: _this.changeViewHandlerNext }, "Next")));
            }
        })();
    };
    WorkflowProgressBar.prototype.changeViewHandlerPrevious = function () {
        var _this = this;
        var viewData = workflowSteps.find(function (step) {
            return step.currentView === _this.activeView;
        });
        this.changeView.emit(viewData.previousView);
    };
    WorkflowProgressBar.prototype.changeViewHandlerNext = function () {
        var _this = this;
        var viewData = workflowSteps.find(function (step) {
            return step.currentView === _this.activeView;
        });
        this.changeView.emit(viewData.nextView);
    };
    WorkflowProgressBar.prototype.changeViewSelectedStep = function (currentView) {
        this.changeView.emit(currentView);
    };
    return WorkflowProgressBar;
}());
WorkflowProgressBar.style = workflowProgressBarCss;
export { ErrorMessage as error_message, LayoutDocumentDetails as layout_document_details, LayoutHelp as layout_help, LayoutLogin as layout_login, LayoutMenu as layout_menu, LayoutOverview as layout_overview, LayoutSelectFile as layout_select_file, LayoutSelectRecipient as layout_select_recipient, LayoutSendDocument as layout_send_document, LayoutSettings as layout_settings, LayoutValidateDocument as layout_validate_document, LayoutVideoLibrary as layout_video_library, WorkflowProgressBar as workflow_progress_bar };
