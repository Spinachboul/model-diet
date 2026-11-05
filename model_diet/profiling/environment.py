
import platform
import psutil
import sys
import os

import sklearn
import numpy as np

try:
    import xgboost
    xgb_version = xgboost.__version__
except ImportError:
    xgb_version = None


def collect_environment():

    return {

        "python_version": sys.version,

        "platform": platform.platform(),

        "processor": platform.processor(),

        "cpu_count_logical": psutil.cpu_count(
            logical=True
        ),

        "cpu_count_physical": psutil.cpu_count(
            logical=False
        ),

        "total_ram_gb": round(
            psutil.virtual_memory().total / (1024 ** 3), 2
        ),

        "cpu_frequency_mhz": (
            psutil.cpu_freq().current
            if psutil.cpu_freq() else None
        ),

        "numpy_version": np.__version__,

        "sklearn_version": sklearn.__version__,

        "xgboost_version": xgb_version,

        "thread_environment": {
            key: os.environ.get(key)
            for key in [
                "OMP_NUM_THREADS",
                "MKL_NUM_THREADS",
                "OPENBLAS_NUM_THREADS",
                "NUMEXPR_NUM_THREADS"
            ]
        }
    }
