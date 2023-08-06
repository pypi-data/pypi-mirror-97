#!/usr/bin/env python3

### Warnings ###
import warnings

warnings.filterwarnings("ignore")

### System ###
import os
import sys
import json
import shutil
import inspect
import configparser
from glob import glob
from hashlib import md5
from collections import defaultdict

### CLI ###
import click

### Display ###
from termcolor import colored

### Logging ###
import logging
import logzero
from logzero import logger, LogFormatter

### Data Handling ###
# import pandas as pd

### Hyperparameter Optimization ###
from mango import scheduler, Tuner

### MoonLine ###
from linechart import Tearsheet, DailyPerformance, AggregateDailyPerformance
from moonline import main as moonline_main, get_config as moonline_get_config


space_x_config = {}
moonline_config = {}
moonline_config_custom = {}


def make_hash_md5(o):
    return md5(repr(make_hashable(o)).encode()).hexdigest()


def make_hashable(o):
    if isinstance(o, (tuple, list)):
        return tuple((make_hashable(e) for e in o))

    if isinstance(o, dict):
        return tuple(sorted((k, make_hashable(v)) for k, v in o.items()))

    if isinstance(o, (set, frozenset)):
        return tuple(sorted(make_hashable(e) for e in o))

    return o


def get_config(config_file, args=[]):
    config = configparser.ConfigParser()
    config.read(config_file)

    valid_categories = set(["MoonLine", "SpaceX", "Output", "Parameters"])

    config_object = defaultdict(dict)
    config_object_custom = defaultdict(dict)
    for section in config.sections():
        if section in valid_categories:
            for k, v in config[section].items():
                config_object[section][k] = v
        else:
            for k, v in config[section].items():
                config_object_custom[section.lower()][k] = v

    for i, item in enumerate(args):
        if i % 2 == 0:
            if ":" in item:
                section, value = item.lstrip("-").split(":")
            else:
                section, value = None, None
        elif section and value:
            config_object_custom[section][value] = item

    errors = []

    iterations = config_object["SpaceX"].get("iterations", None)
    if not iterations:
        config_object["SpaceX"]["iterations"] = 20
    else:
        try:
            config_object["SpaceX"]["iterations"] = int(iterations)
        except Exception as e:
            errors.append(("[SpaceX]->iterations", str(e), config_object["SpaceX"]["iterations"]))

    config_object["MoonLine"]["path"] = os.path.abspath(config_object["MoonLine"]["path"])
    if not os.path.isfile(config_object["MoonLine"]["path"]):
        errors.append(("[MoonLine]->path", "Not a file", config_object["MoonLine"]["path"]))

    config_object["Output"]["path"] = os.path.abspath(config_object["Output"]["path"])
    if os.path.isfile(config_object["Output"]["path"]):
        errors.append(("[Output]->path", "Output path is a file", config_object["Output"]["path"]))
    else:
        if os.path.isdir(config_object["Output"]["path"]):
            shutil.rmtree(config_object["Output"]["path"])
        os.makedirs(config_object["Output"]["path"])

    best_tearsheet = config_object["Output"].get("best_tearsheet", None)
    if best_tearsheet:
        config_object["Output"]["best_tearsheet"] = os.path.abspath(config_object["Output"]["best_tearsheet"])
    else:
        config_object["Output"]["best_tearsheet"] = None

    config_object["Parameters"]["path"] = os.path.abspath(config_object["Parameters"]["path"])
    if not os.path.isdir(config_object["Parameters"]["path"]):
        errors.append(("[Parameters]->path", "Not a directory", config_object["Parameters"]["path"]))
    else:
        found_parameter_files = glob(
            os.path.join(config_object["Parameters"]["path"], "**", "*.py"),
            recursive=True,
        )
        if not found_parameter_files:
            errors.append(("[Parameters]->name", "No parameter files found", None))
        if not config_object["Parameters"].get("name", None) and len(found_parameter_files) > 1:
            errors.append(
                (
                    "[Parameters]->name",
                    "More than one parameters file found but no name was specified",
                    None,
                )
            )

    if errors:
        for config_section, message, faulty_value in errors:
            if faulty_value:
                logger.error(
                    "{} | {} ({})".format(
                        colored(config_section, "magenta"),
                        colored(message, "red"),
                        faulty_value,
                    )
                )
            else:
                logger.error("{} | {}".format(colored(config_section, "magenta"), colored(message, "red")))
        sys.exit(1)

    return dict(config_object), dict(config_object_custom)


def get_parameters(parameter_library_path, parameter_name):
    parameter_files = glob(os.path.join(parameter_library_path, "**", "*.py"), recursive=True)
    tmp_dir = os.path.join(os.path.dirname(__file__), "parameters_tmp")
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir, exist_ok=True)
    for file in parameter_files:
        shutil.copyfile(file, os.path.join(tmp_dir, os.path.basename(file)))
    parameter_files = [
        os.path.join("parameters_tmp", os.path.basename(file))
        for file in glob(os.path.join(tmp_dir, "**", "*.py"), recursive=True)
    ]

    for file in parameter_files:
        if parameter_name == os.path.basename(file):
            try:
                module_name = ".".join(os.path.splitext(file)[0].split(os.sep))
                __import__(module_name, globals=globals(), locals=locals())
            except:
                module_name = "space_x." + ".".join(os.path.splitext(file)[0].split(os.sep))
                __import__(module_name, globals=globals(), locals=locals())
            classes = [(name, obj) for name, obj in inspect.getmembers(sys.modules[module_name], inspect.isclass)]
            for name, strategy_class in classes:
                if "Params" in name:
                    return strategy_class

    available_parameters = {}
    for file in parameter_files:
        try:
            module_name = ".".join(os.path.splitext(file)[0].split(os.sep))
            __import__(module_name, globals=globals(), locals=locals())
        except:
            module_name = "space_x." + ".".join(os.path.splitext(file)[0].split(os.sep))
            __import__(module_name, globals=globals(), locals=locals())
        classes = [(name, obj) for name, obj in inspect.getmembers(sys.modules[module_name], inspect.isclass)]
        for name, strategy_class in classes:
            if "Params" in name:
                available_parameters[name] = strategy_class

    if len(available_parameters) > 1:
        if parameter_name:
            target_class = available_parameters[parameter_name]
            return target_class
        else:
            names = ", ".join([colored(name, "magenta") for name in available_parameters.keys()])
            raise Exception(
                "More than one strategy candidate found: {}\n\t   Please select one with the 'name' option in config.ini".format(
                    names
                )
            )  # noqa: E501

    if not available_parameters:
        raise Exception("No strategies were found")

    target_class = available_parameters[list(available_parameters.keys())[0]]

    return target_class


