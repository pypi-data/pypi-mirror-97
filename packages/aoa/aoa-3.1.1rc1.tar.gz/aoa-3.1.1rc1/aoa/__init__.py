__version__="3.1.1rc1"

# import client
from aoa.api_client import AoaClient

# import APIs into api package
from aoa.api.dataset_api import DatasetApi
from aoa.api.dataset_template_api import DatasetTemplateApi
from aoa.api.dataset_connection_api import DatasetConnectionApi
from aoa.api.model_api import ModelApi
from aoa.api.project_api import ProjectApi
from aoa.api.trainer_api import TrainerApi
from aoa.api.trained_model_api import TrainedModelApi
from aoa.api.trained_model_event_api import TrainedModelEventApi
from aoa.api.trained_model_artefacts_api import TrainedModelArtefactsApi
from aoa.api.job_api import JobApi
from aoa.api.job_event_api import JobEventApi
from aoa.api.deployment_api import DeploymentApi
from aoa.api.api_iterator import ApiIterator
from aoa.api.message_api import MessageApi

# import repo into api package
from aoa.model_utility.model_utility import ModelUtility
from aoa.model_utility.evaluate_model import EvaluateModel
from aoa.model_utility.score_model import ScoreModel
from aoa.model_utility.train_model import TrainModel
from aoa.model_utility.base_model import BaseModel
