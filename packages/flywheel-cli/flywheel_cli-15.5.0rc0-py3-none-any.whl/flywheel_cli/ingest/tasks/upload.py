"""Provides UploadTask class."""

import logging
import tempfile
import zipfile

import fs
import fs.copy
import fs.path
from flywheel_migration import dcm
from fs.zipfs import ZipFS

from .. import deid
from .. import models as M
from .abstract import Task

log = logging.getLogger(__name__)


class UploadTask(Task):
    """Process ingest item (deidentify, pack, upload)"""

    can_retry = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deid_profile = None

    def _initialize(self):
        if self.ingest_config.de_identify:
            self.deid_profile = deid.load_deid_profile(
                self.ingest_config.deid_profile,
                self.ingest_config.deid_profiles,
            )
            # setup deid logging
            loggers = [deid.DeidLogger(self.db.add)]
            if self.fw.deid_log:
                loggers.append(deid.DeidLogPayloadLogger())

            for file_profile in self.deid_profile.file_profiles:
                file_profile.set_log(loggers)

            self.deid_profile.initialize()
        if self.ingest_config.ignore_unknown_tags:
            dcm.global_ignore_unknown_tags()

    def _run(self):
        item = self.db.get_item(self.task.item_id)
        metadata = {}
        deid_log_payload = None
        container = self.db.get_container(item.container_id)
        if item.type == "packfile":
            log.debug("Creating packfile")
            file_obj, metadata, deid_log_payload = create_packfile(
                self.walker,
                item.safe_filename if item.safe_filename is not None else item.filename,
                item.files,
                item.dir,
                item.context,
                max_tempfile=self.worker_config.max_tempfile,
                compression=self.ingest_config.get_compression_type(),
                deid_profile=self.deid_profile,
                create_deid_log=self.fw.deid_log,
            )
            file_name = metadata["name"]
        else:
            file_obj = self.walker.open(fs.path.join(item.dir, item.files[0]))
            file_name = item.safe_filename or item.filename

        if item.safe_filename or container.sidecar:
            metadata.setdefault("info", {})
            metadata["info"]["source"] = fs.path.join(item.dir, item.filename)

        try:
            if deid_log_payload:
                metadata["deid_log_id"] = self.fw.post_deid_log(deid_log_payload)

            if item.fw_metadata:
                whitelist_keys = [
                    "tags",
                    "info",
                    "classification",
                    "modality",
                    "zip_member_count",
                    "type",
                ]
                filtered = {
                    k: v
                    for k, v in item.fw_metadata.items()
                    if v is not None and k in whitelist_keys
                }
                metadata.update(filtered)

            self.fw.upload(
                container.level.name,
                container.dst_context.id,
                file_name,
                file_obj,
                metadata,
            )
        finally:
            file_obj.close()

    def _on_success(self):
        self.db.update_item_stat(upload_completed=M.ItemStat.upload_completed + 1)
        self.db.start_finalizing()

    def _on_error(self):
        self.db.update_item_stat(upload_completed=M.ItemStat.upload_completed + 1)
        self.db.start_finalizing()


def create_packfile(  # pylint: disable=too-many-arguments
    walker,
    filename,
    files,
    subdir,
    context,
    max_tempfile=0,
    compression=None,
    deid_profile=None,
    create_deid_log=False,
):
    """Create packfile"""

    def get_deid_payload_logger():
        for file_profile in deid_profile.file_profiles:
            if file_profile.log:
                for logger in file_profile.log:
                    if isinstance(logger, deid.DeidLogPayloadLogger):
                        return logger
        return None

    compression = compression or zipfile.ZIP_DEFLATED
    max_spool = max_tempfile * (1024 * 1024)
    if max_spool:
        tmpfile = tempfile.SpooledTemporaryFile(max_size=max_spool)
    else:
        tmpfile = tempfile.TemporaryFile()

    packfile_type = context.packfile.type
    paths = list(map(lambda f_name: fs.path.join(subdir, f_name), files))
    deid_log_payload = None

    flatten = context.packfile.flatten
    with ZipFS(tmpfile, write=True, compression=compression) as dst_fs:
        # Attempt to de-identify using deid_profile first
        processed = False

        if deid_profile:
            processed = deid_profile.process_packfile(
                packfile_type, walker, dst_fs, paths
            )

            if create_deid_log:
                deid_logger = get_deid_payload_logger()
                deid_log_payload = deid_logger.logs.get(paths[0])

        if not processed:
            deid_log_payload = None
            # Otherwise, just copy files into place
            for path in paths:
                # Ensure folder exists
                target_path = path
                if subdir:
                    target_path = walker.remove_prefix(subdir, path)
                if flatten:
                    target_path = fs.path.basename(path)
                folder = fs.path.dirname(target_path)
                dst_fs.makedirs(folder, recreate=True)
                with walker.open(path, "rb") as src_file:
                    dst_fs.upload(target_path, src_file)

    zip_member_count = len(paths)
    log.debug(f"zipped {zip_member_count} files")

    tmpfile.seek(0)

    metadata = {
        "name": filename,
        "zip_member_count": zip_member_count,
        "type": packfile_type,
    }

    return tmpfile, metadata, deid_log_payload
