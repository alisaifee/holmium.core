import logging
#: shared stream logger for all holmium classes
log = logging.Logger("holmium.core")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())

