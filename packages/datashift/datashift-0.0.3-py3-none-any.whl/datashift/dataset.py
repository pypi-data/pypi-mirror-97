from __future__ import annotations

import csv
import glob
import json
import logging
import math
import multiprocessing
import os
import sys
from multiprocessing import Pool
from pathlib import Path
from typing import Iterator

import numpy as np
import pandas as pd
import yaml

from datashift.task import AbstractBalancingTask, TaskType, AbstractProcessingTask, AbstractFilterTask


class Data:
    """
        Lightweight and generic data processor that allows quickly filtering, balancing and processing a data set from one form to another.
        Especially useful for processing data from its original form to a form ready for advanced analysis and machine learning.
        It is possible to automatically generate final dataset statistics (metadata) after processing, i.e. number of observations in each class or in the whole dataset,
        which can be useful when adjusting a learning rate optimization during training of a machine learning model.
        List of features:
        -   loading data from multiple csv files,
        -   multi-thread processing of records,
        -   filtering out unwanted records,
        -   saving processed data to multiple files,
        -   balancing the proportion of observations in each class not only by number of elements but also by characteristics of the elements in each class (e.g. same proportion of color and grayscale images in each class),
        -   computing (reducing) numeric values - metadata of the dataset (e.g. number of elements in each class or minimum / maximum number of words in sentences),
        -   saving reduced values to yaml / json files.

        Args:
            input_data_path_pattern (str): Path to the folder where raw data are located
            output_data_dir_path (str): Path to the folder where finall processed data should be saved
            output_file_name_prefix (str): Generic filename prefix of all output (final) files
            processing_chunk_size (int): Number of observation that are processed at the same time. Higher chunk size use more RAM. (Default 20000).
            input_columns (lint[str]): List of column names to be read from the raw input files. To minimize memory consumption in need to load only required columns.
            output_file_size (int): Total number of records / observations written to a single output file. If the number of processed samples exceeds this value, a next new data file is created. (Default: 50000).
            num_workers (int): Number of processing threads. Higher number of threads results in faster processing and higher RAM consumption.
            output_metadata_file_path (str): Path to the file with reduced values (metadata). The file is only created when reducing tasks have been added for processing.
            output_metadata_file_format (str): Format of the file with reduced values (metadata). The file is only created when reducing tasks have been added for processing.
            saving_status_file_prefix (str): Location of a temporary file containing information about the saving status of processed results. The file is deleted after processing is complete and the output dataset is created. (Default: '.saving_status').
            verbose (bool): If it is set to True, processing statusses are logged to the logger during processing. If false, the logger is not used. (Default: True).
            logger: Custom logger to which logs are passed on. If the logger is undefined and verbose = True then a default logger is created to print statuses on the console. (Default: None).
        """

    _FLATTEN_ORDER_EXCEPTION = "The flatten task can only be executed after a processing stage. Currently the are no processing tasks assigned"

    def __init__(self, input_data_path_pattern, output_data_dir_path, output_file_name_prefix, input_columns,
                 output_file_size=50000,
                 processing_chunk_size=20000, num_workers=None, output_metadata_file_path=None,
                 output_metadata_file_format='yaml', saving_status_file_prefix='.saving_status', verbose=True,
                 logger=None):
        self.flattened_steps = []
        self.reduce_tasks = []
        assert output_metadata_file_format == 'yaml' or output_metadata_file_format == 'json' 'Only yaml and json files are supported to save reduced values.'
        self.num_workers = num_workers if num_workers is not None else multiprocessing.cpu_count() - 1
        self.input_data_path_pattern = input_data_path_pattern
        self.output_data_dir_path = output_data_dir_path
        self.output_file_name_prefix = output_file_name_prefix
        self.processing_chunk_size = processing_chunk_size
        self.input_columns = input_columns
        self.output_file_size = output_file_size
        self.tasks = []
        self.inference_tasks=[]
        self.output_files_counter = 0
        self.output_rows_last_file = 0
        self.output_metadata_file_path = output_metadata_file_path
        self.output_metadata_file_format = output_metadata_file_format
        self.saving_status_file_prefix = saving_status_file_prefix
        self.verbose = verbose
        if self.saving_status_file_prefix in self.output_file_name_prefix:
            raise Exception('The saving status file prefix ({}) can be a sub-name of output file name ({})',
                            self.saving_status_file_prefix, self.output_file_name_prefix)
        if verbose and logger is None:
            self.logger = self._create_and_configure_logger()
        elif verbose and logger is not None:
            self.logger = logger

    def process(self, task: AbstractProcessingTask, inference=False) -> Data:
        """
        Adds a new processing task
        """
        assert task.type() == TaskType.PROCESSOR
        self.tasks.append(task)
        if inference:
            self.inference_tasks.append(task)
        return self

    def filter(self, task: AbstractFilterTask, inference=False) -> Data:
        """
        Adds a new filtering task
        """
        assert task.type() == TaskType.FILTER
        self.tasks.append(task)
        if inference:
            self.inference_tasks.append(task)
        return self

    def reduce(self, task: AbstractFilterTask) -> Data:
        """
        Adds a new reducing task
        """
        assert task.type() == TaskType.REDUCER
        self.reduce_tasks.append(task)
        return self

    def balance(self, task: AbstractBalancingTask) -> Data:
        """
        Adds a new balancing task
        """
        assert task.type() == TaskType.BALANCING
        self.tasks.append(task)
        return self

    def flatten(self) -> Data:
        """
        Adds a new flattened task
        """
        if len(self.tasks) > 0 and all([t.type() != TaskType.PROCESSOR for t in self.tasks]):
            raise Exception(self._FLATTEN_ORDER_EXCEPTION)
        self.flattened_steps.append(len(self.tasks))
        return self

    def _create_and_configure_logger(self):
        logger = logging.getLogger('')
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        logger.addHandler(ch)
        return logger

    def _calculate_subcategories_probabilities(self, data_list, task: AbstractBalancingTask) -> dict:
        cat_and_subcat_dict = self._retrieve_and_validate_distribution_categories(data_list, task)
        adjusted_cat_and_subcat_dict = self._adjust_number_of_samples_per_subcategory(cat_and_subcat_dict,
                                                                                      task.max_proportion_difference_characteristic)
        adjusted_cat_and_subcat_dict = self._adjust_number_of_samples_per_category(adjusted_cat_and_subcat_dict,
                                                                                   task.max_proportion_difference_category)
        probabilities = {}
        for cat_name, subcategories in cat_and_subcat_dict.items():
            if cat_name not in probabilities:
                probabilities[cat_name] = {}
            for subcat_name, n_samples in subcategories.items():
                probabilities[cat_name][subcat_name] = adjusted_cat_and_subcat_dict[cat_name][subcat_name] / \
                                                       cat_and_subcat_dict[cat_name][subcat_name]
        return probabilities

    def _adjust_number_of_samples_per_category(self, cat_and_subcat_dict, max_proportion_difference_category) -> dict:
        min_cat = min(
            [sum(subcat.values()) for subcat in cat_and_subcat_dict.values()]) * max_proportion_difference_category
        for cat, subcat in cat_and_subcat_dict.items():
            to_remove = sum(subcat.values()) - min_cat
            subcat_sorted = {k: v for k, v in sorted(subcat.items(), key=lambda item: item[1], reverse=True)}
            new_values = self._remove_from_values(list(subcat.values()), to_remove)
            for k, v in zip(subcat_sorted.keys(), new_values):
                cat_and_subcat_dict[cat][k] = v
        return cat_and_subcat_dict

    def _remove_from_values(self, values, n_to_remove) -> list:
        assert sum(values) > n_to_remove
        values_len = len(values)
        while n_to_remove > 0:
            indices = [i for i in range(values_len) if values[0] == values[i]]
            if indices[-1] + 1 < values_len:
                possible_to_be_deleted = (values[indices[-1]] - values[indices[-1] + 1]) * len(indices)
            else:
                possible_to_be_deleted = n_to_remove
            for i in indices:
                current_to_be_removed = math.floor(possible_to_be_deleted / len(indices))
                if current_to_be_removed < 1:
                    current_to_be_removed = 1
                if current_to_be_removed > n_to_remove:
                    current_to_be_removed = n_to_remove
                values[i] = values[i] - current_to_be_removed
                n_to_remove = n_to_remove - current_to_be_removed
                if n_to_remove == 0:
                    break
        return values

    def _adjust_number_of_samples_per_subcategory(self, cat_and_subcat_dict,
                                                  max_proportion_difference_subcategory) -> dict:
        adjusted_cat_and_subcat_dict = {}
        for cat, subcat in cat_and_subcat_dict.items():
            adjusted_cat_and_subcat_dict[cat] = {}
            min_subcat = min(subcat.values()) * max_proportion_difference_subcategory
            for subcat_name in subcat:
                if subcat[subcat_name] > min_subcat:
                    adjusted_cat_and_subcat_dict[cat][subcat_name] = min_subcat
                else:
                    adjusted_cat_and_subcat_dict[cat][subcat_name] = subcat[subcat_name]
        return adjusted_cat_and_subcat_dict

    def _execute_pipeline(self, execution_groups) -> list:
        data_list = []
        for eg in execution_groups:
            df = pd.read_csv(eg[0], skiprows=eg[1], nrows=eg[2], usecols=eg[3]).fillna('')
            data_list += df.to_dict('records')
        assert len(self.tasks) > 0
        for t_iter, task in enumerate(self.tasks):
            if task.type() == TaskType.BALANCING:
                balancing_probabilities = self._calculate_subcategories_probabilities(data_list, task)
            elements = []
            for data in data_list:
                if task.type() == TaskType.PROCESSOR:
                    elements.append(task.process(data))
                elif task.type() == TaskType.FILTER and task.filter(data):
                    elements.append(data)
                elif task.type() == TaskType.BALANCING:
                    selected_categories = self._calculate_if_given_sample_should_be_selected(data, task,
                                                                                             balancing_probabilities)
                    if selected_categories:
                        task.mark_sample_as_selected(data, selected_categories)
                        elements.append(data)

            if t_iter + 1 in self.flattened_steps:
                data_list = [item for sublist in elements for item in sublist]
            else:
                data_list = elements
        if len(data_list) > 0:
            self._save(data_list, self.output_data_dir_path, self.output_file_name_prefix)
        if len(self.reduce_tasks) > 0 and len(data_list) > 0:
            return self._validate_and_reduce_locally(data_list)
        else:
            return []

    def _generate_file_path(self, output_data_dir, output_file_name_prefix, pid, file_nr) -> str:
        return os.path.join(output_data_dir, '{}_{}_{}.csv'.format(output_file_name_prefix, pid, file_nr))

    def _save(self, data, output_data_dir, output_file_name_prefix) -> None:
        pid = os.getpid()
        saving_status_file_path = '{}/{}_{}'.format(output_data_dir, self.saving_status_file_prefix, pid)
        last_file_path = None
        remaining = 0
        if os.path.isfile(saving_status_file_path):
            with open(saving_status_file_path, 'r') as f:
                last_file_path, last_file_items_str = f.readline().split(';')
                last_file_items = int(last_file_items_str)
                remaining = self.output_file_size - last_file_items
        if last_file_path and remaining > 0:
            self._save_to_csv(data[:remaining], last_file_path, encoding='utf-8', header=False)
            last_file_items+=remaining

        if len(data) > remaining:
            for data_part in self._chunk_by_n_rows(data[remaining:], self.output_file_size):
                next_file_nr = len(
                    glob.glob(self._generate_file_path(output_data_dir, output_file_name_prefix, pid, '*'))) + 1
                file_path = self._generate_file_path(output_data_dir, output_file_name_prefix, pid, next_file_nr)
                self._save_to_csv(data_part, file_path, encoding='utf-8', header=True)
                last_file_path = file_path
                last_file_items = len(data_part)
        with open(saving_status_file_path, 'w') as f:
            f.writelines(['{};{}'.format(last_file_path, last_file_items)])

    def _clean_savings_statuses(self, output_data_dir) -> None:
        saving_status_generic_file_path = '{}/{}_{}'.format(output_data_dir, self.saving_status_file_prefix, '*')
        for file_path in glob.glob(saving_status_generic_file_path):
            os.remove(file_path)

    def _calculate_if_given_sample_should_be_selected(self, sample, task, balancing_probabilities) -> list:
        selected_categories = []
        for category in task.determine_categories(sample):
            if np.random.uniform() <= balancing_probabilities[category][
                task.determine_characteristic(sample)]:
                selected_categories.append(category)
        return selected_categories

    def _calculate_min_occurences(self, dist_categories, max_proportion_difference) -> float:
        return min(dist_categories.values()) * max_proportion_difference

    def _retrieve_and_validate_distribution_categories(self, data_list, task: AbstractBalancingTask) -> dict:
        cat_and_subcat = {}
        for data in data_list:
            distribution_categories = task.determine_categories(data)
            if type(distribution_categories) != list or not distribution_categories or any(
                    [type(c) != str for c in distribution_categories]):
                raise TypeError(
                    'The balancing task should return distribution categories as a list of str, not {}.'.format(
                        type(distribution_categories)))
            distribution_subcategory = task.determine_characteristic(data)
            if type(distribution_subcategory) != str:
                raise TypeError('The balancing task should return distribution subcategory as str, not {}'.format(
                    type(distribution_subcategory)))
            for category in distribution_categories:
                if category not in cat_and_subcat:
                    cat_and_subcat[category] = {distribution_subcategory: 1}
                elif distribution_subcategory not in cat_and_subcat[category]:
                    cat_and_subcat[category][distribution_subcategory] = 1
                else:
                    cat_and_subcat[category][distribution_subcategory] += 1
        return cat_and_subcat

    def _validate_and_reduce_locally(self, data_list) -> dict:
        local_reduction = {}
        assert len(self.reduce_tasks) > 0
        for task in self.reduce_tasks:
            reduced_locally_value = task.reduce_locally(data_list)
            if type(reduced_locally_value) not in (float, int, str, dict):
                raise TypeError("Final value of the reduced chunk must be dict, float, int or str, not {}.".format(
                    type(reduced_locally_value)))
            if type(reduced_locally_value) == dict:
                for v in reduced_locally_value.values():
                    if type(v) not in (float, int, str):
                        raise TypeError(
                            "All values in the dictionary creaded during chunk reduction must be str, float or int, not {}.".format(
                                type(v)))
            local_reduction[task.reduced_value_name] = reduced_locally_value
        return local_reduction

    def _save_to_csv(self, data_list, file_path, header, encoding, mode='a') -> None:
        keys = data_list[0].keys()
        with open(file_path, mode, encoding=encoding) as output_file:
            dict_writer = csv.DictWriter(output_file, keys,quoting=csv.QUOTE_ALL)
            if header:
                dict_writer.writeheader()
            dict_writer.writerows(data_list)

    def _chunk_by_n_parts(self, data_list, num) -> list:
        avg = len(data_list) / float(num)
        out = []
        last = 0.0
        while last < len(data_list):
            out.append(data_list[int(last):int(last + avg)])
            last += avg
        return out

    def _chunk_by_n_rows(self, data_list, size) -> tuple:
        return (data_list[pos:pos + size] for pos in range(0, len(data_list), size))

    def gen_chunks(self, reader, chunksize) -> Iterator[list]:
        """
        Chunk generator. Take a CSV `reader` and yield
        `chunksize` sized slices.
        """
        chunk = []
        for i, line in enumerate(reader):
            if (i % chunksize == 0 and i > 0):
                yield chunk
                del chunk[:]
            chunk.append(line)
        yield chunk

    def _reduce_globally(self, reduction_task) -> tuple:
        task, local_reductions = reduction_task
        result = task.reduce_globally(local_reductions)
        if type(result) not in (float, int, str, dict):
            raise TypeError("Reduced values can be only dict, str, float or int, not {}.".format(type(result)))
        return task.reduced_value_name, result

    def _save_reduced(self, global_reductions) -> None:
        dict_to_save = {}
        for k, v in global_reductions:
            dict_to_save[k] = v
        Path(self.output_metadata_file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_metadata_file_path, 'w') as fp:
            if self.output_metadata_file_format == 'yaml':
                yaml.dump(dict_to_save, fp)
            elif self.output_metadata_file_format == 'json':
                json.dump(dict_to_save, fp)
            else:
                raise Exception("File extension {} not supported".format(self.output_metadata_file_format))

    def _calculate_lines(self, path) -> int:
        with open(path, 'r', encoding='utf-8') as f:
            first_key = next(csv.reader(f))[0]
        df_iter = pd.read_csv(path, usecols=[first_key], chunksize=self.processing_chunk_size)
        for i, df in enumerate(df_iter):
            continue
        return self.processing_chunk_size * i + df.shape[0]

    def _prepare_chunked_execution_groups(self, all_file_paths, pool, chunksize, input_columns) -> list:
        counts = pool.map(self._calculate_lines, all_file_paths)
        execution_groups = []
        remaining = 0
        for file, no_elements in zip(all_file_paths, counts):
            buffer_level = 0
            if remaining > 0:
                execution_groups[-1].append((file, range(0), min(remaining, no_elements), input_columns))
                remaining = min(remaining, no_elements)
                buffer_level = min(remaining, no_elements)

            while buffer_level != no_elements:
                if buffer_level + chunksize <= no_elements:
                    execution_groups.append([(file, range(1, buffer_level), chunksize, input_columns)])
                    buffer_level += chunksize
                else:
                    execution_groups.append([(file, range(1, buffer_level), no_elements - buffer_level, input_columns)])
                    remaining = chunksize - (no_elements - buffer_level)
                    buffer_level += (no_elements - buffer_level)
        return execution_groups

    def shift(self) -> None:
        """
        Performs processing of the dataset according to the created pipeline.
        """
        self._print_logs('Dataset shifting has started - {} workers.'.format(self.num_workers))
        if len(self.reduce_tasks) == 0 and self.output_metadata_file_path is not None:
            raise AssertionError("You have defined a file name for reduce output but there is no task to reduce.")
        if len(self.reduce_tasks) > 0 and self.output_metadata_file_path is None:
            raise AssertionError(
                "You have defined {} tasks to reduce but a file name for reduce output is still not defined.".format(
                    len(self.reduce_tasks)))
        if self.output_data_dir_path and not os.path.exists(self.output_data_dir_path):
            os.makedirs(self.output_data_dir_path)
        pool = Pool(self.num_workers)
        all_file_paths = glob.glob(self.input_data_path_pattern)
        if not all_file_paths:
            raise FileNotFoundError('Files were not found in the location : {}'.format(self.input_data_path_pattern))
        self._print_logs(
            'Localized {} files to be shifted from {} to {}.'.format(len(all_file_paths), self.input_data_path_pattern,
                                                                     self.output_data_dir_path))
        self._print_logs(
            'Data scanning and generation of data chunks for multi-threaded execution. This may take a while...')
        execution_groups = self._prepare_chunked_execution_groups(all_file_paths, pool, self.processing_chunk_size,
                                                                  self.input_columns)
        self._print_logs(
            'Created {} execution chunks for multi-threaded execution. Each chunk contains {} elements/observations.'.format(
                len(execution_groups), self.processing_chunk_size))
        self._print_logs('Processing has started...')
        local_reductions = pool.map(self._execute_pipeline, execution_groups)
        self._print_logs('Processing completed. {} output files saved to {}.'.format(len(execution_groups),
                                                                                     self.output_data_dir_path))
        self._clean_savings_statuses(self.output_data_dir_path)
        if len(self.reduce_tasks) > 0:
            self._print_logs('Metadata generation has started...')
            local_reductions = [lr for lr in local_reductions if lr is not None]
            global_reduction_tasks = [(task, [lr[task.reduced_value_name] for lr in local_reductions]) for task in
                                      self.reduce_tasks]
            global_reductions = pool.map(self._reduce_globally, global_reduction_tasks)
            self._save_reduced(global_reductions)
            self._print_logs(
                'Metadata generation completed. Statistics saved to {}.'.format(self.output_metadata_file_path))
        self._print_logs(
            'Data from {} SUCCESSFULLY shifted to {}!'.format(self.input_data_path_pattern, self.output_data_dir_path))
        pool.close()

    def inference(self, data):
        for inference_task in self.inference_tasks:
            if inference_task.type()==TaskType.PROCESSOR:
                data=inference_task.process(data)
            elif inference_task.type()==TaskType.FILTER and not inference_task.filter(data):
                return None
            else:
                raise Exception('Unsupported task for inference {}.'.format(inference_task.type()))
        return data

    def _print_logs(self, message):
        if self.verbose:
            self.logger.info(message)