from aoa.model_utility.base_model import BaseModel
import json
import os
import importlib
import logging
import shutil
import sys


class EvaluateModel(BaseModel):

    def __init__(self, model_utility):
        super().__init__(model_utility)
        self.logger = logging.getLogger(__name__)

    def evaluate_model_local(self, model_id: str = None, base_path: str = None, data_conf: dict = None):
        base_path = self.model_utility.model_catalog_path if base_path is None else os.path.join(base_path, '')
        model_path = base_path + 'model_definitions/'

        if not os.path.exists(model_path):
            raise ValueError("model directory {0} does not exist".format(model_path))

        if model_id is None:
            if "id" in self.model_utility.model:
                model_id = self.model_utility.model["id"]
            else:
                BaseModel.get_model_id(model_path)

        model_artefacts_path = ".artefacts/{}".format(model_id)
        model_evaluation_path = "{}/evaluation".format(model_artefacts_path)

        if not os.path.exists("{}/output".format(model_artefacts_path)):
            raise ValueError("You must run training before trying to run evaluation.")

        if os.path.exists(model_evaluation_path):
            self.logger.debug("Cleaning local model evaluation path: {}".format(model_evaluation_path))
            shutil.rmtree(model_evaluation_path)

        os.makedirs("{}/output".format(model_evaluation_path))

        try:
            self.__cleanup()

            os.makedirs("./artifacts")

            os.symlink("../{}/output/".format(model_artefacts_path), "./artifacts/input", target_is_directory=True)

            os.symlink("../{}/evaluation/output/".format(model_artefacts_path), "./artifacts/output", target_is_directory=True)

            if not os.path.exists("./models"):
                os.symlink("{}/output".format(model_artefacts_path), "./models", target_is_directory=True)

            model_dir = model_path + model_id

            with open(model_dir + "/model.json", 'r') as f:
                model_definition = json.load(f)

            with open(model_dir + "/config.json", 'r') as f:
                model_conf = json.load(f)

            self.logger.info("Loading and executing model code")

            cli_model_kargs = self._BaseModel__get_model_varargs(model_id)

            engine = self._BaseModel__get_engine(model_definition, "evaluation")
            if engine == "python" or engine == "pyspark":
                if engine == "pyspark":
                    self._BaseModel__configure_pyspark(model_definition, model_artefacts_path, model_dir, "evaluation")

                sys.path.append(model_dir)
                if os.path.isfile("{}/model_modules/evaluation.py".format(model_dir)):
                    evaluation = importlib.import_module(".evaluation", package="model_modules")
                else:
                    logging.debug("No evaluation.py found. Using scoring.py -> evaluate")
                    evaluation = importlib.import_module(".scoring", package="model_modules")

                evaluation.evaluate(data_conf, model_conf, **cli_model_kargs)

            elif engine == "sql":
                self.__evaluate_sql(model_dir, data_conf, model_conf, **cli_model_kargs)

            elif engine == "R":
                self._BaseModel__run_r_model(model_id, base_path, data_conf, "evaluate")

            else:
                raise Exception("Unsupported language: {}".format(model_definition["language"]))

            if os.path.exists("{}/evaluation/output/".format(model_artefacts_path)):
                self.logger.info("Artefacts can be found in: {}/evaluation/output/".format(model_artefacts_path))
            else:
                self.logger.info("Artefacts can be found in: {}".format(model_artefacts_path))

            if os.path.exists("{}/evaluation/output/metrics.json".format(model_artefacts_path)):
                self.logger.info("Evaluation metrics can be found in: {}/evaluation/output/metrics.json".format(model_artefacts_path))

            if os.path.exists("{}/evaluation.json".format(model_artefacts_path)):
                self.logger.info("Evaluation metrics can be found in: {}/evaluation.json".format(model_artefacts_path))

            self.__cleanup()
        except:
            self.__cleanup()
            self.logger.exception("Exception running model code")
            raise

    def __cleanup(self):
        if os.path.exists("./artifacts"):
            shutil.rmtree("./artifacts")
        try:
            os.remove("./models")
        except FileNotFoundError:
            self.logger.debug("Nothing to remove, folder './models' does not exists.")

    def __evaluate_sql(self, model_dir, data_conf, model_conf, **kwargs):
        from teradataml import create_context
        from teradataml.dataframe.dataframe import DataFrame
        from teradataml.context.context import get_connection

        self.logger.info("Starting evaluation...")

        create_context(host=data_conf["hostname"],
                       username=os.environ["TD_USERNAME"],
                       password=os.environ["TD_PASSWORD"],
                       logmech=os.getenv("TD_LOGMECH", "TDNEGO"))

        sql_file = model_dir + "/model_modules/evaluation.sql"
        jinja_ctx = {
            "data_conf": data_conf,
            "model_conf": model_conf,
            "model_table": kwargs.get("model_table"),
            "model_version": kwargs.get("model_version"),
            "model_id": kwargs.get("model_id")
        }

        self._BaseModel__execute_sql_script(get_connection(), sql_file, jinja_ctx)

        self.logger.info("Finished evaluation")

        stats = DataFrame(data_conf["metrics_table"]).to_pandas()
        metrics = dict(zip(stats.key, stats.value))

        with open("models/evaluation.json", "w+") as f:
            json.dump(metrics, f)

        self.logger.info("Saved metrics")
