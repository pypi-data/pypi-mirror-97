'use strict';

/**
 * Core platform service names
 */
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
})(exports.PlatformServiceName || (exports.PlatformServiceName = {}));

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

const fetchMe = async (platform, session) => {
    const options = {
        headers: getHeaders(session),
    };
    const { data } = await platform
        .get(exports.PlatformServiceName.Http)
        .get('getaccept/me', options);
    return data;
};
const switchEntity = async (entity_id, platform, session) => {
    const options = {
        headers: getHeaders(session),
    };
    const payload = {
        entity_id,
    };
    const { data } = await platform
        .get(exports.PlatformServiceName.Http)
        .post('getaccept/switch-entity', payload, options);
    return data;
};
const fetchLimeDocuments = async (platform, limetype, record_id, selectedLimeDocument) => {
    const options = {
        params: {
            limetype,
            record_id: record_id.toString(),
        },
    };
    const documents = await platform
        .get(exports.PlatformServiceName.Http)
        .get('getaccept/documents', options);
    return documents.map(document => ({
        text: document.comment,
        value: document.id,
        icon: 'document',
        iconColor: 'var(--lime-green)',
        selected: selectedLimeDocument && selectedLimeDocument.value === document.id,
    }));
};
const fetchSentDocuments = async (platform, externalId, session) => {
    const options = {
        headers: {
            'ga-auth-token': session.access_token,
        },
        params: {
            external_id: externalId,
        },
    };
    const { documents } = await platform
        .get(exports.PlatformServiceName.Http)
        .get('getaccept/sent-documents', options);
    return documents;
};
const fetchTemplates = async (platform, session, selectedTemplate) => {
    const options = {
        headers: {
            'ga-auth-token': session.access_token,
        },
    };
    const { templates = [] } = await platform
        .get(exports.PlatformServiceName.Http)
        .get('getaccept/templates', options);
    return templates.map((template) => ({
        text: template.name,
        value: template.id,
        icon: 'document',
        iconColor: 'var(--lime-orange)',
        selected: selectedTemplate && selectedTemplate.value === template.id,
    }));
};
const fetchTemplateFields = async (platform, session, limetype, record_id, selectedTemplate) => {
    const options = {
        headers: {
            'ga-auth-token': session.access_token,
        },
        params: {
            template_id: selectedTemplate.value,
            limetype: limetype,
            record_id: record_id.toString(),
        },
    };
    const { data: { fields = [] }, } = await platform
        .get(exports.PlatformServiceName.Http)
        .get('getaccept/template-fields', options);
    return fields;
};
const getHeaders = (session) => {
    return {
        'ga-auth-token': session.access_token,
    };
};
const fetchEntity = async (platform, session) => {
    const options = {
        headers: getHeaders(session),
    };
    const { data } = await platform
        .get(exports.PlatformServiceName.Http)
        .get('getaccept/entity', options);
    return data;
};
const fetchDocumentDetails = async (platform, session, document_id) => {
    const options = {
        headers: getHeaders(session),
        params: {
            document_id,
        },
    };
    const { data } = await platform
        .get(exports.PlatformServiceName.Http)
        .get('getaccept/document-details', options);
    return data;
};
const fetchVideos = async (platform, session) => {
    const options = {
        headers: getHeaders(session),
    };
    const { data } = await platform
        .get(exports.PlatformServiceName.Http)
        .get('getaccept/videos', options);
    return data;
};
const createDocument = async (platform, session, document) => {
    const options = {
        headers: getHeaders(session),
    };
    return platform
        .get(exports.PlatformServiceName.Http)
        .post('getaccept/create-document', document, options);
};
const sealDocument = async (platform, session, documentId) => {
    const options = {
        headers: getHeaders(session),
    };
    const payload = {
        document_id: documentId,
    };
    return platform
        .get(exports.PlatformServiceName.Http)
        .post('getaccept/seal-document', payload, options);
};
const uploadDocument = async (platform, session, documentId) => {
    const options = {
        headers: getHeaders(session),
    };
    const payload = {
        document_id: documentId,
    };
    return platform
        .get(exports.PlatformServiceName.Http)
        .post('getaccept/upload-document', payload, options);
};
const removeDocument = async (platform, session, documentId) => {
    const options = {
        headers: getHeaders(session),
    };
    const payload = {
        document_id: documentId,
    };
    return platform
        .get(exports.PlatformServiceName.Http)
        .post('getaccept/delete-document', payload, options);
};
const signup = async (platform, data) => {
    const payload = data;
    return platform
        .get(exports.PlatformServiceName.Http)
        .post('getaccept/signup', payload);
};
const refreshToken = async (platform, session) => {
    const { access_token, expires_in } = session;
    return platform
        .get(exports.PlatformServiceName.Http)
        .post('getaccept/refresh-token', { access_token, expires_in });
};

exports.createDocument = createDocument;
exports.fetchDocumentDetails = fetchDocumentDetails;
exports.fetchEntity = fetchEntity;
exports.fetchLimeDocuments = fetchLimeDocuments;
exports.fetchMe = fetchMe;
exports.fetchSentDocuments = fetchSentDocuments;
exports.fetchTemplateFields = fetchTemplateFields;
exports.fetchTemplates = fetchTemplates;
exports.fetchVideos = fetchVideos;
exports.refreshToken = refreshToken;
exports.removeDocument = removeDocument;
exports.sealDocument = sealDocument;
exports.signup = signup;
exports.switchEntity = switchEntity;
exports.uploadDocument = uploadDocument;
