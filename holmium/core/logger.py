"""
global logger
"""
import logging
#: shared stream logger for all holmium classes
# pylint: disable=invalid-name
log = logging.Logger("holmium.core")
log.setLevel(logging.INFO)
_shandler = logging.StreamHandler()
_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(_format)
_shandler.setFormatter(formatter)
log.addHandler(_shandler)
