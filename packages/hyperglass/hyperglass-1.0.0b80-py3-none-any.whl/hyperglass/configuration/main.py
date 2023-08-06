"""Import configuration files and returns default values if undefined."""

# Standard Library
import os
import copy
import json
from typing import Dict, List
from pathlib import Path

# Third Party
import yaml

# Project
from hyperglass.log import (
    log,
    set_log_level,
    enable_file_logging,
    enable_syslog_logging,
)
from hyperglass.util import set_app_path, set_cache_env, current_log_level
from hyperglass.constants import (
    SUPPORTED_QUERY_TYPES,
    PARSED_RESPONSE_FIELDS,
    __version__,
)
from hyperglass.exceptions import ConfigError, ConfigMissing
from hyperglass.util.files import check_path
from hyperglass.models.commands import Commands
from hyperglass.models.config.params import Params
from hyperglass.models.config.devices import Devices
from hyperglass.configuration.defaults import (
    CREDIT,
    DEFAULT_HELP,
    DEFAULT_TERMS,
    DEFAULT_DETAILS,
)

# Local
from .markdown import get_markdown
from .validation import validate_config, validate_nos_commands

set_app_path(required=True)

CONFIG_PATH = Path(os.environ["hyperglass_directory"])
log.info("Configuration directory: {d}", d=str(CONFIG_PATH))

# Project Directories
WORKING_DIR = Path(__file__).resolve().parent
CONFIG_FILES = (
    ("hyperglass.yaml", False),
    ("devices.yaml", True),
    ("commands.yaml", False),
)


def _check_config_files(directory: Path):
    """Verify config files exist and are readable."""

    files = ()

    for file in CONFIG_FILES:
        file_name, required = file
        file_path = directory / file_name

        checked = check_path(file_path)

        if checked is None and required:
            raise ConfigMissing(missing_item=str(file_path))

        if checked is None and not required:
            log.warning(
                "'{f}' was not found, but is not required to run hyperglass. "
                + "Defaults will be used.",
                f=str(file_path),
            )
        files += (checked,)

    return files


STATIC_PATH = CONFIG_PATH / "static"

CONFIG_MAIN, CONFIG_DEVICES, CONFIG_COMMANDS = _check_config_files(CONFIG_PATH)


def _config_required(config_path: Path) -> Dict:
    try:
        with config_path.open("r") as cf:
            config = yaml.safe_load(cf)

    except (yaml.YAMLError, yaml.MarkedYAMLError) as yaml_error:
        raise ConfigError(str(yaml_error))

    if config is None:
        log.critical("{} appears to be empty", str(config_path))
        raise ConfigMissing(missing_item=config_path.name)

    return config


def _config_optional(config_path: Path) -> Dict:

    config = {}

    if config_path is None:
        return config

    else:
        try:
            with config_path.open("r") as cf:
                config = yaml.safe_load(cf) or {}

        except (yaml.YAMLError, yaml.MarkedYAMLError) as yaml_error:
            raise ConfigError(error_msg=str(yaml_error))

    return config


user_config = _config_optional(CONFIG_MAIN)

# Read raw debug value from config to enable debugging quickly.
set_log_level(logger=log, debug=user_config.get("debug", True))

# Map imported user configuration to expected schema.
log.debug("Unvalidated configuration from {}: {}", CONFIG_MAIN, user_config)
params = validate_config(config=user_config, importer=Params)

# Re-evaluate debug state after config is validated
log_level = current_log_level(log)

if params.debug and log_level != "debug":
    set_log_level(logger=log, debug=True)
elif not params.debug and log_level == "debug":
    set_log_level(logger=log, debug=False)

# Map imported user commands to expected schema.
_user_commands = _config_optional(CONFIG_COMMANDS)
log.debug("Unvalidated commands from {}: {}", CONFIG_COMMANDS, _user_commands)
commands = validate_config(config=_user_commands, importer=Commands.import_params)

# Map imported user devices to expected schema.
_user_devices = _config_required(CONFIG_DEVICES)
log.debug("Unvalidated devices from {}: {}", CONFIG_DEVICES, _user_devices)
devices = validate_config(config=_user_devices.get("routers", []), importer=Devices)

# Validate commands are both supported and properly mapped.
validate_nos_commands(devices.all_nos, commands)

# Set cache configurations to environment variables, so they can be
# used without importing this module (Gunicorn, etc).
set_cache_env(db=params.cache.database, host=params.cache.host, port=params.cache.port)

# Set up file logging once configuration parameters are initialized.
enable_file_logging(
    logger=log,
    log_directory=params.logging.directory,
    log_format=params.logging.format,
    log_max_size=params.logging.max_size,
)

# Set up syslog logging if enabled.
if params.logging.syslog is not None and params.logging.syslog.enable:
    enable_syslog_logging(
        logger=log,
        syslog_host=params.logging.syslog.host,
        syslog_port=params.logging.syslog.port,
    )

if params.logging.http is not None and params.logging.http.enable:
    log.debug("HTTP logging is enabled")

# Perform post-config initialization string formatting or other
# functions that require access to other config levels. E.g.,
# something in 'params.web.text' needs to be formatted with a value
# from params.
try:
    params.web.text.subtitle = params.web.text.subtitle.format(
        **params.dict(exclude={"web", "queries", "messages"})
    )

    # If keywords are unmodified (default), add the org name &
    # site_title.
    if Params().site_keywords == params.site_keywords:
        params.site_keywords = sorted(
            {*params.site_keywords, params.org_name, params.site_title}
        )

except KeyError:
    pass


