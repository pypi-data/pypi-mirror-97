# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
from __future__ import absolute_import
from datetime import datetime
from functools import partial
import os
import time

from gi.repository.GLib import Error as ModuleMDError
from six import string_types, text_type

from module_build_service.common import conf, log
from module_build_service.common.errors import UnprocessableEntity
from module_build_service.common.modulemd import Modulemd


def to_text_type(s):
    """
    Converts `s` to `text_type`. In case it fails, returns `s`.
    """
    try:
        return text_type(s, "utf-8")
    except TypeError:
        return s


def load_mmd(yaml, is_file=False):
    if not yaml:
        raise UnprocessableEntity('The input modulemd was empty')

    try:
        if is_file:
            mmd = Modulemd.read_packager_file(yaml)
        else:
            mmd = Modulemd.read_packager_string(to_text_type(yaml))

        mmd_version = mmd.get_mdversion()

        # both legacy packager v1 and stream v1 are directly upgraded to v2
        if mmd_version == 1:
            mmd = mmd.upgrade(2)

    except ModuleMDError as e:
        error = None
        if is_file:
            if os.path.exists(yaml):
                with open(yaml, "rt") as yaml_hdl:
                    log.debug("The modulemd file '%s' failed to load:\n%s",
                              yaml,
                              yaml_hdl.read())
            else:
                error = "The modulemd file {} was not found.".format(yaml)
                log.error("The modulemd file %s was not found.", yaml)

        if not error:
            if is_file:
                error = ("The modulemd {} is invalid. The error was:\n'{}'\nPlease verify the"
                         " syntax is correct.").format(os.path.basename(yaml), str(e))
            else:
                error = ("The modulemd is invalid. The error was:\n'{}'\nPlease verify the"
                         " syntax is correct.").format(str(e))

        log.exception(error)
        raise UnprocessableEntity(error)

    return mmd


load_mmd_file = partial(load_mmd, is_file=True)


