from aoa.model_utility.base_model import BaseModel
import shutil
import os
import json
import logging
import importlib
import sys


class TrainModel(BaseModel):

    def __init__(self, model_utility):
        super().__init__(model_utility)
        self.logger = logging.getLogger(__name__)

    def train_model_local(self, model_id: str = None, base_path: str = None, data_conf: dict = None):
        base_path = self.model_utility.model_catalog_path if base_path is None else os.path.join(base_path, '')
        model_path = base_path + 'model_definitions/'

        if not os.path.exists(model_path):
            raise ValueError("model directory {0} does not exist".format(model_path))

        if model_id is None:
            if "id" in self.model_utility.model:
                model_id = self.model_utility.model["id"]
            else:
                BaseModel.get_model_id(model_path)

        model_artefacts_path = ".artefacts/{}/".format(model_id)
        model_artefacts_output_path = ".artefacts/{}/output/".format(model_id)
        if os.path.exists(model_artefacts_path):
            self.logger.debug("Cleaning local model artefact path: {}".format(model_artefacts_path))
            shutil.rmtree(model_artefacts_path)

        os.makedirs(model_artefacts_output_path)

        try:
            if os.path.exists("./artifacts"):
                os.remove("./artifacts")

            if os.path.exists("./models"):
                os.remove("./models")

            os.symlink(model_artefacts_path, "./artifacts", target_is_directory=True)
            os.symlink(model_artefacts_output_path, "./models", target_is_directory=True)

            model_dir = model_path + model_id

            with open(model_dir + "/model.json", 'r') as f:
                model_definition = json.load(f)

            with open(model_dir + "/config.json", 'r') as f:
                model_conf = json.load(f)

            self.logger.info("Loading and executing model code")

            cli_model_kargs = self._BaseModel__get_model_varargs(model_id)

            engine = self._BaseModel__get_engine(model_definition, "training")
            if engine == "python" or engine == "pyspark":
                if engine == "pyspark":
                    self._BaseModel__configure_pyspark(model_definition, model_artefacts_path, model_dir, "training")

                sys.path.append(model_dir)
                training = importlib.import_module(".training", package="model_modules")
                training.train(data_conf, model_conf, **cli_model_kargs)

            elif engine == "sql":
                self.__train_sql(model_dir, data_conf, model_conf, **cli_model_kargs)

            elif engine == "R":
                self._BaseModel__run_r_model(model_id, base_path, data_conf, "train")

            else:
                raise Exception("Unsupported engine: {}".format(engine))

            self.logger.info("Artefacts can be found in: {}".format(model_artefacts_output_path))
            self.__cleanup()
        except:
            self.__cleanup()
            self.logger.exception("Exception running model code")
            raise

    def __cleanup(self):
        if os.path.exists("./artifacts"):
            os.remove("./artifacts")
        if os.path.exists("./models"):
            os.remove("./models")

    def __train_sql(self, model_dir, data_conf, model_conf, **kwargs):
        from teradataml.context.context import get_connection
        from teradataml import create_context

        self.logger.info("Starting training...")

        create_context(host=data_conf["hostname"],
                       username=os.environ["TD_USERNAME"],
                       password=os.environ["TD_PASSWORD"],
                       logmech=os.getenv("TD_LOGMECH", "TDNEGO"))

        sql_file = model_dir + "/model_modules/training.sql"
        jinja_ctx = {
            "data_conf": data_conf,
            "model_conf": model_conf,
            "model_table": kwargs.get("model_table"),
            "model_version": kwargs.get("model_version"),
            "model_id": kwargs.get("model_id")
        }

        self._BaseModel__execute_sql_script(get_connection(), sql_file, jinja_ctx)

        self.logger.info("Finished training")

        self.logger.info("Saved trained model")
