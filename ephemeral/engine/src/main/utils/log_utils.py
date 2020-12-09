"""
This package exposes python standard logging behaviors to ephemeral code
and code libraries using ephemeral.
"""
import logging
import ephemeral.engine.src.main.utils.file_utils as file_utils


class logger:

    valid_levels = {"info": logging.INFO,
                    "debug": logging.DEBUG,
                    "warn": logging.WARN,
                    "error": logging.ERROR,
                    "critical": logging.CRITICAL,
                    "exception": logging.ERROR}

    def __init__(self, library, job, filename=None, level="info", append=True,
                 include_system_messages=False):
        """ The ephemeral logger class creates a log object that can be used
        throughout ephemeral and associated user code. When
        pulled out of ephemeral, user code that uses logger methods will then
        use the python builtin logging methods. In ephemeral, log messages are
        printed with a datetime and qualified by a library, job, and task
        namespace. When creating the logger, users can specify a maximum log
        level, log name, whether to recreate a logfile or append to it, and
        whether or not to ignore system messages.
        """
        self.lib = library
        self.job = job
        self.level = self._validate_level(level)
        self.filename = self._validate_filename(filename)
        self.system = self._validate_system_messages(include_system_messages)
        self.append = self._validate_append(append)
        logging.basicConfig(level=self.level,
                            filename=self.filename,
                            filemode=self.append,
                            format='%(asctime)s %(lib)s %(job)s %(task)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def log(self, message, task=''):
        """ A convenience method of the logger class, writes the given message
        to the established log using the current log level.
        """
        if self.level == logging.INFO:
            self.info(message, task=task)
        elif self.level == logging.DEBUG:
            self.debug(message, task=task)
        elif self.level == logging.WARN:
            self.warn(message, task=task)
        elif self.level == logging.ERROR:
            self.error(message, task=task)
        elif self.level == logging.CRITICAL:
            self.critical(message, task=task)

    def info(self, message, task=''):
        """Prints an info message to the log using the established logger.
        """
        logging.info(message, extra=self._make_context(self.lib,
                                                       self.job,
                                                       task))

    def debug(self, message, task=''):
        """Prints a debug message to the log using the established logger.
        """
        logging.debug(message, extra=self._make_context(self.lib,
                                                        self.job,
                                                        task))

    def warn(self, message, task=''):
        """Prints a warn message to the log using the established logger.
        """
        logging.warning(message, extra=self._make_context(self.lib,
                                                          self.job,
                                                          task))

    def error(self, message, task=''):
        """Prints an error message to the log using the established logger.
        """
        logging.error(message, extra=self._make_context(self.lib,
                                                        self.job,
                                                        task))

    def critical(self, message, task=''):
        """Prints a critical message to the log using the established logger.
        """
        logging.critical(message, extra=self._make_context(self.lib,
                                                           self.job,
                                                           task))

    def exception(self, message, task=''):
        """Prints an exception to the log using the established logger.
        """
        logging.exception(message, extra=self._make_context(self.lib,
                                                            self.job,
                                                            task))

    def _validate_level(self, level):
        """ Validates the passed level and returns an appropriate level.
        """
        if level.lower() in list(self.valid_levels.keys()):
            return self.valid_levels(level.lower())
        return self.valid_levels("info")

    def _validate_filename(self, filename):
        """ Validates the passed filename and returns an appropriate filename.
        """
        if filename is not None:
            return filename
        return '.'.join(file_utils.get_relative_package_path(),
                        self.lib, self.job, 'output', 'log')

    def _validate_append(self, append):
        """Validates an append boolean (file write type).
        """
        if append:
            return 'a'
        return 'w'

    def _validate_system_messages(self, include_system_messages):
        """Validates a keyword that determines whether or not to include
        system messages (from the ephemeral engine) when running. Turning this
        on will include system messages that describe the running system at the
        log level that's provided.
        """
        if include_system_messages:
            return True
        return False

    def _make_context(lib, job, task):
        """Creates contextual information for the logger.
        """
        return {'lib': lib,
                'job': job,
                'task': task}
