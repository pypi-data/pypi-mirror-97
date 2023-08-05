#!/usr/bin/env python3

"""File indexing methods."""

import os
from mimetypes import guess_type
from pathlib import Path
from shutil import copyfile

import filetype
from PIL import Image
from tolkein import tofetch
from tolkein import tofile
from tolkein import tolog

from .analysis import index_template as analysis_index_template
from .es_functions import document_by_id
from .hub import index_templator

LOGGER = tolog.logger(__name__)


def index_template(taxonomy_name, opts):
    """Index template (includes name, mapping and types)."""
    parts = ["file", taxonomy_name, opts["hub-name"], opts["hub-version"]]
    template = index_templator(parts, opts)
    return template


def force_copy(sourcename, destname, symlink=True):
    """Create or replace a symlink to a file."""
    localfile = Path(destname)
    os.makedirs(Path(destname).parent, exist_ok=True)
    try:
        localfile.unlink()
    except FileNotFoundError:
        pass
    if symlink:
        localfile.symlink_to(Path(sourcename))
    else:
        copyfile(Path(sourcename), localfile)


def process_image_file(infile, filename, opts, *, dest_dir="./", attrs=None):
    """Process an image file for indexing."""
    if attrs is None:
        attrs = {}
    filepath = Path(filename)
    dimensions = (100, 100)
    thumbname = "%s.thm%s" % (filepath.stem, filepath.suffix)
    with Image.open(infile) as im:
        attrs.update(
            {
                "thumb_name": thumbname,
                "format": im.format,
                "size_pixels": "%sx%s" % (im.width, im.height),
            }
        )
        if filename != thumbname:
            try:
                im.thumbnail(dimensions)
                im.save("%s/%s/%s" % (opts["hub-path"], dest_dir, thumbname))
            except OSError:
                LOGGER.warn("Cannot create thumbnail for '%s'", infile)
        attrs.update()
    return attrs


def set_file_meta_defaults(opts):
    """Set default values for file metadata."""
    defaults = {}
    for key in {
        "taxon-id",
        "assembly-id",
        "analysis-id",
        "file-title",
        "file-description",
    }:
        value = opts.get(key, False)
        if value:
            defaults.update({key.replace("file-", "").replace("-", "_"): value})
    return defaults


def process_file(
    infile,
    opts,
    *,
    file_template=None,
    analysis_template=None,
    filename=None,
    meta=None,
    local="symlink"
):
    """Process a file for indexing."""
    filepath = Path(infile)
    if filename is None:
        filename = filepath.name
    if meta is None:
        meta = {}
    attrs = {
        "name": filename,
        "size_bytes": os.path.getsize(infile),
        **set_file_meta_defaults(opts),
        **meta,
    }
    try:
        dest_dir = str(filepath.parent.relative_to(opts["hub-path"]))
    except ValueError:
        dest_dir = "files"
        dest_dir += "/taxon-" + attrs.get("taxon_id", "all")
        dest_dir += "/assembly-" + attrs.get("assembly_id", "all")
        dest_dir += "/analysis-" + attrs.get("analysis_id", "all")
        localname = "%s/%s/%s" % (opts["hub-path"], dest_dir, filename)
        if local == "symlink":
            force_copy(infile, localname)
        elif local == "copy":
            force_copy(infile, localname, False)
    attrs.update({"location": dest_dir})
    kind = filetype.guess(infile)
    if kind is not None:
        attrs.update({"extension": kind.extension, "mime_type": kind.mime})
        if filetype.is_image(infile):
            process_image_file(infile, filename, opts, dest_dir=dest_dir, attrs=attrs)
    else:
        attrs.update({"extension": filepath.suffix.replace(".", "")})
        attrs.update({"mime_type": guess_type(filepath)[0]})
    file_props = file_template["mapping"]["mappings"]["properties"].keys()
    analysis_props = analysis_template["mapping"]["mappings"]["properties"].keys()
    file_attrs = {}
    analysis_attrs = {}
    # split attrs into 2 sets for indexing
    for key, value in attrs.items():
        if key in file_props:
            file_attrs.update({key: value})
            if key == "analysis_id":
                analysis_attrs.update({key: value})
        elif key in analysis_props:
            analysis_attrs.update({key: value})
        elif key == "analysis":
            for sub_key, sub_value in value.items():
                if sub_key in analysis_props:
                    analysis_attrs.update({sub_key: sub_value})
    return file_attrs, analysis_attrs


def index_files(es, files, taxonomy_name, opts):
    """Index files."""
    file_template = index_template(taxonomy_name, opts)
    analysis_template = analysis_index_template(taxonomy_name, opts)
    for infile in files:
        LOGGER.info("Indexing %s", infile)
        p = Path(infile)
        if p.is_dir():
            LOGGER.warn(
                "Argument to --file must be a valid file path. '%s' is a directory",
                infile,
            )
            continue
        file_attrs, analysis_attrs = process_file(
            infile,
            opts,
            file_template=file_template,
            analysis_template=analysis_template,
        )


def index_metadata(es, file, taxonomy_name, opts):
    """Index file metadata."""
    data = tofile.load_yaml(file)
    file_template = index_template(taxonomy_name, opts)
    analysis_template = analysis_index_template(taxonomy_name, opts)
    if data is None:
        LOGGER.warn("Unable to load file metadata from '%s'" % file)
        return
    for meta in data:
        local = "symlink"
        if "path" in meta:
            if meta["path"].startswith("~"):
                infile = os.path.expanduser(meta["path"])
            else:
                infile = meta["path"]
            del meta["path"]
        elif "url" in meta:
            infile = tofetch.fetch_tmp_file(meta["url"])
            local = None
        elif "name" in meta:
            infile = meta["name"]
        else:
            LOGGER.warn("Found a record with no associated file in '%s'" % file)
        if "name" in meta:
            filename = meta["name"]
            del meta["name"]
        else:
            filename = None
        local = meta.pop("local", local)
        file_attrs, analysis_attrs = process_file(
            infile,
            opts,
            file_template=file_template,
            analysis_template=analysis_template,
            filename=filename,
            meta=meta,
            local=local,
        )
        # TODO: #30 check taxon_id(s) and assembly_id(s) exist in database
        # Fetch existing analysis entry if available
        res = document_by_id(
            es,
            "analysis-%s" % analysis_attrs["analysis_id"],
            analysis_template["index_name"],
        )
        print(res)
        # Increment file counter
        # Create/update index entry
