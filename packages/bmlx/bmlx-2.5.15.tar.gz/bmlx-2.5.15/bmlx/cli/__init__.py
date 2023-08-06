import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# disable tensorflow info logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "1"
