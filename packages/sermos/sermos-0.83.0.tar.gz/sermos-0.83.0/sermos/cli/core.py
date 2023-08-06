""" Primary CLI group entrypoint
"""
import click
import logging

logger = logging.getLogger(__name__)

# Not all CLI tools will be functional / available depending on which extras
# are installed. For example, the config server won't work if the `workers`
# extra isn't available, which installs celery and networkx.
collection = []

warning_msg = "{} CLI tools are not available. This is most "\
               "likely due to a missing import. Verify you have the correct "\
               "Sermos extras installed."
try:
    from sermos.cli.deploy import deployment
    collection.append(deployment)
except ImportError as e:
    logger.warning(warning_msg.format("Deployment"))
    logger.warning(f"{e}")

try:
    from sermos.cli.config_server import config_server
    collection.append(config_server)
except ImportError as e:
    logger.warning(warning_msg.format("Configuration Server"))
    logger.warning(f"{e}")

sermos = click.CommandCollection(sources=collection)
