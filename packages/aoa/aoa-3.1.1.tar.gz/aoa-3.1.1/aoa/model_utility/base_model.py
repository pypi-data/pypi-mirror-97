import logging
import json
import yaml
import os
import uuid
from jinja2 import Template


class BaseModel(object):

    def __init__(self, model_utility):
        self.model_utility = model_utility

    @staticmethod
    def get_model_id(model_path, rtn_val=False):
        catalog = {}
        index = 0
        model_ids = "Use one of the following models\n"

        for model in os.listdir(model_path):
            if os.path.exists(model_path + model + "/model.json"):
                with open(model_path + model + "/model.json", 'r') as f:
                    model_definition = json.load(f)
                    catalog[index] = model_definition
                    index += 1

        for key in catalog:
            model_ids += "{1}: {0}\n".format(catalog[key]["id"], catalog[key]["name"])

        if rtn_val:
            return catalog

        raise ValueError(model_ids)

    def __get_model_varargs(self, model_id):
        return {
            "model_id": model_id,
            "model_version": "cli",
            "model_table": "AOA_MODELS_cli",
            "project_id": self.__get_project_id(),
            "job_id": str(uuid.uuid4())
        }

    def __get_project_id(self):
        path = os.path.join(self.model_utility.base_path, ".aoa/config.yaml")
        with open(path, "r") as handle:
            return yaml.safe_load(handle)["project_id"]

    def __template_sql_script(self, filename, jinja_ctx):
        with open(filename) as f:
            template = Template(f.read())

        return template.render(jinja_ctx)

    def __execute_sql_script(self, conn, filename, jinja_ctx):
        script = self.__template_sql_script(filename, jinja_ctx)

        stms = script.split(';')

        for stm in stms:
            stm = stm.strip()
            if stm:
                logging.info("Executing statement: {}".format(stm))

                try:
                    conn.execute(stm)
                except Exception as e:
                    if stm.startswith("DROP"):
                        logging.warning("Ignoring DROP statement exception")
                    else:
                        raise e

    def __configure_pyspark(self, model_definition, model_artefacts_path, model_dir, mode):
        import findspark
        import os
        from zipfile import ZipFile
        from os.path import basename, relpath
        import tempfile

        # zip up model files for py-files
        base_zip_path = model_dir + "/model_modules"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as model_modules_fp:
            with ZipFile(model_modules_fp, 'w') as zip:
                for folder_name, _, filenames in os.walk(base_zip_path):
                    for filename in filenames:
                        full_file_path = os.path.join(folder_name, filename)
                        zip_path = relpath(full_file_path, base_zip_path)
                        zip.write(full_file_path, zip_path)

        # read the spark submit resources for the model
        try:
            # current structure
            if "automation" in model_definition and mode in model_definition["automation"]:
                resources = model_definition["automation"][mode]["resources"]
            # legacy 1
            elif "resources" in model_definition:
                resources = model_definition["resources"]["training"]
            # legacy 2
            else:
                resources = model_definition["automation"]["resources"]["training"]
        except KeyError as e:
            raise Exception("pyspark models require an (automation)->resources->training section in model.json")

        aoa_spark_conf = os.environ.get("AOA_SPARK_CONF", "--conf spark.aoa.modelPath={}".format(model_artefacts_path))

        # legacy support for master being specified as separate property. this should be moved to the args var now
        specific_master_arg = ""
        if "master" in resources:
            specific_master_arg = "--master {}".format(resources["master"])

        os.environ["PYSPARK_SUBMIT_ARGS"] = "{} {} --py-files {} {} pyspark-shell".format(
            specific_master_arg, resources["args"], model_modules_fp.name, aoa_spark_conf)

        # SPARK_HOME should be set
        spark_home = findspark.find()
        findspark.init(spark_home)

        self.logger.info("Using SPARK_HOME: {}".format(spark_home))
        self.logger.info("Using PYSPARK_SUBMIT_ARGS: {}".format(os.environ["PYSPARK_SUBMIT_ARGS"]))
        self.logger.info("Using AOA_SPARK_CONF: {}".format(os.environ.get("AOA_SPARK_CONF", "")))

    def __get_engine(self, model_definition, mode):
        if "automation" in model_definition:

            if mode in model_definition["automation"] and "engine" in model_definition["automation"][mode]:
                return model_definition["automation"][mode]["engine"]

            # legacy
            if "trainingEngine" in model_definition["automation"]:
                return model_definition["automation"]["trainingEngine"]

        return model_definition["language"]

    def __run_r_model(self, model_id, base_path, data_conf, mode):
        import tempfile
        import subprocess

        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(json.dumps(data_conf).encode())

        cmd = f"{self.model_utility.dir_path}/run_model.R {model_id} {self.__get_project_id()} {mode} {fp.name} {base_path}"
        subprocess.check_call(cmd, shell=True)

