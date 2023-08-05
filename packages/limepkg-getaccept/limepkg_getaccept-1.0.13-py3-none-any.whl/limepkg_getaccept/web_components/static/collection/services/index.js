import { PlatformServiceName, } from '@limetech/lime-web-components-interfaces';
export const fetchMe = async (platform, session) => {
    const options = {
        headers: getHeaders(session),
    };
    const { data } = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/me', options);
    return data;
};
export const switchEntity = async (entity_id, platform, session) => {
    const options = {
        headers: getHeaders(session),
    };
    const payload = {
        entity_id,
    };
    const { data } = await platform
        .get(PlatformServiceName.Http)
        .post('getaccept/switch-entity', payload, options);
    return data;
};
export const fetchLimeDocuments = async (platform, limetype, record_id, selectedLimeDocument) => {
    const options = {
        params: {
            limetype,
            record_id: record_id.toString(),
        },
    };
    const documents = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/documents', options);
    return documents.map(document => ({
        text: document.comment,
        value: document.id,
        icon: 'document',
        iconColor: 'var(--lime-green)',
        selected: selectedLimeDocument && selectedLimeDocument.value === document.id,
    }));
};
export const fetchSentDocuments = async (platform, externalId, session) => {
    const options = {
        headers: {
            'ga-auth-token': session.access_token,
        },
        params: {
            external_id: externalId,
        },
    };
    const { documents } = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/sent-documents', options);
    return documents;
};
export const fetchTemplates = async (platform, session, selectedTemplate) => {
    const options = {
        headers: {
            'ga-auth-token': session.access_token,
        },
    };
    const { templates = [] } = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/templates', options);
    return templates.map((template) => ({
        text: template.name,
        value: template.id,
        icon: 'document',
        iconColor: 'var(--lime-orange)',
        selected: selectedTemplate && selectedTemplate.value === template.id,
    }));
};
export const fetchTemplateFields = async (platform, session, limetype, record_id, selectedTemplate) => {
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
        .get(PlatformServiceName.Http)
        .get('getaccept/template-fields', options);
    return fields;
};
const getHeaders = (session) => {
    return {
        'ga-auth-token': session.access_token,
    };
};
export const fetchEntity = async (platform, session) => {
    const options = {
        headers: getHeaders(session),
    };
    const { data } = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/entity', options);
    return data;
};
export const fetchDocumentDetails = async (platform, session, document_id) => {
    const options = {
        headers: getHeaders(session),
        params: {
            document_id,
        },
    };
    const { data } = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/document-details', options);
    return data;
};
export const fetchVideos = async (platform, session) => {
    const options = {
        headers: getHeaders(session),
    };
    const { data } = await platform
        .get(PlatformServiceName.Http)
        .get('getaccept/videos', options);
    return data;
};
export const createDocument = async (platform, session, document) => {
    const options = {
        headers: getHeaders(session),
    };
    return platform
        .get(PlatformServiceName.Http)
        .post('getaccept/create-document', document, options);
};
export const sendDocument = async (platform, session, documentId) => {
    const options = {
        headers: getHeaders(session),
    };
    const payload = {
        document_id: documentId,
    };
    return platform
        .get(PlatformServiceName.Http)
        .post('getaccept/send-document', payload, options);
};
export const sealDocument = async (platform, session, documentId) => {
    const options = {
        headers: getHeaders(session),
    };
    const payload = {
        document_id: documentId,
    };
    return platform
        .get(PlatformServiceName.Http)
        .post('getaccept/seal-document', payload, options);
};
export const uploadDocument = async (platform, session, documentId) => {
    const options = {
        headers: getHeaders(session),
    };
    const payload = {
        document_id: documentId,
    };
    return platform
        .get(PlatformServiceName.Http)
        .post('getaccept/upload-document', payload, options);
};
export const removeDocument = async (platform, session, documentId) => {
    const options = {
        headers: getHeaders(session),
    };
    const payload = {
        document_id: documentId,
    };
    return platform
        .get(PlatformServiceName.Http)
        .post('getaccept/delete-document', payload, options);
};
export const signup = async (platform, data) => {
    const payload = data;
    return platform
        .get(PlatformServiceName.Http)
        .post('getaccept/signup', payload);
};
export const refreshToken = async (platform, session) => {
    const { access_token, expires_in } = session;
    return platform
        .get(PlatformServiceName.Http)
        .post('getaccept/refresh-token', { access_token, expires_in });
};
