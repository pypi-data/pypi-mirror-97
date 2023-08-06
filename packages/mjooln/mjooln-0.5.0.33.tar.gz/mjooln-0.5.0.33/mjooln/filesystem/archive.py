import shutil
import zipfile
import gzip

from mjooln.filesystem.file import File


class ArchiveError(Exception):
    pass


class Archive:
    # TODO: Add gz to zip
    # TODO: Add handling of multiple files and folders in archive

    @classmethod
    def is_zip(cls,
               file: File):
        extensions = file.extensions()
        return len(extensions) > 0 and extensions[-1] == 'zip'

    @classmethod
    def zip_to_gz(cls,
                  file: File,
                  delete_source_file: bool = True):

        if not cls.is_zip(file):
            raise ArchiveError(f'File is not zip-file: {file}')

        with zipfile.ZipFile(file, 'r') as zr:
            file_info = zr.filelist
            if len(file_info) > 1:
                raise ArchiveError(f'Multiple files in archive: {file}')
            elif len(file_info) == 0:
                raise ArchiveError(f'No files in archive: {file}')
            file_info = file_info[0]
            file_name = file_info.filename
            if '/' in file_name:
                file_name = file_name.split('/')[-1]
            if '\\' in file_name:
                file_name = file_name.split('\\')[-1]
            gz_file = File.join(file.folder(), file_name + '.gz')
            with zr.open(file_info, 'r') as zf:
                with gzip.open(gz_file, 'w') as gf:
                    shutil.copyfileobj(zf, gf)

        if delete_source_file:
            file.delete()

        return gz_file


