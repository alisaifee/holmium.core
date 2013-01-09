import logging
#: shared stream logger for all holmium classes
log = logging.Logger("holmium.core")
log.setLevel(logging.INFO)
shandler = logging.StreamHandler()
format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(format)
shandler.setFormatter(formatter)
log.addHandler(shandler)
