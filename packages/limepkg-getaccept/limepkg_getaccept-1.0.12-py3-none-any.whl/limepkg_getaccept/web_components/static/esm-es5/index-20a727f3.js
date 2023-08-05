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
/**
 * Core platform service names
 */
var PlatformServiceName;
(function (PlatformServiceName) {
    PlatformServiceName["Translate"] = "translate";
    PlatformServiceName["Http"] = "http";
    PlatformServiceName["Route"] = "route";
    PlatformServiceName["Notification"] = "notifications";
    PlatformServiceName["Query"] = "query";
    PlatformServiceName["CommandBus"] = "commandBus";
    PlatformServiceName["Dialog"] = "dialog";
    PlatformServiceName["EventDispatcher"] = "eventDispatcher";
    PlatformServiceName["LimetypesState"] = "state.limetypes";
    PlatformServiceName["LimeobjectsState"] = "state.limeobjects";
    PlatformServiceName["ApplicationState"] = "state.application";
    PlatformServiceName["ConfigsState"] = "state.configs";
    PlatformServiceName["FiltersState"] = "state.filters";
    PlatformServiceName["DeviceState"] = "state.device";
    PlatformServiceName["TaskState"] = "state.tasks";
})(PlatformServiceName || (PlatformServiceName = {}));
var Operator;
(function (Operator) {
    Operator["AND"] = "AND";
    Operator["OR"] = "OR";
    Operator["EQUALS"] = "=";
    Operator["NOT"] = "!";
    Operator["GREATER"] = ">";
    Operator["LESS"] = "<";
    Operator["IN"] = "IN";
    Operator["BEGINS"] = "=?";
    Operator["LIKE"] = "?";
    Operator["LESS_OR_EQUAL"] = "<=";
    Operator["GREATER_OR_EQUAL"] = ">=";
})(Operator || (Operator = {}));
/**
 * Events dispatched by the commandbus event middleware
 */
var CommandEvent;
(function (CommandEvent) {
    /**
     * Dispatched when the command has been received by the commandbus.
     * Calling `preventDefault()` on the event will stop the command from being handled
     *
     * @detail { command }
     */
    CommandEvent["Received"] = "command.received";
    /**
     * Dispatched when the command has been handled by the commandbus
     *
     * @detail { command, result }
     */
    CommandEvent["Handled"] = "command.handled";
    /**
     * Dispatched if an error occurs while handling the command
     *
     * @detail { command, error }
     */
    CommandEvent["Failed"] = "command.failed";
})(CommandEvent || (CommandEvent = {}));
var TaskState;
(function (TaskState) {
    /**
     * Task state is unknown
     */
    TaskState["Pending"] = "PENDING";
    /**
     * Task was started by a worker
     */
    TaskState["Started"] = "STARTED";
    /**
     * Task is waiting for retry
     */
    TaskState["Retry"] = "RETRY";
    /**
     * Task succeeded
     */
    TaskState["Success"] = "SUCCESS";
    /**
     * Task failed
     */
    TaskState["Failure"] = "FAILURE";
})(TaskState || (TaskState = {}));
/**
 * Events dispatched by the task service
 */
