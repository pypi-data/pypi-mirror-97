import re, os
from kolibri.utils.dict import Dict

homedir = os.path.expanduser("~")
resources_path = os.path.join(os.sep, homedir+os.sep, "kolibri_data")


data = Dict({
    'MIN_EXAMPLES_PER_CLASS': 15,
    'MIN_EXAMPLES_PER_ENTITY': 2
})

# [entity_text](entity_type(:entity_synonym)?)
ent_regex = re.compile(r'\[(?P<entity_text>[^\]]+)'
                       r'\]\((?P<entity>[^:)]*?)'
                       r'(?:\:(?P<text>[^)]+))?\)')

DEFAULT_SERVER_PORT = 5005

MINIMUM_COMPATIBLE_VERSION = "0.0.1"

DEFAULT_NLU_FALLBACK_THRESHOLD = 0.0

DEFAULT_CORE_FALLBACK_THRESHOLD = 0.0

DEFAULT_REQUEST_TIMEOUT = 60 * 5  # 5 minutes

DEFAULT_SERVER_FORMAT = "http://localhost:{}"

DEFAULT_SERVER_URL = DEFAULT_SERVER_FORMAT.format(DEFAULT_SERVER_PORT)

corenlp = Dict({
    'LIBRARY_PATH': '/Users/mbenhaddou/Stanford/stanford-corenlp-full-2018-02-27/',
    'PORT': 9000,
    'D2V_MODEL_PATH': "/Users/mbenhaddou/Documents/Mentis/Developement/Python/Kolibri/kolibri/features/doc2vec/model"
})

modeling = Dict({
    # How many classes are at max put into the output class ranking, everything else will be cut off
    'TARGET_RANKING_LENGTH': 10
})

dialog = Dict({
    'INTENT_MESSAGE_PREFIX': "/",
    'DEFAULT_FALLBACK_ACTION': "action_default_fallback",
    'USER_INTENT_RESTART': "/restart",  # dINTENT_MESSAGE_PREFIX +
    'DOCS_BASE_URL': '.',
    'FALLBACK_SCORE': 1.1
})
