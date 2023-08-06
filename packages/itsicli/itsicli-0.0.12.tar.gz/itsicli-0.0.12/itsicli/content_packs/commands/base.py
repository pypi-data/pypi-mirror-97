from itsicli.content_packs.files import ContentPackConfig, ContentPackManifest, InvalidWorkspace
from itsicli.content_packs.workspace import root_path


def request_input(prompt, validate=lambda x: x):
    while True:
        value = input('{}: '.format(prompt))
        if validate(value):
            break
    return value


class BaseCommand(object):

    @classmethod
    def add_to_parser(cls, parser):
        pass

    def setup_logger(self):
        pass

    def run(self, args):
        raise NotImplementedError


class WorkspaceCommand(BaseCommand):

    def __init__(self):
        super().__init__()

        self.home_path = root_path()

        if not self.home_path:
            raise InvalidWorkspace(
                '\n'.join([
                    "\nUnable to determine a valid workspace from your current path.",
                    "\nMake sure you're in the correct directory, or try running the 'init' command first."
                ])
            )

        self.config = ContentPackConfig(self.home_path)

        if not self.config.id:
            raise InvalidWorkspace(
                '\n'.join([
                    '\nUnable to determine the current content pack id.'
                    "\nMake sure you're in the correct directory, or try running the 'init' command first."
                ])
            )

        self.manifest = ContentPackManifest(self.home_path)
