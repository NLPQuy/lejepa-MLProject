# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import os

os.environ["LOGURU_LEVEL"] = os.environ.get("LOGURU_LEVEL", "INFO")

import logging
import sys
from importlib.util import find_spec

from loguru import logger
from omegaconf import OmegaConf

# Handle optional dependencies without importing heavy modules
_enable_sklearn = os.environ.get("SPT_ENABLE_SKLEARN", "0") == "1"
SKLEARN_AVAILABLE = _enable_sklearn and (find_spec("sklearn") is not None)
WANDB_AVAILABLE = find_spec("wandb") is not None

from .__about__ import (
    __author__,
    __license__,
    __summary__,
    __title__,
    __url__,
    __version__,
)
from .utils.lightning_patch import apply_manual_optimization_patch

_LIGHT_IMPORT = os.environ.get("SPT_LIGHT_IMPORT", "1") == "1"

if not _LIGHT_IMPORT:
    from . import backbone, callbacks, data, losses, module, optim, static, utils
    from .backbone.utils import TeacherStudentWrapper
    from .callbacks import (
        EarlyStopping,
        ImageRetrieval,
        LiDAR,
        LoggingCallback,
        ModuleSummary,
        OnlineKNN,
        OnlineProbe,
        OnlineWriter,
        RankMe,
        TeacherStudentCallback,
        TrainerInfo,
    )
    from .callbacks.registry import log, log_dict
    from .manager import Manager
    from .module import Module

    # Conditionally import callbacks that depend on optional packages
    if SKLEARN_AVAILABLE:
        from .callbacks import SklearnCheckpoint
    else:
        SklearnCheckpoint = None

    __all__ = [
        # Availability flags
        "SKLEARN_AVAILABLE",
        "WANDB_AVAILABLE",
        # Callbacks
        "OnlineProbe",
        "SklearnCheckpoint",
        "OnlineKNN",
        "TrainerInfo",
        "LoggingCallback",
        "ModuleSummary",
        "EarlyStopping",
        "OnlineWriter",
        "RankMe",
        "LiDAR",
        "ImageRetrieval",
        "TeacherStudentCallback",
        # Modules
        "utils",
        "data",
        "module",
        "static",
        "optim",
        "losses",
        "callbacks",
        "backbone",
        # Classes
        "Manager",
        "Module",
        "TeacherStudentWrapper",
        "log",
        "log_dict",
        # Package info
        "__author__",
        "__license__",
        "__summary__",
        "__title__",
        "__url__",
        "__version__",
    ]
else:
    __all__ = [
        "SKLEARN_AVAILABLE",
        "WANDB_AVAILABLE",
        "__author__",
        "__license__",
        "__summary__",
        "__title__",
        "__url__",
        "__version__",
    ]

# Register OmegaConf resolvers
OmegaConf.register_new_resolver("eval", eval)

# Setup logging

# Try to install richuru for better formatting if available
try:
    import richuru

    richuru.install()
except ImportError:
    pass


def rank_zero_only_filter(record):
    """Filter to only log on rank 0 in distributed training."""
    import os

    # Check common environment variables for distributed rank
    rank = os.environ.get("RANK", os.environ.get("LOCAL_RANK", "0"))
    return rank == "0" and record["level"].no >= logger.level("INFO").no


_FILE_COL_WIDTH = 12
_LEVEL_MAP = {"WARNING": "WARN", "SUCCESS": "OK"}


def _log_format(record):
    name = record["file"].name
    if len(name) > _FILE_COL_WIDTH:
        name = name[: _FILE_COL_WIDTH - 1] + "~"
    name = name.ljust(_FILE_COL_WIDTH)
    level = _LEVEL_MAP.get(record["level"].name, record["level"].name)
    level = level.ljust(5)
    return (
        f"<green>{{time:HH:mm:ss}}</green> | <level>{level}</level> | "
        f"<cyan>{name}</cyan>| <level>{{message}}</level>\n{{exception}}"
    )


logger.remove()
logger.add(
    sys.stdout,
    format=_log_format,
    filter=rank_zero_only_filter,
    level="INFO",
)


# Redirect standard logging to loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger.log(record.levelname, record.getMessage())
        # Get corresponding Loguru level if it exists
        # try:
        #     level = logger.level(record.levelname).name
        # except ValueError:
        #     level = "INFO"

        # Find caller from where originated the log message
        # frame, depth = logging.currentframe(), 2
        # while frame.f_code.co_filename == logging.__file__:
        #     frame = frame.f_back
        #     depth += 1
        # logger.opt(depth=depth, exception=record.exc_info).log(
        #     level, record.getMessage()
        # )


# Remove all handlers associated with the root logger object
logging.root.handlers = []
logging.basicConfig(handlers=[InterceptHandler()], level="INFO")

if not _LIGHT_IMPORT:
    # Try to set datasets logging verbosity if available
    try:
        import datasets

        datasets.logging.set_verbosity_info()
    except (ModuleNotFoundError, AttributeError):
        # AttributeError can occur with pyarrow version incompatibilities
        pass

    # Apply Lightning patch for manual optimization parameter support
    apply_manual_optimization_patch()
