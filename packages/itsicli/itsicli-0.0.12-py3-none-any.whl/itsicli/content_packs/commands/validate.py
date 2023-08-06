import logging

from itsicli.content_packs.commands.base import WorkspaceCommand
from itsicli.content_packs.validate.registry import VALIDATORS
from itsicli.content_packs.validate.result import Level, result


class ValidateCommand(WorkspaceCommand):

    HELP = 'validates whether a content pack is in a proper state'

    NAME = 'validate'

    @classmethod
    def add_to_parser(cls, parser):
        subparser = parser.add_parser(cls.NAME, help=cls.HELP)
        return subparser

    def run(self, args):
        num_passed = 0
        num_failed = 0

        for validator_class in VALIDATORS:
            validator = validator_class()

            in_progress_text = "\n{}...".format(validator.in_progress_text)
            logging.info(in_progress_text)

            try:
                results = validator.run(
                    home_path=self.home_path
                )
            except Exception as exc:
                logging.exception(exc)

                results = [
                    result(Level.ERROR, 'Yikes, an error occurred. See the above stack trace.')
                ]

            passed = self.print_results(results)
            if passed:
                num_passed += 1
            else:
                num_failed += 1

        logging.info('\nDone with {} passed, and {} failures.'.format(num_passed, num_failed))

    def print_results(self, results):
        passed = True

        for res in results:
            log = self.get_logging_func(res.level)
            log('\t[{}] {}'.format(res.level, res.message))

            if res.level == Level.ERROR:
                passed = False

        return passed

    def get_logging_func(self, level):
        if level == Level.WARNING:
            return logging.warning

        if level == Level.ERROR:
            return logging.error

        return logging.info
