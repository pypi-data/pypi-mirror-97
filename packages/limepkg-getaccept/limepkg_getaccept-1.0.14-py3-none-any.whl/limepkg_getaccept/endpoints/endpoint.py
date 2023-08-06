import lime_webserver.webserver as webserver
from webargs import ValidationError
from lime_application import LimeApplication
from flask import request, Response
import requests
import logging
from ..endpoints import api
from ..common import get_ga_token
from ..getaccept import GetAccept
from ..lime_helpers import search_lime_objects, get_documents, get_file_data
from .schemas import (
    AuthSchema,
    CreateDocumentSchema,
    GADocumentSchema,
    LimeDocumentSchema,
    RefreshTokenSchema,
    SchemaWithLimeObject,
    SearchPersonSchema,
    SentDocumentsSchema,
    SignupSchema,
    SwitchEntitySchema,
    TemplatesSchema,
    TemplateSchema,
    validate_args
)


logger = logging.getLogger(__name__)


# Change this for admin configurable config later
config = {
    'person': {
        'limetype': 'person',
        'properties': {
            'name': 'name',
            'email': 'email',
            'phone': 'mobilephone',
            'company': 'company',
        }
    },
    'coworker': {
        'limetype': 'coworker',
        'properties': {
            'name': 'name',
            'email': 'email',
            'phone': 'mobilephone',
        }
    },
}


class Login(webserver.LimeResource):
    def post(self):
        args = request.get_json()
        schema = AuthSchema()
        params = validate_args(request, args, schema)
        return GetAccept().login(params['email'], params['password'])


class RefreshToken(webserver.LimeResource):
    def post(self):
        args = request.get_json()
        schema = RefreshTokenSchema()
        params = validate_args(request, args, schema)
        return GetAccept().test_token(**params)


class Signup(webserver.LimeResource):
    def post(self):
        args = request.get_json()
        schema = SignupSchema()
        params = validate_args(request, args, schema)
        return GetAccept().signup(**params)


class GATemplates(webserver.LimeResource):
    def get(self):
        schema = TemplatesSchema()
        token = get_ga_token(request.headers.get('ga-auth-token', None))
        params = validate_args(request, request.args, schema)
        return GetAccept().fetch_templates(params, token)


class GATemplateFields(webserver.LimeResource):
    def get(self):
        app: LimeApplication = self.application
        token = get_ga_token(request.headers.get('ga-auth-token', None))

        schema = TemplateSchema()
        schema.context['application'] = app
        params = validate_args(request, request.args, schema)
        limetype = params['limetype']
        record_id = params['record_id']
        template_id = params['template_id']

        limeobject = app.limetypes.get_limetype(
            limetype).get(record_id)
        if not limeobject:
            raise ValidationError('No such limeobject')

        return GetAccept().fetch_template_fields(
            limeobject, template_id, token)


class GAUserProfile(webserver.LimeResource):
    def get(self):
        token = get_ga_token(request.headers.get('ga-auth-token', None))
        return GetAccept().fetch_me(token)


class GASwitchEntity(webserver.LimeResource):
    def post(self):
        args = request.get_json()
        schema = SwitchEntitySchema()
        token = get_ga_token(request.headers.get('ga-auth-token', None))
        params = validate_args(request, args, schema)
        return GetAccept().refresh_token(params['entity_id'], token)


class Persons(webserver.LimeResource):
    def get(self):
        schema = SearchPersonSchema()
        params = validate_args(request, request.args, schema)

        app: LimeApplication = self.application
        return search_lime_objects(
            app,
            config['person'],
            params['search'],
            params['limit'],
            params['offset']
        )


class Coworkers(webserver.LimeResource):
    def get(self):
        schema = SearchPersonSchema()
        params = validate_args(request, request.args, schema)
        app: LimeApplication = self.application
        return search_lime_objects(
            app,
            config['coworker'],
            params['search'],
            params['limit'],
            params['offset']
        )


class GASentDocuments(webserver.LimeResource):
    def get(self):
        token = get_ga_token(request.headers.get('ga-auth-token', None))
        schema = SentDocumentsSchema()
        params = validate_args(request, request.args, schema)
        external_id = params['external_id']

        return GetAccept().fetch_sent_documents(
            {'external_id': external_id}, token
        )


class GACreateDocument(webserver.LimeResource):
    def post(self):
        token = get_ga_token(request.headers.get('ga-auth-token', None))
        schema = CreateDocumentSchema()
        params = validate_args(request, request.get_json(), schema)
        return GetAccept().create_document(params, token)


class GASealDocument(webserver.LimeResource):
    def post(self):
        token = get_ga_token(request.headers.get('ga-auth-token', None))
        schema = GADocumentSchema()
        params = validate_args(request, request.get_json(), schema)
        return GetAccept().seal_document(params['document_id'], token)
        return GetAccept().create_document(params, token)


class GADeleteDocument(webserver.LimeResource):
    def post(self):
        token = get_ga_token(request.headers.get('ga-auth-token', None))
        schema = GADocumentSchema()
        params = validate_args(request, request.get_json(), schema)
        return GetAccept().delete_document(params['document_id'], token)


