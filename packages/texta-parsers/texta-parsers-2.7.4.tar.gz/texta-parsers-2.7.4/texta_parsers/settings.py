import os
#field which is used to store meta information about the file in ElasticSearch, e.g. path, extension, type
META_FIELD = "properties"
ES_URL = os.getenv("DOCPARSER_ES_URL", "http://localhost:9200")
BROKER_URL = "redis://localhost:6379/0"
RESULT_BACKEND_URL = "redis://localhost:6379/0"

FACE_VECTOR_FIELD_NAME = "texta_face_vectors"
