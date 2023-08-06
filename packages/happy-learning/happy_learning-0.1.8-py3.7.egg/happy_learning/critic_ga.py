import copy
import numpy as np
import os
import pandas as pd
import random

from .evaluate_machine_learning import sml_fitness_score
from .feature_selector import FeatureSelector
from .sampler import MLSampler
from .supervised_machine_learning import ModelGeneratorClf, ModelGeneratorReg, PARAM_SPACE_CLF, PARAM_SPACE_REG
from .utils import HappyLearningUtils
from datetime import datetime
from easyexplore.data_import_export import DataExporter
from easyexplore.data_visualizer import DataVisualizer
from easyexplore.utils import Log
from multiprocessing.pool import Pool, ThreadPool
from typing import Dict, List


class ActorException(Exception):
    """
    Class for managing exceptions for class Actor
    """
    pass


class Actor:
    """
    Class for optimizing development of supervised machine learning algorithms by using Genetic Algorithm
    """
    def __init__(self,
                 mode: str,
                 df: pd.DataFrame,
                 target: str,
                 features: List[str] = None,
                 re_split_data: bool = False,
                 re_sample_cases: bool = False,
                 re_sample_features: bool = False,
                 max_features: int = 5,
                 labels: List[str] = None,
                 models: List[str] = None,
                 model_params: Dict[str, str] = None,
                 burn_in_generations: int = -1,
                 warm_start: bool = True,
                 max_generations: int = 50,
                 pop_size: int = 64,
                 mutation_rate: float = 0.1,
                 mutation_prob: float = 0.15,
                 parents_ratio: float = 0.5,
                 early_stopping: int = 0,
                 convergence: bool = True,
                 convergence_measure: str = 'min',
                 timer_in_seconds: int = 43200,
                 plot: bool = False,
                 file_path: str = None,
                 critic: bool = True,
                 critic_prob: float = 0.9,
                 #critic_meth: str = 'supervised_param_imp',
                 critic_top_n: int = 5,
                 critic_mutate_top_n: bool = True,
                 critic_burn_in_gen: int = -1,
                 multi_threading: bool = False,
                 multi_processing: bool = False,
                 log: bool = False,
                 verbose: int = 0,
                 feature_engineer=None,
                 **kwargs
                 ):
        """
        :param mode: str
            Optimization specification
                -> model: Optimize model or parameter set
                -> feature: Optimize feature set

        :param df: pd.DataFrame
            Data set

        :param target: str
            Name of the target feature

        :param features: List[str]
            Name of the features used as predictors

        :param re_split_data: bool
            Whether to re-split data set into train & test data every generation or not

        :param re_sample_cases: bool
            Whether to re-sample cases set every generation or not

        :param re_sample_features: bool
            Whether to re-sample features set every generation or not

        :param max_features: int
            Number of feature attributes of each individual (if re_sample_features == True or mode != "model")

        :param feature_engineer: object
            FeatureEngineer object for generating features

        :param models: dict
            Machine learning model objects

        :param model_params: dict
            Pre-defined machine learning model parameter config if mode == "feature"

        :param genes: dict
            Attributes of the individuals (genes)

        :param max_generations: int
            Maximum number of generations

        :param pop_size: int
            Population size of each generation

        :param mutation_rate: float
            Mutation rate

        :param parents_ratio: float
            Ratio of parents to generate

        :param warm_start: bool
            Whether to start evolution (generation 0) using standard parameter config for each model type once

        :param early_stopping: int
            Number of generations for starting early stopping condition checks

        :param convergence: bool
            Whether to check convergence conditions for early stopping or not

        :param convergence_measure: str
            Measurement to use for applying convergence conditions:
                -> min:
                -> median:
                -> max:

        :param timer_in_seconds: int
            Maximum time exceeding to interrupt algorithm

        :param plot: bool
            Whether to visualize results or not

        :param file_path: str
            File path for exporting results (model, visualization, etc.)

        :param critic: bool
            Whether to enable actor-critic-framework or not

        :parma critic_prob: float
            Probability for using critic response for mutating individuals if critic is activated

        :param critic_meth: str
            Name of the critic method to use

        :param critic_top_n: int
            Number of top parameters to select if critic_meth is "supervised_param_imp"

        :param critic_mutate_top_n: bool
            Whether to mutate top n parameters or to mutate all other parameters if critic_meth is "supervised_param_imp"
            breeding several machine learning models

        :param critic_burn_in_gen: int
            Number of burn-in generations (exploration phase) for start criticizing (exploitation phase)

        :param multi_threading: bool
            Whether to run genetic algorithm using multiple threads (of one cpu core) or single thread

        :param multi_processing: bool
            Whether to run genetic algorithm using multiple processes (cpu cores) or single cpu core

        :param log: bool
            Write logging file or just print messages

        :param verbose: int
            Logging level:
                -> 0: Log basic info only
                -> 1: Log all info including algorithm results

        :param kwargs: dict
            Key-word arguments
        """
        self.log: bool = log
        self.verbose: int = verbose
        self.warm_start: bool = warm_start
        self.df: pd.DataFrame = df
        self.pop_size: int = pop_size if pop_size > 3 else 64
        self.max_generations: int = max_generations if max_generations >= 0 else 50
        self.parents_ratio: float = parents_ratio if (parents_ratio > 0) and (parents_ratio < 1) else 0.5
        self.burn_in_generations: int = burn_in_generations if burn_in_generations >= 0 else round(0.1 * self.max_generations)
        self.population: List[object] = []
        self.mutation_rate: float = mutation_rate if mutation_rate <= 0 or mutation_rate >= 1 else 0.1
        self.mutation_prob: float = mutation_prob if mutation_prob < 0 or mutation_prob >= 1 else 0.15
        if target not in self.df.keys():
            raise ActorException('Target feature ({]) not found in data set'.format(target))
        self.target: str = target
        _target_values: np.array = self.df[self.target].unique()
        self.target_classes: int = len(_target_values)
        self.target_labels: List[str] = labels
        self.target_type: str = EasyMLUtils().get_ml_type(values=_target_values)
        self.model = None
        self.models: List[str] = models
        self.evolved_model = None
        self.model_params: dict = model_params
        self.max_features: int = max_features
        self.re_split_data: bool = re_split_data
        self.re_sample_cases: bool = re_sample_cases
        self.re_sample_features: bool = re_sample_features
        if file_path is None:
            self.file_path: str = ''
        else:
            self.file_path: str = file_path.replace('\\', '/')
            if self.file_path[len(self.file_path) - 1] != '/':
                self.file_path = '{}/'.format(self.file_path)
        if features is None:
            self.features: List[str] = list(df.keys())
        else:
            if len(features) == 0:
                self.features: List[str] = list(df.keys())
            else:
                self.features: List[str] = features
        if self.target in self.features:
            self.features.remove(self.target)
        self.feature_engineer = feature_engineer
        if mode in ['feature_engineer', 'feature_selector', 'model']:
            self.mode = mode
            if self.mode.find('feature') >= 0:
                self.data_set: dict = {}
                if self.mode == 'feature_engineer':
                    if self.feature_engineer is None:
                        raise ActorException('FeatureEngineer object not found')
                    else:
                        if pop_size <= 3:
                            self.pop_size = round(len(self.feature_engineer.get_predictors()) * self.max_features)
                        self.critic_meth: str = 'supervised_feature_mutation'
                        self.critic_top_n: int = critic_top_n if critic_top_n > 0 else 3
                        self.feature_pairs: list = [random.sample(self.feature_engineer.get_predictors(), self.max_features) for _ in range(0, self.pop_size, 1)]
                elif self.mode == 'feature_selector':
                    self.critic_meth: str = 'supervised_feature_imp'
                    self.feature_pairs: list = [random.sample(self.features, self.max_features) for _ in range(0, self.pop_size, 1)]
            else:
                self.feature_pairs = None
                self.critic_meth: str = 'supervised_param_imp'
                self.critic_top_n: int = critic_top_n if critic_top_n > 0 else 5
                _stratify: bool = False if kwargs.get('stratification') is None else kwargs.get('stratification')
                if self.re_sample_features:
                    _features: List[str] = random.sample(self.features, self.max_features)
                else:
                    _features: List[str] = self.features
                self.data_set: dict = MLSampler(df=self.df,
                                                target=self.target,
                                                features=_features,
                                                train_size=0.8 if kwargs.get('train_size') is None else kwargs.get('train_size'),
                                                stratification=_stratify if self.target_type.find('clf') >= 0 else False
                                                ).train_test_sampling()
        else:
            raise ActorException('Optimization mode ({}) not supported. Use "model", "feature_engineer" or "feature_selector" instead.'.format(mode))
        if (self.pop_size * self.parents_ratio) % 2 != 1:
            if self.parents_ratio == 0.5:
                self.pop_size += 1
            else:
                self.parents_ratio = 0.5
                if (self.pop_size * self.parents_ratio) % 2 != 1:
                    self.pop_size += 1
        self.use_critic: bool = critic
        self.critic = None
        self.critic_prob: float = critic_prob if (critic_prob >= 0) and (critic_prob <= 1) else 0.9
        self.critic_mutate_top_n: bool = critic_mutate_top_n
        self.critic_burn_in: int = critic_burn_in_gen if critic_burn_in_gen > 1 else round(0.8 * self.max_generations)
        if self.max_generations <= self.critic_burn_in:
            self.use_critic = False
            Log(write=self.log, logger_file_path=self.file_path).log('Critic burn in generations are greather than maximum of generations. Therefore critic is deactivated.')
        self.plot: bool = plot
        self.n_threads: int = self.pop_size
        self.multi_threading: bool = multi_threading
        self.multi_processing: bool = multi_processing
        self.kwargs: dict = kwargs
        self.n_individuals: int = -1
        self.child_idx: List[int] = []
        self.parents_idx: List[int] = []
        self.evolved_features: List[str] = []
        self.mutated_features: dict = dict(parent=[], child=[], fitness=[], generation=[], action=[])
        self.current_generation_meta_data: dict = dict(generation=0, fitness=[], trained_model=[])
        self.generation_history: dict = dict(population={}, inheritance={})
        self.evolution_history: dict = dict(id=[],
                                            model=[],
                                            generation=[],
                                            parent=[],
                                            mutation_type=[],
                                            fitness_score=[],
                                            ml_metric=[],
                                            train_test_diff=[],
                                            train_time_in_seconds=[],
                                            cpu_usage=[],
                                            ram_usage=[],
                                            original_ml_train_metric=[],
                                            original_ml_test_metric=[]
                                            )
        self.evolution_gradient: dict = dict(min=[], median=[], mean=[], max=[])
        self.convergence: bool = convergence
        self.convergence_measure: str = convergence_measure
        self.early_stopping: int = early_stopping if early_stopping >= 0 else 0
        self.timer: int = timer_in_seconds if timer_in_seconds > 0 else 99999
        self.start_time: datetime = datetime.now()

    def _collect_meta_data(self, current_gen: bool, idx: int = None):
        """
        Collect evolution meta data

        :param current_gen: bool
            Whether to write evolution meta data of each individual of current generation or not

        :param idx: int
            Index number of individual within population
        """
        if self.generation_history['population'].get('gen_{}'.format(self.current_generation_meta_data['generation'])) is None:
            self.generation_history['population'].update(
                {'gen_{}'.format(self.current_generation_meta_data['generation']): dict(id=[],
                                                                                        model=[],
                                                                                        parent=[],
                                                                                        fitness=[]
                                                                                        )
                 })
        if current_gen:
            if self.current_generation_meta_data['generation'] == 0:
                self.current_generation_meta_data.get('trained_model').append(self.population[idx].model)
                self.current_generation_meta_data.get('fitness').append(self.evolution_history.get('fitness_score')[-1])
            else:
                self.current_generation_meta_data.get('trained_model')[idx] = self.population[idx].model
                self.current_generation_meta_data.get('fitness')[idx] = self.evolution_history.get('fitness_score')[-1]
            setattr(self.population[idx], 'features', list(self.data_set.get('x_train').keys()))
            if self.mode == 'model':
                self.critic.collect_model_training_data(model_name=self.population[idx].model_name,
                                                        parameter=self.population[idx].model_param,
                                                        fitness_score=self.evolution_history.get('fitness_score')[-1]
                                                        )
            elif self.mode == 'feature_engineer':
                if self.current_generation_meta_data['generation'] > 0:
                    self.critic.collect_action_training_data(action=self.mutated_features['action'][-1],
                                                             fitness_score=self.evolution_history.get('fitness_score')[-1]
                                                             )
            elif self.mode == 'feature_selector':
                self.critic.collect_feature_training_data(child_features=list(set(pair for pair in self.feature_pairs[self.child_idx])),
                                                          parent_features=list(set(pair for pair in self.feature_pairs[self.parents_idx]))
                                                          )
        else:
            if idx is None:
                self.generation_history['population']['gen_{}'.format(self.current_generation_meta_data['generation'])]['fitness'] = self.current_generation_meta_data.get('fitness')
                try:
                    self.evolution_gradient.get('min').append(min(self.current_generation_meta_data.get('fitness')))
                    self.evolution_gradient.get('median').append(np.median(self.current_generation_meta_data.get('fitness')))
                    self.evolution_gradient.get('mean').append(np.mean(self.current_generation_meta_data.get('fitness')))
                    self.evolution_gradient.get('max').append(max(self.current_generation_meta_data.get('fitness')))
                    Log(write=self.log, logger_file_path=self.file_path).log(
                        'Fitness: Max -> {}'.format(self.evolution_gradient.get('max')[-1]))
                    Log(write=self.log, logger_file_path=self.file_path).log(
                        'Fitness: Median -> {}'.format(self.evolution_gradient.get('median')[-1]))
                    Log(write=self.log, logger_file_path=self.file_path).log(
                        'Fitness: Mean -> {}'.format(self.evolution_gradient.get('mean')[-1]))
                    Log(write=self.log, logger_file_path=self.file_path).log(
                        'Fitness: Min -> {}'.format(self.evolution_gradient.get('min')[-1]))
                except (IndexError, ValueError):
                    pass
            else:
                if self.current_generation_meta_data['generation'] == 0:
                    self.evolution_history.get('parent').append(-1)
                else:
                    self.evolution_history.get('parent').append(self.population[idx].id)
                self.generation_history['population']['gen_{}'.format(self.current_generation_meta_data['generation'])][
                    'parent'].append(self.evolution_history.get('parent')[-1])
                self.n_individuals += 1
                setattr(self.population[idx], 'id', self.n_individuals)
                setattr(self.population[idx], 'target', self.target)
                self.evolution_history.get('id').append(self.population[idx].id)
                self.evolution_history.get('generation').append(self.current_generation_meta_data['generation'])
                self.evolution_history.get('model').append(self.population[idx].model_name)
                self.evolution_history.get('mutation_type').append(self.population[idx].model_param_mutation)
                self.generation_history['population']['gen_{}'.format(self.current_generation_meta_data['generation'])][
                    'id'].append(self.population[idx].id)
                self.generation_history['population']['gen_{}'.format(self.current_generation_meta_data['generation'])][
                    'model'].append(self.population[idx].model_name)

    def _crossover(self, parent: int, child: int):
        """
        Mutate individuals after mixing the individual genes using cross-over method

        :param parent: int
            Index number of parent in population

        :param child: int
            Index number of child in population
        """
        _inherit_genes: List[str] = copy.deepcopy(self.feature_pairs[parent])
        _x: int = 0
        for x in range(0, round(len(self.feature_pairs[parent]) * self.parents_ratio), 1):
            #print('parent', self.feature_pairs[parent])
            #print('old child', self.feature_pairs[child])
            _new_pair: List[str] = copy.deepcopy(self.feature_pairs[child])
            while True:
                _gene: str = np.random.choice(_inherit_genes)
                if _gene not in self.feature_pairs[child] or _x == 20:
                    _x = 0
                    _new_pair[x] = copy.deepcopy(_gene)
                    break
                else:
                    _x += 1
            self.feature_pairs[child] = copy.deepcopy(_new_pair)
            #print('new child', self.feature_pairs[child])

    def _is_gradient_converged(self, compare: str = 'min', threshold: float = 0.05) -> bool:
        """
        Check whether evolutionary gradient has converged into optimum

        :param compare: str
            Measurement to compare maximum fitness score with:
                -> min: Compare maximum and minimum fitness score of generation
                -> median: Compare maximum and median fitness score of generation
                -> mean: Compare maximum and mean fitness score of generation

        :param threshold: float
            Conversion threshold of relative difference between maximum fitness score and comparison fitness score

        :return bool
            Whether to stop evolution because the hole generation achieve very similar gradient score or not
        """
        _threshold: float = threshold if threshold > 0 else 0.05
        _threshold_score: float = self.evolution_gradient.get('max')[-1] - (self.evolution_gradient.get('max')[-1] * _threshold)
        if compare == 'median':
            if self.evolution_gradient.get('median')[-1] >= _threshold_score:
                return True
            else:
                return False
        elif compare == 'mean':
            if self.evolution_gradient.get('mean')[-1] >= _threshold_score:
                return True
            else:
                return False
        else:
            if self.evolution_gradient.get('min')[-1] >= _threshold_score:
                return True
            else:
                return False

    def _is_gradient_stagnating(self,
                                min_fitness: bool = True,
                                median_fitness: bool = True,
                                mean_fitness: bool = True,
                                max_fitness: bool = True
                                ) -> bool:
        """
        Check whether evolutional gradient (best fitness metric of generation) has not increased a certain amount of generations

        :param min_fitness: bool
            Use minimum fitness score each generation to evaluate stagnation

        :param median_fitness: bool
            Use median fitness score each generation to evaluate stagnation

        :param mean_fitness: bool
            Use mean fitness score each generation to evaluate stagnation

        :param max_fitness: bool
            Use maximum fitness score each generation to evaluate stagnation

        :return bool
            Whether to stop evolution early because of the stagnation of gradient or not
        """
        _gradients: int = 0
        _stagnating: int = 0
        if min_fitness:
            _gradients += 1
            _stagnating = int(len(self.evolution_gradient.get('min')) - np.array(self.evolution_gradient.get('min')).argmax() >= self.early_stopping)
        if median_fitness:
            _gradients += 1
            _stagnating = int(len(self.evolution_gradient.get('median')) - np.array(self.evolution_gradient.get('median')).argmax() >= self.early_stopping)
        if mean_fitness:
            _gradients += 1
            _stagnating = int(len(self.evolution_gradient.get('mean')) - np.array(self.evolution_gradient.get('mean')).argmax() >= self.early_stopping)
        if max_fitness:
            _gradients += 1
            _stagnating = int(len(self.evolution_gradient.get('max')) - np.array(self.evolution_gradient.get('max')).argmax() >= self.early_stopping)
        if _gradients == _stagnating:
            return True
        else:
            return False

    def _fitness(self, individual: object, ml_metric: str):
        """
        Calculate fitness metric for evaluate individual ability to survive

        :param individual: object
            Object of individual to evaluating fitness metric

        :param ml_metric: str
            Name of the machine learning metric
                -> Unknown - profit: Profit by given probability and quota
                -> Regression - rmse_norm: Root-Mean-Squared Error normalized by standard deviation
                -> Classification Binary - auc: Area-Under-Curve (AUC)
                                           f1: F1-Score
                                           recall: Recall
                                           accuracy: Accuracy
                -> Classification Multi - auc: Area-Under-Curve (AUC) multi classes summarized
                                          auc_multi: Area-Under-Curve (AUC) multi classes separately
        """
        if ml_metric == 'profit':
            pass
        else:
            _best_score: float = 0.0 if ml_metric == 'rmse_norm' else 1.0
            _ml_metric: str = 'roc_auc' if ml_metric == 'auc' else ml_metric
            _scores: dict = productivity(ml_metric=tuple([_best_score, individual.fitness['test'].get(_ml_metric)]),
                                         train_test_metric=tuple([individual.fitness['train'].get(_ml_metric), individual.fitness['test'].get(_ml_metric)]),
                                         train_time_in_seconds=individual.train_time,
                                         cpu_usage_in_percent=individual.cpu_usage,
                                         ram_usage_in_percent=individual.ram_usage
                                         )
        for score in _scores.keys():
            self.evolution_history.get(score).append(_scores.get(score))

    def _inherit(self) -> List[tuple]:
        """
        Inheritance from one parent to one child

        :return List[tuple]
            Selected combination of parent id and child id of population
        """
        _parent_child_combination: List[tuple] = []
        _min_matching_length: int = len(self.parents_idx) if len(self.parents_idx) <= len(self.child_idx) else len(self.child_idx)
        for c in range(0, _min_matching_length, 1):
            _parent_child_combination.append(tuple([self.parents_idx[c], self.child_idx[c]]))
        return _parent_child_combination

    def _mating_pool(self):
        """
        Selecting best individuals in the current generation as parents for reducing the offspring of the next generation
        """
        if self.re_split_data or self.re_sample_cases or self.re_sample_features:
            _features: List[str] = self.features
            if self.re_sample_features:
                _features: List[str] = random.sample(self.features, self.max_features)
            self.data_set = MLSampler(df=self.df,
                                      target=self.target,
                                      features=_features,
                                      train_size=0.8 if self.kwargs.get('train_size') is None else self.kwargs.get('train_size'),
                                      random=True if self.kwargs.get('random') is None else self.kwargs.get('random'),
                                      stratification=False if self.kwargs.get('stratification') is None else self.kwargs.get('stratification')
                                      ).train_test_sampling(validation_split=0.1 if self.kwargs.get('validation_split') is None else self.kwargs.get('validation_split'))
        _threads: dict = {}
        _thread_pool: ThreadPool = ThreadPool(processes=self.n_threads) if self.multi_threading else None
        for i in range(0, self.pop_size, 1):
            if i not in self.parents_idx:
                if self.multi_threading:
                    _threads.update({i: _thread_pool.apply_async(func=self._modeling, args=[i])})
                else:
                    self._modeling(pop_idx=i)
        if self.multi_threading:
            for thread in _threads.keys():
                _threads.get(thread).get()
        self._collect_meta_data(current_gen=False, idx=None)

    def _modeling(self, pop_idx: int):
        """
        Generate, train and evaluate supervised machine learning model

        :param pop_idx: int
            Population index number
        """
        self._collect_meta_data(current_gen=False, idx=pop_idx)
        _re: int = 0
        _re_generate: bool = False
        _re_generate_max: int = 50
        while True:
            _re += 1
            try:
                if self.mode == 'model':
                    if _re_generate:
                        if np.random.uniform(low=0, high=1) <= self.mutation_prob:
                            self.population[pop_idx] = self.population[pop_idx].generate_model()
                        else:
                            self.population[pop_idx] = self.population[pop_idx].generate_params(param_rate=self.mutation_rate)
                elif self.mode == 'feature_engineer':
                    if self.current_generation_meta_data['generation'] > 0:
                        self.data_set = MLSampler(df=self.feature_engineer.get_data(),
                                                  target=self.target,
                                                  features=self.feature_pairs[pop_idx],
                                                  train_size=0.8 if self.kwargs.get('train_size') is None else self.kwargs.get('train_size'),
                                                  random=True if self.kwargs.get('random') is None else self.kwargs.get('random'),
                                                  stratification=False if self.kwargs.get('stratification') is None else self.kwargs.get('stratification')
                                                  ).train_test_sampling(validation_split=0.1 if self.kwargs.get('validation_split') is None else self.kwargs.get('validation_split'))
                self.population[pop_idx].train(x=copy.deepcopy(self.data_set.get('x_train').values),
                                               y=copy.deepcopy(self.data_set.get('y_train').values),
                                               validation=dict(x_val=copy.deepcopy(self.data_set.get('x_val').values),
                                                               y_val=copy.deepcopy(self.data_set.get('y_val').values)
                                                               )
                                               )
                _re = 0
                break
            except Exception as e:
                if _re == _re_generate_max:
                    break
                else:
                    _re_generate = True
                    Log(write=self.log, logger_file_path=self.file_path).log(msg='Error while training model ({})\n{}'.format(self.population[pop_idx].model_name, e))
        if _re == _re_generate_max:
            raise ActorException('Maximum number of errors occurred. Check last error message ...')
        if self.target_type == 'reg':
            _pred: np.array = self.population[pop_idx].predict(x=self.data_set.get('x_test').values)
            self.population[pop_idx].eval(obs=self.data_set.get('y_test').values, pred=_pred, eval_metric=None)
            self._fitness(individual=self.population[pop_idx], ml_metric='rmse_norm')
        else:
            _pred: np.array = self.population[pop_idx].predict(x=self.data_set.get('x_test').values, probability=True)
            self.population[pop_idx].eval(obs=self.data_set.get('y_test').values, pred=_pred, eval_metric=None)
            if self.target_type == 'clf_multi':
                self._fitness(individual=self.population[pop_idx], ml_metric='f1')
            else:
                self._fitness(individual=self.population[pop_idx], ml_metric='auc')
        self._collect_meta_data(current_gen=True, idx=pop_idx)

    def _mutate(self, parent: int, child: int, force_param: dict = None):
        """
        Mutate individual

        :param parent: int
            Index number of parent in population

        :param child: int
            Index number of child in population

        :param force_param: dict
            Model parameter config to force during mutation
        """
        if self.mode == 'model':
            if np.random.uniform(low=0, high=1) <= self.mutation_prob:
                self.population[child] = self.population[parent].generate_model()
            else:
                self.population[child] = self.population[parent].generate_params(param_rate=self.mutation_rate, force_param=force_param)
        elif self.mode.find('feature') >= 0:
            _new_features: List[str] = []
            _feature_pool: List[str] = self.feature_pairs[np.random.choice(a=self.parents_idx)]
            for feature in self.feature_pairs[child]:
                if feature in self.feature_pairs[parent]:
                    if self.mode == 'feature_engineer':
                        if np.random.uniform(low=0, high=1) <= self.mutation_prob:
                            if self.use_critic and (self.critic_burn_in <= self.current_generation_meta_data['generation']):
                                self.feature_engineer.act(actor=feature,
                                                          inter_actors=_feature_pool,
                                                          force_action=self.critic.criticize_engineer(),
                                                          alternative_actions=self.critic.imp_action
                                                          )
                            else:
                                self.feature_engineer.act(actor=feature,
                                                          inter_actors=_feature_pool,
                                                          force_action=None,
                                                          alternative_actions=None
                                                          )
                            _new_features.append(self.feature_engineer.get_last_generated_feature())
                            self.mutated_features['parent'].append(feature)
                            self.mutated_features['child'].append(_new_features[-1])
                            self.mutated_features['generation'].append(feature)
                            self.mutated_features['action'].append(self.feature_engineer.get_last_action())
                        else:
                            _new_features.append(feature)
                    elif self.mode == 'feature_selector':
                        _new_features.append(feature)
                else:
                    _new_features.append(feature)
            self.feature_pairs[child] = copy.deepcopy(_new_features)
            print('mutated new child', self.feature_pairs[child])

    def _mutation(self, crossover: bool = False):
        """
        Mutate genes of chosen parents

        :param crossover: bool
            Allow individuals to include crossover before mutating single genes as additional mutation strategy
        """
        for parent, child in self._inherit():
            if crossover:
                # Mutation including crossover strategy (used for optimizing feature engineering and selection)
                if self.use_critic and (self.critic_burn_in <= self.current_generation_meta_data['generation']) and self.mode == 'supervised_feature_imp':
                    if np.random.uniform(low=0.0, high=1.0) >= self.critic_prob:
                        self.feature_pairs[child] = self.critic.criticize_selector(child_features=self.feature_pairs[child],
                                                                                   parent_features=self.feature_pairs[parent],
                                                                                   mutataion_rate=self.mutation_rate
                                                                                   )
                    else:
                        self._crossover(parent=parent, child=child)
                        self._mutate(parent=parent, child=child)
                else:
                    self._crossover(parent=parent, child=child)
                    self._mutate(parent=parent, child=child)
            else:
                # Mutation without crossover strategy (used for optimizing ml models / parameters)
                self._mutate(parent=parent, child=child)
                if self.use_critic:
                    if self.critic_burn_in <= self.current_generation_meta_data['generation']:
                        if np.random.uniform(low=0.0, high=1.0) >= self.critic_prob:
                            _max_critics: int = 50
                            _c: int = 0
                            while True:
                                _c += 1
                                if _c > _max_critics:
                                    break
                                if self.critic_meth == 'supervised_param_imp':
                                    if self.models is not None and len(self.models) == 1:
                                        # Run critic for selecting the best fitting model parameters:
                                        self._mutate(parent=parent,
                                                     child=child,
                                                     force_param=self.critic.criticize_param(model_name=self.population[child].model_name,
                                                                                             model_param=self.population[child].model_param,
                                                                                             mutate_top_n=self.critic_mutate_top_n
                                                                                             )
                                                     )
                                        break
                                    else:
                                        # Run critic for selecting the best fitting models:
                                        if self.critic.accept_model(model_name=self.population[child].model_name):
                                            break
                                        else:
                                            #Log(write=self.log).log('Critic has not accepted chosen model {}'.format(self.population[child].model_name))
                                            self._mutate(parent=parent, child=child)
                                else:
                                    break

    def _natural_selection(self):
        """
        Select best individuals of population as parents for next generation
        """
        # Calculate number of parents within generation:
        _count_parents: int = int(self.pop_size * self.parents_ratio)
        # Rank parents according to their fitness score
        _sorted_fitness_matrix: pd.DataFrame = pd.DataFrame(data=dict(fitness=self.current_generation_meta_data.get('fitness'))).sort_values(by='fitness', axis=0, ascending=False)
        self.parents_idx = _sorted_fitness_matrix[0:_count_parents].index.values.tolist()
        self.child_idx = _sorted_fitness_matrix[_count_parents:].index.values.tolist()

    def _populate(self):
        """
        Populate generation zero with individuals
        """
        for p in range(0, self.pop_size, 1):
            if self.mode.find('feature') >= 0:
                self.data_set = MLSampler(df=self.feature_engineer.get_data(),
                                          target=self.target,
                                          features=self.feature_pairs[p],
                                          train_size=0.8 if self.kwargs.get('train_size') is None else self.kwargs.get('train_size'),
                                          random=True if self.kwargs.get('random') is None else self.kwargs.get('random'),
                                          stratification=False if self.kwargs.get('stratification') is None else self.kwargs.get('stratification')
                                          ).train_test_sampling(validation_split=0.1 if self.kwargs.get('validation_split') is None else self.kwargs.get('validation_split'))
            if self.target_type == 'reg':
                self.population.append(ModelGeneratorReg(n_cases=self.data_set.get('x_train').shape[0],
                                                         n_features=self.data_set.get('x_train').shape[1],
                                                         reg_params=self.model_params,
                                                         models=self.models
                                                         ).generate_model())
            else:
                self.population.append(ModelGeneratorClf(n_cases=self.data_set.get('x_train').shape[0],
                                                         n_features=self.data_set.get('x_train').shape[1],
                                                         clf_params=self.model_params,
                                                         models=self.models
                                                         ).generate_model())

    def _save_locally(self):
        """
        Save evolution history data generated by genetic algorithm
        """
        # Export evolution history data:
        #DataExporter(obj=self.evolution_history, file_path=os.path.join(self.file_path, 'evolution_history.p'), create_dir=True, overwrite=False).file()
        # Export generation history data:
        #DataExporter(obj=self.generation_history, file_path=os.path.join(self.file_path, 'generation_history.p'), create_dir=True, overwrite=False).file()
        # Export evolved model:
        DataExporter(obj=self.evolved_model, file_path=os.path.join(self.file_path, 'model.p'), create_dir=True, overwrite=False).file()
        # Export training data for supervised critic:
        #DataExporter(obj=self.critic, file_path=os.path.join(self.file_path, 'critic_train_data.p'), create_dir=True, overwrite=False).file()

    def _visualize(self,
                   results_table: bool = True,
                   model_distribution: bool = False,
                   model_evolution: bool = True,
                   param_distribution: bool = False,
                   train_time_distribution: bool = True,
                   technical_usage: bool = True,
                   breeding_map: bool = False,
                   breeding_graph: bool = False,
                   fitness_distribution: bool = True,
                   fitness_evolution: bool = True,
                   fitness_dimensions: bool = True,
                   per_generation: bool = True,
                   prediction_of_best_model: bool = True
                   ):
        """
        Visualize evolutionary activity

        :param model_evolution: bool
            Evolution of individuals
                -> Scatter Chart

        :param model_distribution: bool
            Distribution of used model types
                -> Bar Chart / Pie Chart

        :param param_distribution: bool
            Distribution of used model parameter combination
                -> Tree Map / Sunburst

        :param train_time_distribution: bool
            Distribution of training time
                -> Violin

        :param technical_usage: bool
            Distribution of CPU and RAM usage
                -> Histogram

        :param breeding_map: bool
            Breeding evolution as
                -> Heat Map
                -> Network Chart

        :param fitness_distribution: bool
            Distribution of fitness metric
                -> Ridge Line Chart

        :param fitness_evolution: bool
            Evolution of fitness metric
                -> Line Chart

        :param fitness_dimensions: bool
            Calculated loss value for each dimension in fitness metric
                -> Radar Chart
                -> Tree Map

        :param per_generation: bool
            Visualize results of each generation in detail or visualize just evolutionary results

        :param prediction_of_best_model: bool
            Evaluation of prediction of the fittest model of evolution
                -> Parallel Coordinate Chart
                -> Joint Chart
        """
        _charts: dict = {}
        _evolution_history_data: pd.DataFrame = pd.DataFrame(data=self.evolution_history)
        _m: List[str] = ['fitness_score', 'ml_metric', 'train_test_diff', 'cpu_usage', 'ram_usage']
        _evolution_history_data[_m] = _evolution_history_data[_m].round(decimals=2)
        _evolution_gradient_data: pd.DataFrame = pd.DataFrame(data=self.evolution_gradient)
        _evolution_gradient_data['generation'] = [i for i in range(0, len(self.evolution_gradient.get('max')), 1)]
        _best_model_results: pd.DataFrame = pd.DataFrame(data=dict(obs=self.selected_model.get('obs'),
                                                                   pred=self.selected_model.get('pred')
                                                                   )
                                                         )
        _best_model_results['abs_diff'] = _best_model_results['obs'] - _best_model_results['pred']
        _best_model_results['rel_diff'] = _best_model_results['obs'] / _best_model_results['pred']
        _best_model_results = _best_model_results.round(decimals=4)
        if results_table:
            _charts.update({'Results of Genetric Algorithm:': dict(data=_evolution_history_data,
                                                                   plot_type='table',
                                                                   file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_metadata_table.html')
                                                                   )
                            })
        if model_evolution:
            _charts.update({'Evolution of used ML Models:': dict(data=_evolution_history_data,
                                                                 features=['fitness_score', 'generation'],
                                                                 color_feature='model',
                                                                 plot_type='scatter',
                                                                 melt=True,
                                                                 file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_model_evolution.html')
                                                                 )
                            })
        if model_distribution:
            if len(self.models) > 1:
                _charts.update({'Distribution of used ML Models:': dict(data=_evolution_history_data,
                                                                        features=['model'],
                                                                        group_by=['generation'] if per_generation else None,
                                                                        plot_type='pie',
                                                                        file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_model_distribution.html')
                                                                        )
                                })
        if param_distribution:
            _charts.update({'Distribution of ML Model parameters:': dict(data=_evolution_history_data,
                                                                         features=['model_param'],
                                                                         group_by=['generation'] if per_generation else None,
                                                                         plot_type='tree',
                                                                         file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_parameter_treemap.html')
                                                                         )
                            })
        if train_time_distribution:
            _charts.update({'Distribution of elapsed Training Time:': dict(data=_evolution_history_data,
                                                                           features=['train_time_in_seconds'],
                                                                           group_by=['model'],
                                                                           plot_type='violin',
                                                                           melt=True,
                                                                           file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_training_time_distribution.html')
                                                                           )
                            })
        if technical_usage:
            _charts.update({'Distribution of CPU & RAM usage:': dict(data=_evolution_history_data,
                                                                     features=['ram_usage', 'cpu_usage'],
                                                                     group_by=['model'],
                                                                     plot_type='violin',
                                                                     melt=True,
                                                                     file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_cpu_ram_distribution.html')
                                                                     )
                            })
        if breeding_map:
            _breeding_map: pd.DataFrame = pd.DataFrame(data=dict(gen_0=self.generation_history['population']['gen_0'].get('fitness')))
            for g in self.generation_history['population'].keys():
                if g != 'gen_0':
                    _breeding_map[g] = self.generation_history['population'][g].get('fitness')
            _charts.update({'Breeding Heat Map:': dict(data=_breeding_map,
                                                       plot_type='heat',
                                                       file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_breeding_heatmap.html')
                                                       )
                            })
        if breeding_graph:
            _charts.update({'Breeding Network Graph:': dict(data=_evolution_history_data,
                                                            features=['generation', 'fitness_score'],
                                                            graph_features=dict(node='id', edge='parent'),
                                                            color_feature='model',
                                                            plot_type='network',
                                                            file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_breeding_graph.html')
                                                            )
                            })
        if fitness_distribution:
            _charts.update({'Distribution of Fitness Metric:': dict(data=_evolution_history_data,
                                                                    features=['fitness_score'],
                                                                    time_features=['generation'],
                                                                    plot_type='ridgeline',
                                                                    file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_fitness_score_distribution_per_generation.html')
                                                                    )
                            })
        if fitness_dimensions:
            _charts.update({'Evolution Meta Data:': dict(data=_evolution_history_data,
                                                         features=['train_time_in_seconds',
                                                                   'cpu_usage',
                                                                   'ram_usage',
                                                                   'ml_metric',
                                                                   'train_test_diff',
                                                                   'fitness_score',
                                                                   'parent',
                                                                   'id',
                                                                   'generation',
                                                                   'model'
                                                                   ],
                                                         color_feature='model',
                                                         plot_type='parcoords',
                                                         file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_metadata_evolution_coords_actor_only.html')
                                                         )
                            })
        if fitness_evolution:
            _charts.update({'Fitness Evolution:': dict(data=_evolution_gradient_data,
                                                       features=['min', 'median', 'mean', 'max'],
                                                       time_features=['generation'],
                                                       plot_type='line',
                                                       file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_evolution_fitness_score.html')
                                                       )
                            })
        if prediction_of_best_model:
            if self.target_type == 'reg':
                _charts.update({'Prediction Evaluation of final inherited ML Model:': dict(data=_best_model_results,
                                                                                           features=['obs', 'abs_diff', 'rel_diff', 'pred'],
                                                                                           color_feature='pred',
                                                                                           plot_type='parcoords',
                                                                                           file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_prediction_evaluation_coords.html')
                                                                                           ),
                                'Prediction vs. Observation of final inherited ML Model:': dict(data=_best_model_results,
                                                                                                features=['obs', 'pred'],
                                                                                                plot_type='joint',
                                                                                                file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_prediction_scatter_contour.html')
                                                                                                )
                                })
            elif self.target_type == 'clf_binary':
                _prob: List[str] = []
                #for c in range(0, self.selected_model.get('prob').shape[1], 1):
                #    _prob.append('prob_{}'.format(c))
                #    _best_model_results[_prob[-1]] = [prob[c] for prob in self.selected_model.get('prob')]
                _prob.extend(['obs', 'pred'])
                _charts.update({'Prediction Evaluation of final inherited ML Model:': dict(data=_best_model_results,
                                                                                           features=_prob,
                                                                                           color_feature='pred',
                                                                                           plot_type='parcoords',
                                                                                           brushing=True,
                                                                                           file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_prediction_evaluation_category.html')
                                                                                           )
                                })
                _charts.update({'Prediction vs. Observation of final inherited ML Model:': dict(data=_best_model_results,
                                                                                                features=['obs', 'pred'],
                                                                                                color_feature='pred',
                                                                                                plot_type='heat',
                                                                                                file_path=self.file_path if self.file_path is None else '{}{}'.format(self.file_path, 'ga_prediction_confusion_heatmap.html')
                                                                                                )
                                })
            elif self.target_type == 'clf_multi':
                pass
        if len(_charts.keys()) > 0:
            DataVisualizer(subplots=_charts,
                           interactive=True,
                           file_path=self.file_path,
                           render=True if self.file_path is None else False,
                           height=750,
                           width=750,
                           unit='px'
                           ).run()

    def optimize(self):
        """
        Optimize attribute configuration of supervised machine learning models in order to select best model, parameter set or feature set
        """
        self.critic = Critic(ml_type=self.target_type,
                             critic=self.critic_meth,
                             path=self.file_path,
                             feature_engineer=self.feature_engineer
                             )
        if self.use_critic:
            Log(write=self.log, logger_file_path=self.file_path).log('Actor-Critic framework activated')
        self.current_generation_meta_data['generation'] = 0
        _evolve: bool = True
        _stopping_reason: str = ''
        self._populate()
        while _evolve:
            Log(write=self.log, logger_file_path=self.file_path).log('Generation: {}'.format(self.current_generation_meta_data['generation']))
            if self.current_generation_meta_data['generation'] > 0:
                self.n_threads = len(self.child_idx)
            self._mating_pool()
            self._natural_selection()
            if self.use_critic:
                if self.critic_burn_in == self.current_generation_meta_data['generation']:
                    if self.mode == 'model':
                        if self.critic_meth == 'supervised_param_imp':
                            Log(write=self.log, logger_file_path=self.file_path).log('Train Critic using Parameter Importance Evaluation ...')
                            self.critic.param_importance(models=self.models, top_n=self.critic_top_n)
                        else:
                            self.use_critic = False
                            Log(write=self.log, logger_file_path=self.file_path).log('Critic method ({}) not supported. Critic disabled'.format(self.critic_meth))
                    elif self.mode == 'feature_selector':
                        Log(write=self.log, logger_file_path=self.file_path).log('Train Critic using simple Feature Survival Scoring ...')
                    elif self.mode == 'feature_engineer':
                        Log(write=self.log, logger_file_path=self.file_path).log('Train Critic using Feature Engineering Method Importance Evaluation ...')
                        self.critic.action_importance(top_n=self.critic_top_n)
            self._mutation(crossover=False if self.mode == 'model' else True)
            if (self.mode == 'model') and (self.current_generation_meta_data['generation'] > self.burn_in_generations):
                if self.convergence:
                    if self._is_gradient_converged(compare=self.convergence_measure, threshold=0.05):
                        _evolve = False
                        _stopping_reason = 'gradient_converged'
                        Log(write=self.log).log('Fitness metric (gradient) has converged. Therefore the evolution stops at generation {}'.format(self.current_generation_meta_data.get('generation')))
                if self.early_stopping > 0:
                    if self._is_gradient_stagnating(min_fitness=True, median_fitness=True, mean_fitness=True, max_fitness=True):
                        _evolve = False
                        _stopping_reason = 'gradient_stagnating'
                        Log(write=self.log).log('Fitness metric (gradient) per generation has not increased a certain amount of generations ({}). Therefore the evolution stops early at generation {}'.format(self.early_stopping, self.current_generation_meta_data.get('generation')))
            if (datetime.now() - self.start_time).seconds >= self.timer:
                _evolve = False
                _stopping_reason = 'time_exceeded'
                Log(write=self.log).log('Time exceeded:{}'.format(self.timer))
            self.current_generation_meta_data['generation'] += 1
            if self.current_generation_meta_data['generation'] > self.max_generations:
                _evolve = False
                _stopping_reason = 'max_generation_evolved'
                Log(write=self.log).log('Maximum number of generations reached:{}'.format(self.max_generations))
        if self.mode.find('feature') >= 0:
            self._mating_pool()
            self._natural_selection()
            for parent in self.parents_idx:
                self.evolved_features.extend(self.feature_pairs[parent])
            self.evolved_features = list(set(self.evolved_features))
        _best_individual_idx: int = np.array(self.current_generation_meta_data['fitness']).argmax()
        self.model = self.population[_best_individual_idx]
        Log(write=self.log, logger_file_path=self.file_path).log(msg='Best model:{}'.format(self.model.model))
        Log(write=self.log, logger_file_path=self.file_path).log(msg='Fitness:{}'.format(self.model.fitness))
        self.evolved_model: dict = dict(trained_model=self.model.model,
                                        model_name=self.model.model_name,
                                        param=self.model.model_param,
                                        param_mutated=self.model.model_param_mutated,
                                        fitness=self.model.fitness,
                                        features=self.model.features,
                                        target=self.model.target,
                                        target_type=self.target_type,
                                        obs=self.data_set.get('y_test').values,
                                        pred=self.model.predict(self.data_set.get('x_test').values),
                                        prob=None,
                                        re_split_data=self.re_split_data,
                                        re_split_cases=self.re_split_cases,
                                        re_sample_features=self.re_sample_features,
                                        id=self.model.id,
                                        mode=self.mode,
                                        generations=self.current_generation_meta_data['generation'],
                                        parent_ratio=self.parents_ratio,
                                        mutation_prob=self.mutation_prob,
                                        mutation_rate=self.mutation_rate,
                                        mutated_features=self.mutated_features,
                                        generation_history=self.generation_history,
                                        evolution_history=self.evolution_history,
                                        evolution_gradient=self.evolution_gradient,
                                        convergence_check=self.convergence,
                                        convergence_measure=self.convergence_measure,
                                        early_stopping=self.early_stopping,
                                        max_time=self.timer,
                                        start_time=self.start_time,
                                        end_time=str(datetime.now()),
                                        stopping_reason=_stopping_reason,
                                        critic=self.use_critic,
                                        critic_burn_in=self.critic_burn_in if self.use_critic else 0,
                                        critic_meth=self.critic_meth,
                                        critic_imp_param=self.critic.imp_param,
                                        critic_imp_action=self.critic.imp_action,
                                        critic_train_data=self.critic.train_data
                                        )
        if self.plot:
            self._visualize()
        if self.file_path is not None:
            if len(self.file_path) > 0:
                self._save_locally()


