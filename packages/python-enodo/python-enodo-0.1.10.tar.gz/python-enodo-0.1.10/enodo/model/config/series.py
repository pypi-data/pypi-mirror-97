import json

from . import ConfigModel
from enodo.jobs import JOB_TYPES


class SeriesJobConfigModel(ConfigModel):
    __slots__ = ('activated', 'model', 'job_schedule', 'model_params')

    def __init__(self, model, job_schedule, model_params, activated=True):

        if not isinstance(activated, bool):
            raise Exception("Invalid series job config")

        if not isinstance(model, str):
            raise Exception("Invalid series job config")

        if not isinstance(job_schedule, int):
            raise Exception("Invalid series job config")

        if not isinstance(model_params, dict):
            raise Exception("Invalid series job config")

        self.activated = activated
        self.model = model
        self.job_schedule = job_schedule
        self.model_params = model_params

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return {
            'activated': self.activated,
            'model': self.model,
            'job_schedule': self.job_schedule,
            'model_params': self.model_params
        }

class SeriesConfigModel(ConfigModel):

    __slots__ = ('job_models', 'min_data_points')
    
    def __init__(self, job_models, min_data_points=None):
        """
        Create new Series Config
        :param job_models: dict of job(key) and model name(value)
        :param job_schedule: dict of job(key) and n_new_points(value)
        :param model_params: dict of model(key) and dict(value)
        :return:
        """

        if not isinstance(job_models, dict):
            raise Exception("Invalid series config")

        self.job_models = {}
        for job_model in job_models:
            jmc = SeriesJobConfigModel.from_dict(job_model)
            self.job_models[job_model.model] = jmc

        if not isinstance(min_data_points, int):
            raise Exception("Invalid series config")

        self.min_data_points = min_data_points

    def get_model_for_job(self, job_type):
        if job_type not in self.job_models:
            return False
        
        return self.job_models.get(job_type)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return {
            'job_models': self.job_models,
            'job_schedule': {key:value.to_dict() for (key,value) in self.job_models.items()},
            'min_data_points': self.min_data_points
        }