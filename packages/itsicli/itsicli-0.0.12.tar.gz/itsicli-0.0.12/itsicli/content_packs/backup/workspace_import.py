import logging
import shutil

from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from itsicli.content_packs.backup.convert_backup import BackupConverter
from itsicli.content_packs.workspace import root_path
from itsicli.content_packs.files import ContentPackManifest, ContentModel


BACKUP_DIR = 'backup'
ITSI_DIR = 'itsi'


def unarchive(source_zip, dest_dir):
    if source_zip.is_dir():
        backup_dir = Path(dest_dir).joinpath(BACKUP_DIR)
        shutil.copytree(source_zip, backup_dir)
        return backup_dir

    zip_file = ZipFile(source_zip)
    zip_file.extractall(path=dest_dir)

    backup_dir = Path(dest_dir).joinpath(BACKUP_DIR)

    return backup_dir if backup_dir.is_dir() else None


class BackupImporter(object):
    def __init__(self, content_pack_id):
        self.content_pack_id = content_pack_id

    def import_backup(self, backup_path):
        with TemporaryDirectory() as extract_dir:
            backup_dir = unarchive(backup_path, extract_dir)
            if not backup_dir:
                raise Exception('No {}/ directory found in the backup file'.format(BACKUP_DIR))

            prefix = '{}-'.format(self.content_pack_id).lower()
            converter = BackupConverter(prefix)
            models = converter.to_models(backup_dir)

        self.write_models(models)

    def write_models(self, content_models):
        home_path = root_path()

        manifest = ContentPackManifest(home_path)

        for content_type, models in content_models.items():
            for model in models:
                try:
                    content_model = ContentModel(home_path, model)

                    if content_model.path.exists():
                        logging.info('Updating {}'.format(content_model.path))
                    else:
                        logging.info('Creating {}'.format(content_model.path))

                    content_model.write()
                except Exception as exc:
                    logging.error('Failed to create "{}" with id="{}"'.format(content_type, model.get_key()))
                    logging.exception(exc)
                else:
                    manifest.add_content_model(content_model)

        if manifest.path.exists():
            logging.info('Updating manifest file at {}'.format(manifest.path))
        else:
            logging.info('Creating manifest file at {}'.format(manifest.path))

        manifest.write()
