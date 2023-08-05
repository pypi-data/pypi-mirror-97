# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
from __future__ import absolute_import
import mock

import pytest

from module_build_service.common import models
from module_build_service.common.errors import UnprocessableEntity
from module_build_service.common.utils import (import_mmd, load_mmd,
                                               provide_module_stream_version_from_mmd,
                                               provide_module_stream_version_from_timestamp)
from module_build_service.scheduler.db_session import db_session
from tests import read_staged_data, staged_data_filename


@pytest.mark.parametrize("context", ["c1", None])
def test_import_mmd_contexts(context):
    mmd = load_mmd(read_staged_data("formatted_testmodule"))
    mmd.set_context(context)

    xmd = mmd.get_xmd()
    xmd["mbs"]["koji_tag"] = "foo"
    mmd.set_xmd(xmd)

    build, msgs = import_mmd(db_session, mmd)

    mmd_context = build.mmd().get_context()
    if context:
        assert mmd_context == context
        assert build.context == context
    else:
        assert mmd_context == models.DEFAULT_MODULE_CONTEXT
        assert build.context == models.DEFAULT_MODULE_CONTEXT


def test_import_mmd_multiple_dependencies():
    mmd = load_mmd(read_staged_data("formatted_testmodule"))
    mmd.add_dependencies(mmd.get_dependencies()[0].copy())

    expected_error = "The imported module's dependencies list should contain just one element"
    with pytest.raises(UnprocessableEntity) as e:
        import_mmd(db_session, mmd)
        assert str(e.value) == expected_error


def test_import_mmd_no_xmd_buildrequires():
    mmd = load_mmd(read_staged_data("formatted_testmodule"))
    xmd = mmd.get_xmd()
    del xmd["mbs"]["buildrequires"]
    mmd.set_xmd(xmd)

    expected_error = (
        "The imported module buildrequires other modules, but the metadata in the "
        'xmd["mbs"]["buildrequires"] dictionary is missing entries'
    )
    with pytest.raises(UnprocessableEntity) as e:
        import_mmd(db_session, mmd)
        assert str(e.value) == expected_error


def test_import_mmd_minimal_xmd_from_local_repository():
    mmd = load_mmd(read_staged_data("formatted_testmodule"))
    xmd = mmd.get_xmd()
    xmd["mbs"] = {}
    xmd["mbs"]["koji_tag"] = "repofile:///etc/yum.repos.d/fedora-modular.repo"
    xmd["mbs"]["mse"] = True
    xmd["mbs"]["commit"] = "unknown"
    mmd.set_xmd(xmd)

    build, msgs = import_mmd(db_session, mmd, False)
    assert build.name == mmd.get_module_name()


@pytest.mark.parametrize(
    "stream, disttag_marking, error_msg",
    (
        ("f28", None, None),
        ("f28", "fedora28", None),
        ("f-28", "f28", None),
        ("f-28", None, "The stream cannot contain a dash unless disttag_marking is set"),
        ("f28", "f-28", "The disttag_marking cannot contain a dash"),
        ("f-28", "fedora-28", "The disttag_marking cannot contain a dash"),
    ),
)
def test_import_mmd_base_module(stream, disttag_marking, error_msg, require_empty_database):
    mmd = load_mmd(read_staged_data("platform"))
    mmd = mmd.copy(mmd.get_module_name(), stream)

    if disttag_marking:
        xmd = mmd.get_xmd()
        xmd["mbs"]["disttag_marking"] = disttag_marking
        mmd.set_xmd(xmd)

    if error_msg:
        with pytest.raises(UnprocessableEntity, match=error_msg):
            import_mmd(db_session, mmd)
    else:
        import_mmd(db_session, mmd)


def test_import_mmd_remove_dropped_virtual_streams():
    mmd = load_mmd(read_staged_data("formatted_testmodule"))

    # Add some virtual streams
    xmd = mmd.get_xmd()
    xmd["mbs"]["virtual_streams"] = ["f28", "f29", "f30"]
    mmd.set_xmd(xmd)

    # Import mmd into database to simulate the next step to reimport a module
    import_mmd(db_session, mmd)

    # Now, remove some virtual streams from module metadata
    xmd = mmd.get_xmd()
    xmd["mbs"]["virtual_streams"] = ["f28", "f29"]  # Note that, f30 is removed
    mmd.set_xmd(xmd)

    # Test import modulemd again and the f30 should be removed from database.
    module_build, _ = import_mmd(db_session, mmd)

    db_session.refresh(module_build)
    assert ["f28", "f29"] == sorted(item.name for item in module_build.virtual_streams)
    assert 0 == db_session.query(models.VirtualStream).filter_by(name="f30").count()