def _build_frontend_devices():
    """Build filtered JSON structure of devices for frontend.

    Schema:
    {
        "device.name": {
            "display_name": "device.display_name",
            "vrfs": [
                "Global",
                "vrf.display_name"
            ]
        }
    }

    Raises:
        ConfigError: Raised if parsing/building error occurs.

    Returns:
        {dict} -- Frontend devices
    """
    frontend_dict = {}
    for device in devices.objects:
        if device.name in frontend_dict:
            frontend_dict[device.name].update(
                {
                    "network": device.network.display_name,
                    "display_name": device.display_name,
                    "vrfs": [
                        {
                            "id": vrf.name,
                            "display_name": vrf.display_name,
                            "default": vrf.default,
                            "ipv4": True if vrf.ipv4 else False,  # noqa: IF100
                            "ipv6": True if vrf.ipv6 else False,  # noqa: IF100
                        }
                        for vrf in device.vrfs
                    ],
                }
            )
        elif device.name not in frontend_dict:
            frontend_dict[device.name] = {
                "network": device.network.display_name,
                "display_name": device.display_name,
                "vrfs": [
                    {
                        "id": vrf.name,
                        "display_name": vrf.display_name,
                        "default": vrf.default,
                        "ipv4": True if vrf.ipv4 else False,  # noqa: IF100
                        "ipv6": True if vrf.ipv6 else False,  # noqa: IF100
                    }
                    for vrf in device.vrfs
                ],
            }
    if not frontend_dict:
        raise ConfigError(error_msg="Unable to build network to device mapping")
    return frontend_dict


def _build_networks() -> List[Dict]:
    """Build filtered JSON Structure of networks & devices for Jinja templates."""
    networks = []
    _networks = list(set({device.network.display_name for device in devices.objects}))

    for _network in _networks:
        network_def = {"display_name": _network, "locations": []}
        for device in devices.objects:
            if device.network.display_name == _network:
                network_def["locations"].append(
                    {
                        "_id": device._id,
                        "name": device.name,
                        "network": device.network.display_name,
                        "vrfs": [
                            {
                                "_id": vrf._id,
                                "display_name": vrf.display_name,
                                "default": vrf.default,
                                "ipv4": True if vrf.ipv4 else False,  # noqa: IF100
                                "ipv6": True if vrf.ipv6 else False,  # noqa: IF100
                            }
                            for vrf in device.vrfs
                        ],
                    }
                )
        networks.append(network_def)

    if not networks:
        raise ConfigError(error_msg="Unable to build network to device mapping")
    return networks


content_params = json.loads(
    params.json(include={"primary_asn", "org_name", "site_title", "site_description"})
)


def _build_vrf_help() -> Dict:
    """Build a dict of vrfs as keys, help content as values."""
    all_help = {}
    for vrf in devices.vrf_objects:

        vrf_help = {}
        for command in SUPPORTED_QUERY_TYPES:
            cmd = getattr(vrf.info, command)
            if cmd.enable:
                help_params = {**content_params, **cmd.params.dict()}

                if help_params["title"] is None:
                    command_params = getattr(params.queries, command)
                    help_params[
                        "title"
                    ] = f"{vrf.display_name}: {command_params.display_name}"

                md = get_markdown(
                    config_path=cmd,
                    default=DEFAULT_DETAILS[command],
                    params=help_params,
                )

                vrf_help.update(
                    {
                        command: {
                            "content": md,
                            "enable": cmd.enable,
                            "params": help_params,
                        }
                    }
                )

        all_help.update({vrf._id: vrf_help})

    return all_help


content_greeting = get_markdown(
    config_path=params.web.greeting,
    default="",
    params={"title": params.web.greeting.title},
)

content_vrf = _build_vrf_help()

content_help_params = copy.copy(content_params)
content_help_params["title"] = params.web.help_menu.title
content_help = get_markdown(
    config_path=params.web.help_menu, default=DEFAULT_HELP, params=content_help_params
)

content_terms_params = copy.copy(content_params)
content_terms_params["title"] = params.web.terms.title
content_terms = get_markdown(
    config_path=params.web.terms, default=DEFAULT_TERMS, params=content_terms_params
)
content_credit = CREDIT.format(version=__version__)

networks = _build_networks()
frontend_devices = _build_frontend_devices()
_include_fields = {
    "cache": {"show_text", "timeout"},
    "debug": ...,
    "developer_mode": ...,
    "primary_asn": ...,
    "request_timeout": ...,
    "org_name": ...,
    "google_analytics": ...,
    "site_title": ...,
    "site_description": ...,
    "site_keywords": ...,
    "web": ...,
    "messages": ...,
}
_frontend_params = params.dict(include=_include_fields)


_frontend_params["web"]["logo"]["light_format"] = params.web.logo.light.suffix
_frontend_params["web"]["logo"]["dark_format"] = params.web.logo.dark.suffix

_frontend_params.update(
    {
        "hyperglass_version": __version__,
        "queries": {**params.queries.map, "list": params.queries.list},
        "networks": networks,
        "parsed_data_fields": PARSED_RESPONSE_FIELDS,
        "content": {
            "help_menu": content_help,
            "terms": content_terms,
            "credit": content_credit,
            "vrf": content_vrf,
            "greeting": content_greeting,
        },
    }
)
frontend_params = _frontend_params

URL_DEV = f"http://localhost:{str(params.listen_port)}/"
URL_PROD = "/api/"

REDIS_CONFIG = {
    "host": str(params.cache.host),
    "port": params.cache.port,
    "decode_responses": True,
    "password": params.cache.password,
}