# @scheduler.serial
@scheduler.parallel(n_jobs=4)
def moonline_objective(**kwargs):
    global space_x_config, moonline_config, moonline_config_custom
    config = defaultdict(dict)
    config_custom = defaultdict(dict)

    config.update(moonline_config)
    config_custom.update(moonline_config_custom)

    for k, v in kwargs.items():
        section, name = k.split(":")
        if section in config:
            config[section.lower()][name] = v
        config_custom[section.lower()][name] = v

    path_hash = make_hash_md5(kwargs)

    weight_path = os.path.join(space_x_config["Output"]["path"], path_hash, "weights.csv")
    tearsheet_path = os.path.join(space_x_config["Output"]["path"], path_hash, "tearsheet.csv")
    parameter_path = os.path.join(space_x_config["Output"]["path"], path_hash, "parameters.json")

    os.makedirs(os.path.dirname(weight_path), exist_ok=True)

    config["Output"]["weights"] = weight_path
    config["Output"]["tearsheet_csv"] = tearsheet_path

    logzero.loglevel(logging.CRITICAL)

    moonline_main(config, config_custom)

    logzero.loglevel(logging.INFO)

    with open(parameter_path, "w") as f:
        json.dump(kwargs, f)

    # weights = pd.read_csv(weight_path)
    # tearsheet = pd.read_csv(tearsheet_path)

    perf = DailyPerformance.from_moonshot_csv(tearsheet_path)
    perf_agg = AggregateDailyPerformance(perf)

    score = (perf_agg.cagr - (perf_agg.cagr * perf_agg.max_drawdown)) + perf_agg.sharpe

    # logger.info(f"CAGR: {perf_agg.cagr * 100:.2f}%")
    # logger.info(f"Sharpe: {perf_agg.sharpe}")
    # logger.info(f"Drawdown: {perf_agg.max_drawdown * 100:.2f}%")
    # logger.info(f"Score: {score}")

    return score


@click.command(context_settings={"ignore_unknown_options": True, "allow_extra_args": True})
@click.option(
    "-c",
    "--config",
    "config_file",
    required=True,
    type=click.Path(dir_okay=False, exists=True, resolve_path=True),
    help="A file containing Space-X configuration options",
)
@click.option("-v", "--verbose", is_flag=True)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def cli(config_file, verbose, args):
    global space_x_config, moonline_config, moonline_config_custom

    formatter = LogFormatter(
        fmt="%(color)s[%(levelname)1.1s %(asctime)s]%(end_color)s %(message)s",
        datefmt="%H:%M:%S",
    )
    logzero.formatter(formatter)

    logzero.loglevel(logging.DEBUG if verbose else logging.INFO)

    space_x_config, _ = get_config(config_file)

    params = get_parameters(space_x_config["Parameters"]["path"], space_x_config["Parameters"]["name"])

    logger.info("Loading Parameters")
    params = params()
    available_params = params.get_sections()

    param_space = {}
    for section in available_params:
        for param, value in section.get_parameters():
            param_space[param] = value

    moonline_config, moonline_config_custom = moonline_get_config(space_x_config["MoonLine"]["path"], args)

    # Disable PDF tearsheet generation
    moonline_config["Output"]["tearsheet"] = None
    # Disable order generation
    moonline_config["Output"]["orders"] = None
    # Disable shutil.rmtree during strategy copy (this conflicts when using parallel processing)
    moonline_config["System"]["clear_tmp_dir"] = False
    # Enable quiet mode to reduce log spam
    moonline_config["System"]["quiet"] = True

    logger.info(f"Running Hyperparameter Optimization with {space_x_config['SpaceX']['iterations']} iterations")
    tuner = Tuner(param_space, moonline_objective, {"num_iteration": space_x_config["SpaceX"]["iterations"]})

    results = tuner.maximize()

    logger.info(f"Best Parameters: {results['best_params']}")
    logger.info(f"Best Objective: {results['best_objective']}")

    # Generate tearsheet for best run
    if space_x_config["Output"]["best_tearsheet"]:
        best_hash = make_hash_md5(results["best_params"])

        tearsheet_path = os.path.join(space_x_config["Output"]["path"], best_hash, "tearsheet.csv")

        file_no_ext = os.path.splitext(space_x_config["Output"]["best_tearsheet"])[0]
        shutil.copyfile(tearsheet_path, f"{file_no_ext}.csv")
        Tearsheet.from_moonshot_csv(f"{file_no_ext}.csv", pdf_filename=f"{file_no_ext}.pdf")

    for params_tried, score in sorted(zip(results["params_tried"], results["objective_values"]), key=lambda x: x[1]):
        logger.info(f"{params_tried}: {score}")