def test_import_mmd_dont_remove_dropped_virtual_streams_associated_with_other_modules():
    mmd = load_mmd(read_staged_data("formatted_testmodule"))
    # Add some virtual streams to this module metadata
    xmd = mmd.get_xmd()
    xmd["mbs"]["virtual_streams"] = ["f28", "f29", "f30"]
    mmd.set_xmd(xmd)
    import_mmd(db_session, mmd)

    # Import another module which has overlapping virtual streams
    another_mmd = load_mmd(read_staged_data("formatted_testmodule-more-components"))
    # Add some virtual streams to this module metadata
    xmd = another_mmd.get_xmd()
    xmd["mbs"]["virtual_streams"] = ["f29", "f30"]
    another_mmd.set_xmd(xmd)
    another_module_build, _ = import_mmd(
        db_session, another_mmd)

    # Now, remove f30 from mmd
    xmd = mmd.get_xmd()
    xmd["mbs"]["virtual_streams"] = ["f28", "f29"]
    mmd.set_xmd(xmd)

    # Reimport formatted_testmodule again
    module_build, _ = import_mmd(db_session, mmd)

    db_session.refresh(module_build)
    assert ["f28", "f29"] == sorted(item.name for item in module_build.virtual_streams)

    # The overlapped f30 should be still there.
    db_session.refresh(another_module_build)
    assert ["f29", "f30"] == sorted(item.name for item in another_module_build.virtual_streams)


def test_load_mmd_v2():
    """
    Test to check if we can load a v2 packager file.
    """
    mmd = load_mmd(read_staged_data("testmodule_v2.yaml"))

    assert mmd.get_mdversion() == 2

    dep = mmd.get_dependencies()
    btm = dep[0].get_buildtime_modules()
    rtm = dep[0].get_runtime_modules()

    assert len(btm) == 1
    assert len(rtm) == 1
    assert btm[0] == "platform"
    assert rtm[0] == "platform"

    bts = dep[0].get_buildtime_streams(btm[0])
    rts = dep[0].get_runtime_streams(rtm[0])

    assert len(bts) == 1
    assert len(rts) == 1
    assert bts[0] == "f28"
    assert rts[0] == "f28"


def test_load_mmd_v3():
    """
    Test to check if we can load a v3 packager file.
    """
    mmd = load_mmd(read_staged_data("v3/mmd_packager.yaml"))

    assert mmd.get_mdversion() == 3
    contexts = mmd.get_build_config_contexts_as_strv()
    bc1 = mmd.get_build_config(contexts[0])
    assert bc1.get_context() == "CTX1"
    assert bc1.get_platform() == "f28"
    btm1 = bc1.get_buildtime_modules_as_strv()
    rtm1 = bc1.get_runtime_modules_as_strv()
    assert len(btm1) == 0
    assert len(rtm1) == 1
    assert rtm1[0] == "nginx"
    assert bc1.get_runtime_requirement_stream(rtm1[0]) == "1"

    bc2 = mmd.get_build_config(contexts[1])
    assert bc2.get_context() == "CTX2"
    assert bc2.get_platform() == "f29"
    assert not bc2.get_buildtime_modules_as_strv()
    assert not bc2.get_runtime_modules_as_strv()


def test_provide_module_stream_version_from_timestamp():
    ux_timestamp = "1613048427"
    version = provide_module_stream_version_from_timestamp(ux_timestamp)
    assert version == 20210211130027


@mock.patch("module_build_service.common.utils.time")
def test_provide_module_stream_version_from_timestamp_no_params(mock_time):
    mock_time.time.return_value = "1613048427"

    version = provide_module_stream_version_from_timestamp()

    assert version == 20210211130027


def test_provide_module_stream_version_from_mmd_v2():
    expected_version = 20210211130027

    mmd = load_mmd(read_staged_data("testmodule_v2.yaml"))
    mmd.set_version(expected_version)

    version = provide_module_stream_version_from_mmd(mmd)

    assert version == expected_version


@mock.patch("module_build_service.common.utils.time")
def test_provide_module_stream_version_from_mmd_v2_no_set_version(mock_time):
    mock_time.time.return_value = "1613048427"

    mmd = load_mmd(read_staged_data("testmodule_v2.yaml"))

    version = provide_module_stream_version_from_mmd(mmd)

    assert version == 20210211130027


@mock.patch("module_build_service.common.utils.time")
def test_provide_module_stream_version_from_mmd_v3(mock_time):
    mock_time.time.return_value = "1613048427"

    mmd = load_mmd(read_staged_data("v3/mmd_packager.yaml"))

    version = provide_module_stream_version_from_mmd(mmd)

    assert version == 20210211130027


def test_load_mmd_bad_mdversion_raise():
    bad_mdversion_mmd = read_staged_data("v3/mmd_packager.yaml").replace("3", "4")

    with pytest.raises(UnprocessableEntity) as e:
        load_mmd(bad_mdversion_mmd)

    err_msg = e.value.args[0]
    assert "modulemd is invalid" in err_msg
    assert "Invalid mdversion" in err_msg
    assert "modulemd-yaml-error-quark" in err_msg


def test_load_mmd_missing_file_raise():
    bad_path = "../something/something"

    with pytest.raises(UnprocessableEntity) as e:
        load_mmd(bad_path, is_file=True)

    err_msg = e.value.args[0]
    assert "file ../something/something was not found" in err_msg


def test_load_mmd_file_wrong_data_raise():
    bad_file = staged_data_filename("bad.yaml")

    with pytest.raises(UnprocessableEntity) as e:
        load_mmd(bad_file, is_file=True)

    err_msg = e.value.args[0]
    assert "modulemd-yaml-error-quark" in err_msg
    assert "Parse error identifying document type and version" in err_msg
    assert "The modulemd bad.yaml is invalid" in err_msg