class CriticException(Exception):
    """
    Class for handling exception for class Critic
    """
    pass


class Critic:
    """
    Class for building an actor-critic framework using genetic algorithm as an actor
    """
    def __init__(self, ml_type: str, critic: str = 'supervised_param_imp', path: str = None, feature_engineer=None):
        """
        :param ml_type: str
            Name of the supervised machine learning type:
                -> reg: Regression
                -> clf_multi: Classification with multi-class target values
                -> clf_binary: Classification with binary target values

        :param critic: str
            Name of the machine learning method of the critic to use
                -> supervised_param_imp: Parameter importance based on shapley scores (supervised learning)
                -> supervised_decision_tree: Decision Tree (supervised learning)
                -> supervised_feature_mutation: Mutation (feature)
                -> supervised_feature_imp: Feature importance based on the survival of the fittest concept

        :param path: str
            Path for writing meta data to store on local hard drive

        :param feature_engineer: FeatureEngineer
            FeatureEngineer object for feature based critics only
        """
        self.model = None
        self.critic: str = critic
        self.ml_type: str = ml_type
        self.fitness: dict = dict(train=0.0, test=0.0)
        self.imp_param: dict = {}
        self.imp_action: List[str] = []
        self.action_space: dict = {}
        self.parameter_space: dict = dict(clf={}, reg={})
        self.path: str = path
        self.feature_engineer = feature_engineer
        if self.critic.find('feature') >= 0:
            if self.feature_engineer is None:
                raise CriticException('No feature engineer object found')
            if self.critic == 'supervised_feature_imp':
                self.train_data: dict = {feature: 0.0 for feature in self.feature_engineer.get_predictors()}
            elif self.critic == 'supervised_feature_mutation':
                self.train_data: dict = dict(x={}, y=[])
                self._get_action_space()
        else:
            self._get_parameter_space()
            self.train_data: dict = dict(clf=dict(x={}, y=[]), reg=dict(x={}, y=[]))
            self.train_data['clf']['x'] = {clf: [] for clf in self.parameter_space.get('clf').keys()}
            self.train_data['reg']['x'] = {reg: [] for reg in self.parameter_space.get('reg').keys()}

    def _get_action_space(self):
        """
        Get action (feature engineering) space
        """
        _action_space: dict = self.feature_engineer.get_action_space()['continuous']
        for action in _action_space.keys():
            for meth in _action_space.get(action):
                self.action_space.update({action: meth})
                _action: str = meth if action == 'transformation' else '{}_{}'.format(action, meth)
                self.train_data['x'].update({_action: []})

    def _get_parameter_space(self):
        """
        Get parameter space
        """
        for clf in PARAM_SPACE_CLF.keys():
            _model_name: str = clf
            for clf_param in PARAM_SPACE_CLF.get(clf).keys():
                if isinstance(PARAM_SPACE_CLF[clf].get(clf_param), list):
                    for cat in PARAM_SPACE_CLF[clf].get(clf_param):
                        self.parameter_space['clf'].update({'{}_{}'.format(_model_name, cat): 0})
                else:
                    self.parameter_space['clf'].update({'{}_{}'.format(_model_name, clf_param): PARAM_SPACE_CLF[clf].get(clf_param)})
        for reg in PARAM_SPACE_REG.keys():
            _model_name: str = reg
            for reg_param in PARAM_SPACE_REG.get(reg).keys():
                if isinstance(PARAM_SPACE_REG[reg].get(reg_param), list):
                    for cat in PARAM_SPACE_REG[reg].get(reg_param):
                        self.parameter_space['reg'].update({'{}_{}'.format(_model_name, cat): 0})
                else:
                    self.parameter_space['reg'].update({'{}_{}'.format(_model_name, reg_param): PARAM_SPACE_REG[reg].get(reg_param)})

    def accept_model(self, model_name: str) -> bool:
        """
        Accept or reject model selection based on the model parameter meta data

        :param model_name: str
            Name of the model

        :return bool:
            Whether to approve or reject action
        """
        if model_name in self.imp_param.keys():
            return True
        return False

    def action_importance(self, top_n: int = 3):
        """
        Calculate action (feature engineering method) importance score

        :param top_n: int
            Number of top actions to extract
        """
        _meta_data: pd.DataFrame = pd.DataFrame(data=self.train_data.get('x'))
        _actions: List[str] = list(_meta_data.keys())
        _meta_data['y'] = self.train_data.get('y')
        self.imp_action.extend(FeatureSelector(df=_meta_data,
                                               target='y',
                                               features=_actions,
                                               visualize_all_scores=True,
                                               visualize_variant_scores=False,
                                               visualize_core_feature_scores=False,
                                               path=self.path,
                                               **dict(stratification=False)
                                               ).get_imp_features(meth='shapley',
                                                                  imp_threshold=0.01
                                                                  )['imp_features'][0:top_n]
                               )

    def criticize_engineer(self) -> str:
        """
        Criticize feature engineering by generating action based on the action importance scoring (Shapley)

        :return str:
            Feature engineering method
        """
        return np.random.choice(a=self.imp_action)

    def criticize_param(self, model_name: str, model_param: dict, mutate_top_n: bool = True) -> dict:
        """
        Criticize action by generating models based on the parameter importance scoring (Shapley)

        :param model_name: str
            Name of the model

        :param model_param: dict
            Model parameter config

        :param mutate_top_n: bool
            Whether to mutate parameters which are in the top n ranking or not in the top n ranking

        :return dict:
            Recommended model parameter config
        """
        _model_param: dict = {}
        _feature: str = np.random.choice(a=self.imp_param.get('imp_params'), size=1)
        _param_space: dict = PARAM_SPACE_REG if self.ml_type == 'reg' else PARAM_SPACE_CLF
        for param in _param_space.get(model_name).keys():
            if isinstance(param, list):
                for param_cat in param:
                    if param_cat in self.imp_param.get(model_name):
                        if param in _model_param.keys():
                            for feature in self.imp_param.get('imp_params'):
                                if feature == param_cat:
                                    _model_param.update({param: param_cat.split('_')[-1]})
                                elif feature == '{}_{}'.format(param, _model_param.get(param)):
                                    break
                        else:
                            _model_param.update({param: param_cat.split('_')[-1]})
            else:
                if mutate_top_n:
                    if param not in self.imp_param.get(model_name):
                        _model_param.update({param: model_param.get(param)})
                else:
                    if param in self.imp_param.get(model_name):
                        _model_param.update({param: model_param.get(param)})
        return _model_param

    def criticize_selector(self, child_features: List[str], parent_features: List[str], mutation_rate: float) -> List[str]:
        """
        Criticize action of feature selector by force cross-over inheritance based on fitness scoring

        :param child_features: List[str]
            Name of the features used in child model

        :param parent_features: List[str]
            Name of the features used in parent model

        :param mutation_rate: float
            Selection rate

        :return List[str]:
            Name of the features used in new model
        """
        _new_selection: List[str] = []
        _selection: List[str] = list(set(child_features + parent_features))
        _feature_scores: pd.DataFrame = pd.DataFrame(data=self.train_data, index=['score'])
        _feature_scores = _feature_scores[_selection].transpose()
        _feature_scores['parent'] = [1 if feature else 0 in parent_features for feature in _feature_scores.index.values]
        _feature_scores.sort_values(by='score', ascending=False, inplace=True)
        _n: int = round(len(parent_features) * mutation_rate)
        _m: int = len(parent_features) - _n
        for i, parent in enumerate(_feature_scores.loc[_feature_scores['parent'] == 1, 'score'].index.values):
            _new_selection.append(parent)
            if i + 1 == _n:
                break
        for j, child in enumerate(_feature_scores.loc[_feature_scores['parent'] == 0, 'score'].index.values):
            _new_selection.append(child)
            if j + 1 == _m:
                break
        return _new_selection

    def collect_action_training_data(self, action: str, fitness_score: float):
        """
        Collect action (feature engineering method) meta data for train supervised learning algorithm

        :param action: str
            Name of the feature engineering method

        :param fitness_score: float
            Fitness score
        """
        for feature in self.train_data['x'].keys():
            if feature == action:
                self.train_data['x'][action].append(1)
            else:
                self.train_data['x'][feature].append(0)
        self.train_data['y'].append(fitness_score)

    def collect_feature_training_data(self, child_features: List[str], parent_features: List[str]):
        """
        Collect feature meta data for survival scoring

        :param child_features: List[str]
            Name of the child features

        :param parent_features: List[str]
            Name of the parent features
        """
        for child in child_features:
            self.train_data[child] -= 10
        for parent in parent_features:
            self.train_data[parent] += 10

    def collect_model_training_data(self, model_name: str, parameter: dict, fitness_score: float):
        """
        Collect data for train supervised learning algorithm

        :param model_name: str
            Name of the model to use

        :param parameter: dict
            Parameter configuration of given model

        :param fitness_score: float
            Fitness score
        """
        _param_space: dict = PARAM_SPACE_REG if self.ml_type == 'reg' else PARAM_SPACE_CLF
        _train_data: dict = copy.deepcopy(self.parameter_space.get(self.ml_type.split('_')[0]))
        for p in parameter.keys():
            if isinstance(_param_space[model_name].get(p), list):
                if isinstance(parameter.get(p), str):
                    _train_data.update({'{}_{}_{}'.format(model_name, p, parameter.get(p)): 1})
                else:
                    for o in _param_space[model_name].get(p):
                        if hasattr(o, '__call__'):
                            if str(o.__name__) == parameter.get(p).__name__:
                                _train_data.update({'{}_{}_{}'.format(model_name, p, o.__name__): 1})
                        else:
                            if str(parameter.get(p)).find(o.replace('{}_'.format(p), '')) >= 0:
                                _train_data.update({'{}_{}'.format(model_name, o): 1})
            else:
                _train_data.update({'{}_{}'.format(model_name, p): parameter.get(p)})
        for data in _train_data.keys():
            try:
                self.train_data[self.ml_type.split('_')[0]]['x'][data].append(_train_data.get(data))
            except KeyError:
                pass
                #print('Model: ', model_name , 'Input param', parameter)
                #print('Output param', data, ' - ', _train_data.get(data))
        self.train_data[self.ml_type.split('_')[0]]['y'].append(fitness_score)

    def param_importance(self, models: List[str], top_n: int = 5):
        """
        Calculate parameter importance score

        :param models: List[str]
            Name of the used models

        :param top_n: int
            Number of top parameters to use
        """
        _meta_data: pd.DataFrame = pd.DataFrame(data=self.train_data[self.ml_type.split('_')[0]]['x'])
        for m in _meta_data.keys():
            if m.split('_')[0]:
                print(m, _meta_data[m].unique())
        _meta_data = _meta_data[[feature for feature in _meta_data.keys() if feature.split('_')[0] in models]]
        _param_name: List[str] = list(_meta_data.keys())
        _meta_data['y'] = self.train_data[self.ml_type.split('_')[0]]['y']
        self.imp_param.update({'imp_params': FeatureSelector(df=_meta_data,
                                                             target='y',
                                                             features=_param_name,
                                                             visualize_all_scores=True,
                                                             visualize_variant_scores=False,
                                                             visualize_core_feature_scores=False,
                                                             path=self.path,
                                                             **dict(stratification=False)
                                                             ).get_imp_features(meth='shapley',
                                                                                imp_threshold=0.01
                                                                                )['imp_features'][0:top_n]
                               })
        for param in self.imp_param.get('imp_params'):
            _feature_name: List[str] = param.split('_')
            _model_name: str = _feature_name[0]
            _param_name: str = param.replace('{}_'.format(_model_name), '')
            if _model_name in self.imp_param.keys():
                self.imp_param[_model_name].append(_param_name)
            else:
                self.imp_param.update({_model_name: [_param_name]})

    def predict_score(self, model_name: str, parameter: dict) -> float:
        """
        Evaluate actor decision by predicting fitness score of the chosen model a-priori

        :return: float
            Predicted fitness value of mutated model
        """
        _test_data: dict = {}
        _param_space: dict = PARAM_SPACE_REG if self.ml_type == 'reg' else PARAM_SPACE_CLF
        for space in self.parameter_space[self.ml_type.split('_')[0]].keys():
            if space in parameter.keys():
                for p in parameter.keys():
                    if isinstance(_param_space[model_name].get(p), list):
                        if isinstance(parameter.get(p), str):
                            _test_data.update({'{}_{}_{}'.format(model_name, p, parameter.get(p)): 1})
                        else:
                            for o in _param_space[model_name].get(p):
                                if str(parameter.get(p)).find(o.replace('{}_'.format(p), '')) >= 0:
                                    _test_data.update({'{}_{}'.format(model_name, o): 1})
                    else:
                        _test_data.update({'{}_{}'.format(model_name, p): parameter.get(p)})
            else:
                _test_data.update({space: self.parameter_space[self.ml_type.split('_')[0]][space]})
        return self.model.predict(x=pd.DataFrame(data=_test_data, index=[0]).values)

    def train_decision_tree(self, tree_meth: str = 'xgb'):
        """
        Train supervised decision tree critic for optimizing actions of genetic algorithm (actor)

        :param tree_meth: str
            Name of the decision tree method to use as critic
                -> xgb: Extreme Gradient Boosting Decision Tree
                -> rf: Random Forest
        """
        if tree_meth in ['rf', 'xgb']:
            _meth: str = tree_meth
        else:
            _meth: str = 'xgb'
        _meta_data: pd.DataFrame = pd.DataFrame(data=self.train_data[self.ml_type.split('_')[0]]['x'])
        _meta_data['y'] = self.train_data[self.ml_type.split('_')[0]]['y']
        _data: dict = MLSampler(df=_meta_data,
                                target='y',
                                train_size=0.8,
                                random=True,
                                stratification=False #True if self.ml_type.find('clf') >= 0 else False
                                ).train_test_sampling()
        self.model = ModelGeneratorReg(n_cases=_meta_data.shape[0],
                                       n_features=_meta_data.shape[1],
                                       model_name=_meth,
                                       reg_params=dict(n_estimators=50)
                                       ).generate_model()
        self.model.train(x=_data.get('x_train').values,
                         y=_data.get('y_train').values,
                         validation=dict(x_val=_data.get('x_val').values,
                                         y_val=_data.get('y_val').values
                                         )
                         )

    def train_policy_gradient(self):
        """
        Train reinforced Policy Gradient algorithm for optimizing action of genetic algorithm (actor)
        """
        raise NotImplementedError('Policy Gradient Critic not implemented')
