from lime_filter import Filter, OrOperator, EqualsOperator
from lime_filter.filter import LikeOperator
from lime_type.unit_of_work import _serialize_properties_and_values
from lime_type.limeobjects import (BelongsToPropertyAccessor,
                                   OptionPropertyAccessor,
                                   SetPropertyAccessor)


def get_filter(config, value):
    filter = None
    for key, field in config['properties'].items():
        operator = LikeOperator(field, value)
        if not filter:
            filter = operator
            continue
        filter = OrOperator(operator, filter)
    return Filter(filter)


def search_lime_objects(app, limetype_config, search, limit, offset):
    limetype = app.limetypes.get_limetype(limetype_config['limetype'])
    filter = get_filter(limetype_config, search)
    return [_serialize_properties_and_values(get_lime_values(obj))
            for obj in limetype.get_all(
                filter=filter, limit=limit, offset=offset
    )]


def get_documents(app, limetype, record_id):
    documents = app.limetypes.get_limetype('document').get_all(
        filter=Filter(EqualsOperator(limetype, record_id)))
    return [dict(**doc.values(), id=doc.id) for doc in documents]


def match_merge_fields(limeobject, data):
    fields = data.get('fields', [])
    for field in fields:
        value = get_merge_field_value(limeobject, field)
        field.update({'field_value': value})
    return fields


def get_file_data(app, document_id):
    document = app.limetypes.get_limetype('document').get(document_id)
    return document.properties.document.fetch()


def get_merge_field_value(limeobject, field):
    if not field.get('field_label', None):
        return field['field_value']
    try:
        key = field['field_value'].replace(
            '{{', '').replace('}}', '').split('.')[1]

        value = _serialize_properties_and_values(
            get_lime_values(limeobject))[key]
        return value
    except Exception:
        return field['field_value']


def get_lime_values(limeobject):
    def extract_value(prop):
        if isinstance(prop, BelongsToPropertyAccessor):
            return prop.descriptive
        if isinstance(prop, OptionPropertyAccessor):
            return prop.value.key
        if isinstance(prop, SetPropertyAccessor):
            return [p.key for p in prop.value]
        return prop.value

    props = limeobject.get_properties_with_value()
    values = {
        prop.name: extract_value(prop)
        for prop in props
    }

    values.update(limeobject._system_properties)
    return values