def import_mmd(db_session, mmd, check_buildrequires=True):
    """
    Imports new module build defined by `mmd` to MBS database using `session`.
    If it already exists, it is updated.

    The ModuleBuild.koji_tag is set according to xmd['mbs]['koji_tag'].
    The ModuleBuild.state is set to "ready".
    The ModuleBuild.rebuild_strategy is set to "all".
    The ModuleBuild.owner is set to "mbs_import".

    :param db_session: SQLAlchemy session object.
    :param mmd: module metadata being imported into database.
    :type mmd: Modulemd.ModuleStream
    :param bool check_buildrequires: When True, checks that the buildrequires defined in the MMD
        have matching records in the `mmd["xmd"]["mbs"]["buildrequires"]` and also fills in
        the `ModuleBuild.buildrequires` according to this data.
    :return: module build (ModuleBuild),
             log messages collected during import (list)
    :rtype: tuple
    """
    from module_build_service.common import models

    xmd = mmd.get_xmd()
    # Set some defaults in xmd["mbs"] if they're not provided by the user
    if "mbs" not in xmd:
        xmd["mbs"] = {"mse": True}

    if not mmd.get_context():
        mmd.set_context(models.DEFAULT_MODULE_CONTEXT)

    # NSVC is used for logging purpose later.
    nsvc = mmd.get_nsvc()
    if nsvc is None:
        msg = "Both the name and stream must be set for the modulemd being imported."
        log.error(msg)
        raise UnprocessableEntity(msg)

    name = mmd.get_module_name()
    stream = mmd.get_stream_name()
    version = str(mmd.get_version())
    context = mmd.get_context()

    xmd_mbs = xmd["mbs"]

    disttag_marking = xmd_mbs.get("disttag_marking")

    # If it is a base module, then make sure the value that will be used in the RPM disttags
    # doesn't contain a dash since a dash isn't allowed in the release field of the NVR
    if name in conf.base_module_names:
        if disttag_marking and "-" in disttag_marking:
            msg = "The disttag_marking cannot contain a dash"
            log.error(msg)
            raise UnprocessableEntity(msg)
        if not disttag_marking and "-" in stream:
            msg = "The stream cannot contain a dash unless disttag_marking is set"
            log.error(msg)
            raise UnprocessableEntity(msg)

    virtual_streams = xmd_mbs.get("virtual_streams", [])

    # Verify that the virtual streams are the correct type
    if virtual_streams and (
        not isinstance(virtual_streams, list)
        or any(not isinstance(vs, string_types) for vs in virtual_streams)
    ):
        msg = "The virtual streams must be a list of strings"
        log.error(msg)
        raise UnprocessableEntity(msg)

    if check_buildrequires:
        deps = mmd.get_dependencies()
        if len(deps) > 1:
            raise UnprocessableEntity(
                "The imported module's dependencies list should contain just one element")

        if "buildrequires" not in xmd_mbs:
            # Always set buildrequires if it is not there, because
            # get_buildrequired_base_modules requires xmd/mbs/buildrequires exists.
            xmd_mbs["buildrequires"] = {}
            mmd.set_xmd(xmd)

        if len(deps) > 0:
            brs = set(deps[0].get_buildtime_modules())
            xmd_brs = set(xmd_mbs["buildrequires"].keys())
            if brs - xmd_brs:
                raise UnprocessableEntity(
                    "The imported module buildrequires other modules, but the metadata in the "
                    'xmd["mbs"]["buildrequires"] dictionary is missing entries'
                )

    if "koji_tag" not in xmd_mbs:
        log.warning("'koji_tag' is not set in xmd['mbs'] for module {}".format(nsvc))
        log.warning("koji_tag will be set to None for imported module build.")

    # Log messages collected during import
    msgs = []

    # Get the ModuleBuild from DB.
    build = models.ModuleBuild.get_build_from_nsvc(db_session, name, stream, version, context)
    if build:
        msg = "Updating existing module build {}.".format(nsvc)
        log.info(msg)
        msgs.append(msg)
    else:
        build = models.ModuleBuild()
        db_session.add(build)

    build.name = name
    build.stream = stream
    build.version = version
    build.koji_tag = xmd_mbs.get("koji_tag")
    build.state = models.BUILD_STATES["ready"]
    build.modulemd = mmd_to_str(mmd)
    build.context = context
    build.owner = "mbs_import"
    build.rebuild_strategy = "all"
    now = datetime.utcnow()
    build.time_submitted = now
    build.time_modified = now
    build.time_completed = now
    if build.name in conf.base_module_names:
        build.stream_version = models.ModuleBuild.get_stream_version(stream)

    # Record the base modules this module buildrequires
    if check_buildrequires:
        for base_module in build.get_buildrequired_base_modules(db_session):
            if base_module not in build.buildrequires:
                build.buildrequires.append(base_module)

    build.update_virtual_streams(db_session, virtual_streams)

    db_session.commit()

    msg = "Module {} imported".format(nsvc)
    log.info(msg)
    msgs.append(msg)

    return build, msgs


def mmd_to_str(mmd):
    """
    Helper method to convert a Modulemd.ModuleStream object to a YAML string.

    :param Modulemd.ModuleStream mmd: the modulemd to convert
    :return: the YAML string of the modulemd
    :rtype: str
    """
    index = Modulemd.ModuleIndex()
    index.add_module_stream(mmd)
    return to_text_type(index.dump_to_string())


def provide_module_stream_version_from_timestamp(timestamp=None):
    """
    Provides a module stream version from a unix timestamp. If the timestamp is not defined
    it will will generate one..

    :param timestamp: modulemd object representing module metadata.
    :type mmd: Modulemd.Module
    :return: module stream version
    :rtype: int
    """
    if timestamp:
        dt = datetime.utcfromtimestamp(int(timestamp))
    else:
        dt = datetime.utcfromtimestamp(int(time.time()))

    return int(dt.strftime("%Y%m%d%H%M%S"))


def provide_module_stream_version_from_mmd(mmd):
    """
    Provides a module stream version for a module stream. If a mmd v2 already contains
    a version it will return it else it will generate a new one.

    :param mmd: modulemd object representing module metadata.
    :type mmd: Modulemd.Module
    :return: module stream version
    :rtype: int
    """

    if mmd.get_mdversion() == 2 and mmd.get_version():
        return mmd.get_version()

    dt = datetime.utcfromtimestamp(int(time.time()))
    return int(dt.strftime("%Y%m%d%H%M%S"))
