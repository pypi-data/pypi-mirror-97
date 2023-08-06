import json
from cloudpretrain.constants import COMPLETED_JOB_STATUS,FAILED_JOB_STATUS
from cloudpretrain.utils.cloudml import get_task_state, Cloud_ml_task_type
from enum import Enum
import pickle


class Cloud_ml_task:
    def __init__(self, name, task_type, model_name = None, version = "1", state = None, predict_file_path = None, algorithm = None, model_params = None, data_params = None):
        self.name = name
        self.task_type = task_type
        self.version = version
        self.state = state
        self.model = model_name
        self.dev_metrics = None
        self.export_path = None
        self.predict_file_path = predict_file_path
        self.serving_name = None
        self.test_metrics = None
        self.export_fast = None
        self.export_fp16 = None
        self.enable_server_batching = None
        self.enable_tensorboard = False
        self.algorithm = algorithm
        self.model_params = model_params
        self.data_params = data_params

    def is_finished(self):
        return self.state == COMPLETED_JOB_STATUS or self.state == FAILED_JOB_STATUS

    def get_state(self):
        if self.is_finished():
            return self.state
        
        # check the status from cloudml
        return get_task_state(self.name, self.task_type)
    
    def set_start_time(self, start_time):
        self.start_time = start_time
    
    def set_update_time(self, update_time):
        self.update_time = update_time
    
    def set_dev_metrics(self, dev_metrics):
        self.dev_metrics = dev_metrics
    
    def set_serving_name(self, serving_name):
        self.serving_name = serving_name
    
    def set_export_path(self, export_path):
        self.export_path = export_path
    
    def set_test_metrics(self, test_metrics):
        self.test_metrics = test_metrics


class Bert_params:
    def __init__(self, lr, batch, epoch, seq_len):
        # self.model_type = model_type
        self.learning_rate = lr
        self.epoch = epoch
        self.batch = batch
        self.seq_len = seq_len
    
    def set_num_gpus(self, num_gpus):
        self.num_gpus = num_gpus
    
    def to_str(self):
        return "lr: {}, batch_size: {}, seq_len: {}, epoch: {}".format(self.learning_rate, self.batch, self.seq_len, self.epoch)
    
   
class Job_type(Enum):
    TRAIN = 1
    TEST = 2
    EXPORT = 3
    SERVING = 4
    DELETED = 5


class Classfier_metrics:
    def __init__(self, step, loss):
        self.step = step
        self.loss = loss
    
    def set_acc(self, acc):
        self.acc = acc

    def set_loss(self, loss):
        self.loss = loss
    
    def set_precision(self, precision):
        self.precision = precision
    
    def set_recall(self, recall):
        self.recall = recall
    
    def set_f1(self, f1):
        self.f1 = f1
    
    def to_str(self):
        return "Acc: {0:.3f}, Precision: {1:.3f}, Recall: {2:.3f}, F1: {3:.3f}".format(self.acc, self.precision, self.recall, self.f1)


class Job_info:
    def __init__(self, name, job_type, train_tasks, problem):
        self.name = name
        self.job_types = [job_type]
        self.train_tasks = train_tasks
        self.params = None
        self.problem = problem
        self.predict_tasks = None
        self.export_tasks = None
        self.serving_tasks = None

    def set_dataset(self, dataset_name, dataset_version, team, is_public, group):
        self.dataset_name = dataset_name
        self.dataset_version = dataset_version
        self.dataset_team = team
        self.dataset_public = is_public
        self.dataset_group = group
    
    def to_str(self):
        return pickle.dumps(self)

    # todo: bug here, if override the old tasks, when should we delete it from cloudml?
    def set_predict_tasks(self, predict_tasks):
        if Job_type.TEST not in self.job_types:
            self.job_types.append(Job_type.TEST)
        self.predict_tasks = predict_tasks
    
    # todo: bug here, if override the old tasks, when should we delete it from cloudml?
    def set_export_tasks(self, export_tasks):
        if Job_type.EXPORT not in self.job_types:
            self.job_types.append(Job_type.EXPORT)
        self.export_tasks = export_tasks
    
    # todo: bug here, if override the old tasks, when should we delete it from cloudml?
    def set_serving_tasks(self, serving_tasks):
        if Job_type.SERVING not in self.job_types:
            self.job_types.append(Job_type.SERVING)
        
        self.serving_tasks = serving_tasks
    
    def get_all_cloudml_tasks(self):
        tasks = []

        if self.train_tasks:
            tasks += self.train_tasks
        
        if self.predict_tasks:
            tasks += self.predict_tasks
        
        if self.export_tasks:
            tasks += self.export_tasks
        
        return tasks
    
    def get_all_cloudml_tasks_with_servings(self):
        other_tasks = self.get_all_cloudml_tasks()

        if self.serving_tasks:
            other_tasks += self.serving_tasks

        return other_tasks