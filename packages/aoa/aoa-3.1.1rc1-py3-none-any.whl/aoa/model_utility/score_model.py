from aoa.model_utility.base_model import BaseModel
import json
import os
import importlib
import logging
import shutil
import sys


class ScoreModel(BaseModel):

    def __init__(self, model_utility):
        super().__init__(model_utility)
        self.logger = logging.getLogger(__name__)

    def batch_score_model_local(self, model_id: str = None, base_path: str = None, data_conf: dict = None):
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

        if not os.path.exists("{}/output".format(model_artefacts_path)):
            raise ValueError("You must run training before trying to run scoring.")

        try:
            self.__cleanup()

            os.makedirs("./artifacts")

            os.symlink("../{}/output/".format(model_artefacts_path), "./artifacts/input", target_is_directory=True)

            # legacy models folder
            if not os.path.exists("./models"):
                os.symlink("{}/output".format(model_artefacts_path), "./models", target_is_directory=True)

            model_dir = model_path + model_id

            with open(model_dir + "/model.json", 'r') as f:
                model_definition = json.load(f)

            with open(model_dir + "/config.json", 'r') as f:
                model_conf = json.load(f)

            self.logger.info("Loading and executing model code")

            cli_model_kargs = {
                "model_id": model_id,
                "model_version": "cli",
                "project_id": self._BaseModel__get_project_id()
            }

            engine = self._BaseModel__get_engine(model_definition, "deployment")
            if engine == "python" or engine == "pyspark":
                if engine == "pyspark":
                    self._BaseModel__configure_pyspark(model_definition, model_artefacts_path, model_dir, "deployment")

                sys.path.append(model_dir)
                scoring = importlib.import_module(".scoring", package="model_modules")
                scoring.score(data_conf, model_conf, **cli_model_kargs)

            elif engine == "sql":
                raise Exception("not supported")

            elif engine == "R":
                self._BaseModel__run_r_model(model_id, base_path, data_conf, "score.batch")

            else:
                raise Exception("Unsupported language: {}".format(model_definition["language"]))

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
