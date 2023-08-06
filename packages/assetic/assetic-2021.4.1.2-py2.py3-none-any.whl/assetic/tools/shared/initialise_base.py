import abc
import logging
import sys

import six

import assetic
from assetic.tools.shared.config_base import ConfigBase


@six.add_metaclass(abc.ABCMeta)
class InitialiseBase:
    def __init__(self, __version__, configfile=None, inifile=None, logfile=None
                 , loglevelname=None, config=None):
        """
        Constructor of the class.

        :Param configfile: the name of the XML config file with ESRI to
        Assetic field mappings. If none then will look in the users
        appdata\Assetic folder for arcmap_edit_config.xml
        :Param inifile: the file name (including path) of the ini file
        (host, username, api_key).
        If none then will look in local folder for assetic.ini
        ,else look in environment variables for asseticSDKhost
        , asseticSDKusername,asseticSDKapi_key
        :Param logfile: the file name (including path) of the log file.
        If None then no logfile will be created
        :Param loglevelname: set as a valid logging level description
        e.g. INFO
        """

        config = config  # type: ConfigBase
        warn_log_level_conflict = False

        # check of log level is defined in config file and use that
        if config.loglevelname and config.layerconfig and config.layerconfig.loglevel:
            if config.loglevelname != config.layerconfig.loglevel:
                warn_log_level_conflict = True
                loglevelname = config.layerconfig.loglevel
        elif config.layerconfig and config.layerconfig.loglevel:
            loglevelname = config.layerconfig.loglevel

        warn_log_file_conflict = False
        # check of log file name defined in config file and use that
        if config.logfile and config.layerconfig and config.layerconfig.logfile:
            if config.logfile != config.layerconfig.logfile:
                warn_log_file_conflict = True
                logfile = config.layerconfig.logfile
        elif not config.logfile and config.layerconfig and config.layerconfig.logfile:
            logfile = config.layerconfig.logfile

        # initialise the Assetic sdk library
        config.loglevel = logging.DEBUG

        msg = "Initiated Assetic Spatial Integration. Version {0}".format(__version__)
        config.asseticsdk.logger.info(msg)
        if warn_log_file_conflict:
            config.asseticsdk.logger.warn(
                "Differing logfile names defined in configuration xml and "
                "passed in parameter.  Definition in configuration xml will "
                "be used")
        if warn_log_level_conflict:
            config.asseticsdk.logger.warn(
                "Differing log levels defined in configuration xml and "
                "passed in parameter.  Definition in configuration xml will "
                "be used")

        logging.getLogger().addHandler(logging.StreamHandler())

        assetic_sdk_handle = None
        for sdk_handle in config.asseticsdk.logger.handlers:
            if isinstance(sdk_handle, logging.handlers.RotatingFileHandler):
                assetic_sdk_handle = sdk_handle
                break
        if config.logfile and not assetic_sdk_handle:
            assetic_sdk_handle = logging.FileHandler(config.logfile)
        elif not config.logfile:
            assetic_sdk_handle = logging.StreamHandler(sys.stdout)

        assetic_sdk_handle = logging.StreamHandler(sys.stdout)
        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
        rootLogger = logging.getLogger()

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)
        # when the assetic-esri package is initiated a logger is created
        # to catch any issues that occur before this config instance is
        # initialised
        # Now we have a log file defined in the config we can remove
        # that handler and attach the sdk handler
        assetic_logger = logging.getLogger(__name__).parent
        for handle in assetic_logger.handlers:
            if isinstance(handle, logging.FileHandler):
                assetic_logger.removeHandler(handle)
                # now attach the handler defined in the xml config file
                assetic_logger.addHandler(assetic_sdk_handle)
                break

        assetic_logger.addHandler(assetic_sdk_handle)
        logging.getLogger(__name__).addHandler(logging.StreamHandler(sys.stdout))

        min_version = "2019.13.2.0"
        try:
            assetic_version = assetic.__version__.__version__.split(".")
        except Exception as ex:
            config.asseticsdk.logger.info("Unable to determine version of"
                                          " Assetic python package: {0}"
                                          .format(ex))
        else:
            if assetic_version >= min_version.split("."):
                pass
            else:
                # version may be too old.  Issue warning
                config.asseticsdk.logger.warning(
                    "Current version of assetic python package is too old."
                    " Version is: {0}, expecting minimum of {1}".format(
                        assetic.__version__.__version__), min_version)