class GASendDocument(webserver.LimeResource):
    def post(self):
        token = get_ga_token(request.headers.get('ga-auth-token', None))
        schema = GADocumentSchema()
        params = validate_args(request, request.get_json(), schema)
        return GetAccept().send_document(params['document_id'], token)


class Entity(webserver.LimeResource):
    def get(self):
        token = get_ga_token(request.headers.get('ga-auth-token', None))
        return GetAccept().entity(token)


class GADocumentDetails(webserver.LimeResource):
    def get(self):
        token = get_ga_token(request.headers.get('ga-auth-token', None))
        schema = GADocumentSchema()
        params = validate_args(request, request.args, schema)
        document_id = params['document_id']
        return GetAccept().fetch_document_detail(
            document_id, token)


class UploadDocument(webserver.LimeResource):
    def post(self):
        token = get_ga_token(request.headers.get('ga-auth-token', None))
        schema = LimeDocumentSchema()
        params = validate_args(request, request.get_json(), schema)
        file = get_file_data(self.application, params['document_id'])
        return GetAccept().upload_file(file.filename, file.stream, token)


class Videos(webserver.LimeResource):
    def get(self):
        token = get_ga_token(request.headers.get('ga-auth-token', None))
        return GetAccept().videos(token)


class PageThumbProxy(webserver.LimeResource):
    def get(self, bucket, entity_id, document_id, page_id, s3_credentials):
        host = 'https://{bucket}.s3.{region}.amazonaws.com'.format(
            bucket=bucket, region=bucket.replace('ga-', ''))
        req = requests.get(
            '{host}/{entity_id}/document/{document_id}/thumb/{page_id}.png?{s3_credentials}'.format(  # noqa
                host=host,
                entity_id=entity_id,
                document_id=document_id,
                page_id=page_id,
                s3_credentials=s3_credentials)
        )

        return Response(
            response=req.content,
            status=200,
            mimetype=req.headers.get('content-type'))


class ThumbProxy(webserver.LimeResource):
    def get(self, url_path, path):
        host = 'https://media.getaccept.com'
        req = requests.get(
            '{host}/{url_path}/{path}'.format(
                host=host, url_path=url_path, path=path)
        )

        return Response(
            response=req.content,
            status=200,
            mimetype=req.headers.get('content-type'))


class PreviewProxy(webserver.LimeResource):
    def get(self, entity_id, template_id):
        host = 'https://media.getaccept.com/preview'

        req = requests.get(
            '{host}/{entity_id}/{template_id}.png'.format(
                host=host,
                entity_id=entity_id,
                template_id=template_id)
        )

        return Response(response=req.content,
                        status=200, mimetype=req.headers.get('content-type'))


class VideoThumbProxy(webserver.LimeResource):
    def get(self, video_id, image):
        host = 'https://video.getaccept.com'

        req = requests.get(
            '{host}/{video_id}/{image}'.format(host=host,
                                               video_id=video_id, image=image)
        )
        return Response(
            response=req.content,
            status=200,
            mimetype=req.headers.get('content-type'))


class LimeDocuments(webserver.LimeResource):
    def get(self):
        schema = SchemaWithLimeObject()
        schema.context['application'] = self.application
        params = validate_args(request, request.args, schema)

        return get_documents(
            self.application,
            params['limetype'],
            params['record_id'])


class GALogos(webserver.LimeResource):
    def get(self, logo):
        if logo not in ['logo-inverted', 'logo', 'logo_only']:
            return Response(status=404)
        url = 'https://static-vue.getaccept.com/img/{logo}.png'.format(
            logo=logo)
        req = requests.get(url)
        return Response(
            response=req.content,
            status=200,
            mimetype=req.headers.get('content-type'))


api.add_resource(Login, '/login/')
api.add_resource(GATemplates, '/templates')
api.add_resource(GATemplateFields, '/template-fields')
api.add_resource(GAUserProfile, '/me')
api.add_resource(GASwitchEntity, '/switch-entity')
api.add_resource(Persons, '/persons')
api.add_resource(Coworkers, '/coworkers')
api.add_resource(GASentDocuments, '/sent-documents')
api.add_resource(GACreateDocument, '/create-document')
api.add_resource(GASealDocument, '/seal-document')
api.add_resource(GASendDocument, '/send-document')
api.add_resource(Signup, '/signup')
api.add_resource(RefreshToken, '/refresh-token')
api.add_resource(Entity, '/entity')
api.add_resource(GADocumentDetails, '/document-details')
api.add_resource(Videos, '/videos')
api.add_resource(GADeleteDocument, '/delete-document')
api.add_resource(PreviewProxy, '/preview_proxy/<entity_id>/<template_id>')
api.add_resource(ThumbProxy, '/thumb_proxy/<url_path>/<path>')
api.add_resource(
    PageThumbProxy,
    '/page_thumb_proxy/<bucket>/<entity_id>/<document_id>/<page_id>/<s3_credentials>')  # noqa
api.add_resource(VideoThumbProxy, '/video_thumb_proxy/<video_id>/<image>')
api.add_resource(LimeDocuments, '/documents')
api.add_resource(UploadDocument, '/upload-document')
api.add_resource(GALogos, '/logos/<logo>')
