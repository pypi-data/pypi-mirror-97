# Copyright IBM Corp. 2020. All Rights Reserved.

import sys

from .client import CPDOrchestration
from .cpd_paths import CpdScope, CpdPath
from .version import __version__

if sys.version_info[0] == 2:
    import logging

    logger = logging.getLogger('ibm_cpd_orchestration_initialization')
    logger.warning("Python 2 is not supported.")