var TaskEvent;
(function (TaskEvent) {
    /**
     * Dispatched when a task has been created.
     *
     * @detail { task }
     */
    TaskEvent["Created"] = "task.created";
    /**
     * Dispatched when the task has successfully been completed
     *
     * @detail { task }
     */
    TaskEvent["Success"] = "task.success";
    /**
     * Dispatched if an error occured while running the task
     *
     * @detail { task, error? }
     */
    TaskEvent["Failed"] = "task.failed";
})(TaskEvent || (TaskEvent = {}));
var fetchMe = function (platform, session) { return __awaiter(void 0, void 0, void 0, function () {
    var options, data;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                options = {
                    headers: getHeaders(session),
                };
                return [4 /*yield*/, platform
                        .get(PlatformServiceName.Http)
                        .get('getaccept/me', options)];
            case 1:
                data = (_a.sent()).data;
                return [2 /*return*/, data];
        }
    });
}); };
var switchEntity = function (entity_id, platform, session) { return __awaiter(void 0, void 0, void 0, function () {
    var options, payload, data;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                options = {
                    headers: getHeaders(session),
                };
                payload = {
                    entity_id: entity_id,
                };
                return [4 /*yield*/, platform
                        .get(PlatformServiceName.Http)
                        .post('getaccept/switch-entity', payload, options)];
            case 1:
                data = (_a.sent()).data;
                return [2 /*return*/, data];
        }
    });
}); };
var fetchLimeDocuments = function (platform, limetype, record_id, selectedLimeDocument) { return __awaiter(void 0, void 0, void 0, function () {
    var options, documents;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                options = {
                    params: {
                        limetype: limetype,
                        record_id: record_id.toString(),
                    },
                };
                return [4 /*yield*/, platform
                        .get(PlatformServiceName.Http)
                        .get('getaccept/documents', options)];
            case 1:
                documents = _a.sent();
                return [2 /*return*/, documents.map(function (document) { return ({
                        text: document.comment,
                        value: document.id,
                        icon: 'document',
                        iconColor: 'var(--lime-green)',
                        selected: selectedLimeDocument && selectedLimeDocument.value === document.id,
                    }); })];
        }
    });
}); };
var fetchSentDocuments = function (platform, externalId, session) { return __awaiter(void 0, void 0, void 0, function () {
    var options, documents;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                options = {
                    headers: {
                        'ga-auth-token': session.access_token,
                    },
                    params: {
                        external_id: externalId,
                    },
                };
                return [4 /*yield*/, platform
                        .get(PlatformServiceName.Http)
                        .get('getaccept/sent-documents', options)];
            case 1:
                documents = (_a.sent()).documents;
                return [2 /*return*/, documents];
        }
    });
}); };
var fetchTemplates = function (platform, session, selectedTemplate) { return __awaiter(void 0, void 0, void 0, function () {
    var options, _a, templates;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                options = {
                    headers: {
                        'ga-auth-token': session.access_token,
                    },
                };
                return [4 /*yield*/, platform
                        .get(PlatformServiceName.Http)
                        .get('getaccept/templates', options)];
            case 1:
                _a = (_b.sent()).templates, templates = _a === void 0 ? [] : _a;
                return [2 /*return*/, templates.map(function (template) { return ({
                        text: template.name,
                        value: template.id,
                        icon: 'document',
                        iconColor: 'var(--lime-orange)',
                        selected: selectedTemplate && selectedTemplate.value === template.id,
                    }); })];
        }
    });
}); };
var fetchTemplateFields = function (platform, session, limetype, record_id, selectedTemplate) { return __awaiter(void 0, void 0, void 0, function () {
    var options, _a, fields;
    return __generator(this, function (_b) {
        switch (_b.label) {
            case 0:
                options = {
                    headers: {
                        'ga-auth-token': session.access_token,
                    },
                    params: {
                        template_id: selectedTemplate.value,
                        limetype: limetype,
                        record_id: record_id.toString(),
                    },
                };
                return [4 /*yield*/, platform
                        .get(PlatformServiceName.Http)
                        .get('getaccept/template-fields', options)];
            case 1:
                _a = (_b.sent()).data.fields, fields = _a === void 0 ? [] : _a;
                return [2 /*return*/, fields];
        }
    });
}); };
var getHeaders = function (session) {
    return {
        'ga-auth-token': session.access_token,
    };
};
var fetchEntity = function (platform, session) { return __awaiter(void 0, void 0, void 0, function () {
    var options, data;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                options = {
                    headers: getHeaders(session),
                };
                return [4 /*yield*/, platform
                        .get(PlatformServiceName.Http)
                        .get('getaccept/entity', options)];
            case 1:
                data = (_a.sent()).data;
                return [2 /*return*/, data];
        }
    });
}); };
var fetchDocumentDetails = function (platform, session, document_id) { return __awaiter(void 0, void 0, void 0, function () {
    var options, data;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                options = {
                    headers: getHeaders(session),
                    params: {
                        document_id: document_id,
                    },
                };
                return [4 /*yield*/, platform
                        .get(PlatformServiceName.Http)
                        .get('getaccept/document-details', options)];
            case 1:
                data = (_a.sent()).data;
                return [2 /*return*/, data];
        }
    });
}); };
var fetchVideos = function (platform, session) { return __awaiter(void 0, void 0, void 0, function () {
    var options, data;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                options = {
                    headers: getHeaders(session),
                };
                return [4 /*yield*/, platform
                        .get(PlatformServiceName.Http)
                        .get('getaccept/videos', options)];
            case 1:
                data = (_a.sent()).data;
                return [2 /*return*/, data];
        }
    });
}); };
var createDocument = function (platform, session, document) { return __awaiter(void 0, void 0, void 0, function () {
    var options;
    return __generator(this, function (_a) {
        options = {
            headers: getHeaders(session),
        };
        return [2 /*return*/, platform
                .get(PlatformServiceName.Http)
                .post('getaccept/create-document', document, options)];
    });
}); };
var sealDocument = function (platform, session, documentId) { return __awaiter(void 0, void 0, void 0, function () {
    var options, payload;
    return __generator(this, function (_a) {
        options = {
            headers: getHeaders(session),
        };
        payload = {
            document_id: documentId,
        };
        return [2 /*return*/, platform
                .get(PlatformServiceName.Http)
                .post('getaccept/seal-document', payload, options)];
    });
}); };
var uploadDocument = function (platform, session, documentId) { return __awaiter(void 0, void 0, void 0, function () {
    var options, payload;
    return __generator(this, function (_a) {
        options = {
            headers: getHeaders(session),
        };
        payload = {
            document_id: documentId,
        };
        return [2 /*return*/, platform
                .get(PlatformServiceName.Http)
                .post('getaccept/upload-document', payload, options)];
    });
}); };
var removeDocument = function (platform, session, documentId) { return __awaiter(void 0, void 0, void 0, function () {
    var options, payload;
    return __generator(this, function (_a) {
        options = {
            headers: getHeaders(session),
        };
        payload = {
            document_id: documentId,
        };
        return [2 /*return*/, platform
                .get(PlatformServiceName.Http)
                .post('getaccept/delete-document', payload, options)];
    });
}); };
var signup = function (platform, data) { return __awaiter(void 0, void 0, void 0, function () {
    var payload;
    return __generator(this, function (_a) {
        payload = data;
        return [2 /*return*/, platform
                .get(PlatformServiceName.Http)
                .post('getaccept/signup', payload)];
    });
}); };
var refreshToken = function (platform, session) { return __awaiter(void 0, void 0, void 0, function () {
    var access_token, expires_in;
    return __generator(this, function (_a) {
        access_token = session.access_token, expires_in = session.expires_in;
        return [2 /*return*/, platform
                .get(PlatformServiceName.Http)
                .post('getaccept/refresh-token', { access_token: access_token, expires_in: expires_in })];
    });
}); };
export { PlatformServiceName as P, fetchEntity as a, fetchSentDocuments as b, fetchDocumentDetails as c, removeDocument as d, fetchTemplates as e, fetchMe as f, fetchLimeDocuments as g, fetchTemplateFields as h, createDocument as i, sealDocument as j, fetchVideos as k, signup as l, refreshToken as r, switchEntity as s, uploadDocument as u };
