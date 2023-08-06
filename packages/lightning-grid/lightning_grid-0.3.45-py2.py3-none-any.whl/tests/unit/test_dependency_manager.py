from pathlib import Path
import sys

from pkg_resources import Requirement
import pytest

from grid import dependency_manager
from grid.dependency_manager import _conda2parsed_pypi
from grid.dependency_manager import _get_rule_maps
from grid.dependency_manager import _get_system_deps
from grid.dependency_manager import _guess_valid_name
from grid.dependency_manager import _source2parsed_pypi
from grid.dependency_manager import CondaManager
from grid.dependency_manager import CondaPackage
from grid.dependency_manager import NonComparableError
from grid.dependency_manager import PipManager
from grid.dependency_manager import PipPackage
from grid.dependency_manager import yaml


class TestRule:
    def test_get_rule_map(self):
        rule_labels = {"pip_name_mapping", "conda_name_mapping", "system"}
        rules = _get_rule_maps()

        # verifying rule labels
        assert len(rule_labels.symmetric_difference(rules.keys())) == 0

        # verifying types for each labels
        assert isinstance(rules["pip_name_mapping"], dict)
        key = list(rules["pip_name_mapping"].keys())[0]
        assert isinstance(rules["pip_name_mapping"][key], str)

        assert isinstance(rules["conda_name_mapping"], dict)
        key = list(rules["conda_name_mapping"].keys())[0]
        assert isinstance(rules["conda_name_mapping"][key], str)

        assert isinstance(rules["system"], dict)
        key = list(rules["system"].keys())[0]
        assert isinstance(rules["system"][key], list)

    def test_hyphen_in_rules(self):
        rules = _get_rule_maps()
        for name, value in rules["pip_name_mapping"].items():
            assert "-" not in name
            assert "-" not in value

        for value in rules["conda_name_mapping"].values():
            assert "-" not in value

        for name in rules["system"]:
            assert "-" not in name

    def test_get_system_deps_missing_rule(self):
        # Should return an empty list if a rule is missing
        assert _get_system_deps("dummy_name") == []

    def test_conda2parsed_pypi_missing_rule(self):
        # Should return the same name if a name is missing
        assert _conda2parsed_pypi("dummy_name") == "dummy_name"

    def test_source2parsed_pypi_name_for_missing_rule(self):
        assert _source2parsed_pypi("dummy-name") == "dummy_name"


class TestDifferentRequirementsStringForPIP:
    # these strings are tested in the test cases. Keeping here as
    # documentation
    strings = [
        "dummy-name==0.1.0",
        "dummy@ git+https://github.com/dummy/dummy",
        "dummy>0.1.0,<=1.0.0",
        "dummy-name",
        "pkg==1.4.0;python_version > '3.5'",
        "pkg==1.4.0 -i https://someurl.com/repo",
        "pkg==1.4.0 --index-url https://someurl.com/repo",
        "git+https://github.com/dummy/dummy.git",
        "git+https://github.com/dummy/dummy",
        "https://repo.com/dummy.tar.gz",
        "-e git+https://github.com/dummy/dummy.git",
        ".",
        "/some/path/outside/of/cwd",
        "path/to/wheel.whl",
        "-e file:///path/to/package",
        " pkg==1.4.0",  # string starting with space
        " git+https://github.com/dummy/dummy",  # url starting with space
        "--invalid-option pkg==1.4.0",
        "dummy @ file:///some/local/path",
        "dummy @ /some/local/path",
        "pkg==1.4.0; python_version < '2.7'",
        "pkg==1.4.0;python_version < '2.7'",
        "git+https://github.com/dummy/dummy; python_version < '2.7'",
        "git+https://github.com/dummy/dummy;python_version < '2.7'",  # invalid
        ".==1.4",  # invalid
        "valid/path; python_version < 1.4",
        "valid/path;python_version < 1.4",
        "-e file:///path/to/package; python_version < 1.4",
        "git+https://github.com/dummy/dummy==1.4",  # invalid
        "invalid:requirement$string"
    ]

    def test_name_and_version(self):
        spec = "dummy-name==0.1.0"
        pkg = PipPackage.from_string(spec)
        assert pkg._requirement_obj.url is None
        assert pkg.name == "dummy-name"
        assert pkg.parsed_name == "dummy_name"
        assert pkg._requirement_obj.specs == [("==", "0.1.0")]
        assert pkg._original_string is None
        assert str(pkg) == spec

    def test_name_and_git_url(self):
        spec = "dummy@ git+https://github.com/dummy/dummy"
        pkg = PipPackage.from_string(spec)
        assert str(pkg) == spec
        assert pkg._requirement_obj.url == "git+https://github.com/dummy/dummy"
        # This situation never occurs since our env package won't have version
        # TODO: test the above assumption
        assert PipPackage.from_string("dummy==0.1.0") != pkg  # noqa

    @pytest.mark.skipif(sys.version_info < (3, 8),
                        reason="spec of the format `name@ path` is not "
                        "supported by pkg_resources in 3.7")
    def test_name_and_file_url(self):
        spec = "dummy@ file:///some/local/path"
        pkg = PipPackage.from_string(spec)
        assert str(pkg) == spec
        assert pkg != PipPackage.from_string("dummy")  # noqa

    @pytest.mark.skipif(sys.version_info >= (3, 8),
                        reason="spec of the format `name@ path` is not "
                        "supported by pkg_resources in 3.7")
    def test_name_and_file_url_for_37(self):
        spec = "dummy@ file:///some/local/path"
        pkg = PipPackage.from_string(spec)
        assert str(pkg) == spec
        with pytest.raises(NonComparableError):
            pkg != PipPackage.from_string("dummy")  # noqa

    def test_name_and_path(self, monkeypatch):
        spec = "dummy@ /some/local/path"
        pkg = PipPackage.from_string(spec)
        assert str(pkg) == spec
        assert len(pkg.name) == 5
        monkeypatch.setattr(dependency_manager.Path, "exists", lambda x: True)
        pkg = PipPackage.from_string(spec)
        assert pkg.name == "dummy"

    def test_path_and_specifier(self):
        spec = ".==1.4"
        with pytest.raises(RuntimeError, match="Error while parsing"):
            PipPackage.from_string(spec)

    def test_url_and_specifier(self):
        spec = "git+https://github.com/dummy/dummy==1.4"
        pkg = PipPackage.from_string(spec)
        assert str(pkg) == spec  # noqa
        # Not comparable since pkg._requirement_obj is None
        with pytest.raises(NonComparableError):
            pkg == PipPackage.from_string("dummy==1.4")  # noqa
        with pytest.raises(NonComparableError):
            PipPackage.from_string("dummy==1.4") == pkg  # noqa

    def test_name_with_multiple_specifiers(self):
        spec = "dummy<=1.0.0,>0.1.0"
        pkg = PipPackage.from_string(spec)
        assert str(pkg) == spec

    def test_name_version_and_marker(self):
        spec = "pkg==1.4.0; python_version < '2.7'"
        pkg = PipPackage.from_string(spec)
        assert pkg._requirement_obj == Requirement.parse(spec)
        spec = "pkg==1.4.0;python_version < '2.7'"
        pkg = PipPackage.from_string(spec)
        assert pkg._requirement_obj == Requirement.parse(spec)

    def test_url_and_marker(self):
        spec = "git+https://github.com/dummy/dummy; python_version < '2.7'"
        pkg = PipPackage.from_string(spec)
        assert str(pkg) == spec
        assert pkg.name == "dummy"

        # URL can't parse correctly hence name is uuid
        spec = "git+https://github.com/dummy/dummy;python_version < '2.7'"
        pkg = PipPackage.from_string(spec)
        assert str(pkg) == spec
        # not a valid name but we are ignoring this innocuous error
        assert pkg.name == "dummy;python_version < '2"

    def test_path_and_marker(self, monkeypatch):
        monkeypatch.setattr(dependency_manager.Path, "exists", lambda x: True)
        spec = "valid/path/dummy; python_version < 1.4"
        pkg = PipPackage.from_string(spec)
        assert str(pkg) == spec
        assert pkg.name == "dummy"
        spec = "valid/path/dummy;python_version < 1.4"
        pkg = PipPackage.from_string(spec)
        assert str(pkg) == spec
        assert pkg.name == "dummy"

    def test_just_name(self):
        spec = "dummy-name"
        pkg = PipPackage.from_string(spec)
        assert str(pkg) == spec

    def test_name_and_markers(self):
        spec = 'pkg==1.4.0; python_version > "3.5"'
        pkg = PipPackage.from_string(spec)
        assert str(pkg) == spec
        assert PipPackage.from_string("pkg==1.4.0") == pkg

    def test_name_and_option(self):
        spec = "pkg==1.4.0 -i https://someurl.com/repo"
        pkg = PipPackage.from_string(spec)
        assert pkg.name == "pkg"
        assert str(pkg) == spec
        with pytest.raises(NonComparableError):
            PipPackage.from_string("pkg==100.4.0") == pkg  # noqa

    def test_name_and_long_option(self):
        spec = "pkg==1.4.0 --index-url https://someurl.com/repo"
        pkg = PipPackage.from_string(spec)
        assert pkg.name == "pkg"
        assert str(pkg) == spec
        with pytest.raises(NonComparableError):
            PipPackage.from_string("pkg==100.4.0") == pkg  # noqa

        spec = "pkg==1.4.0 --index-url https://someurl.com/repo -f https://anotherurl.com/"
        pkg = PipPackage.from_string(spec)
        assert pkg.name == "pkg"
        assert str(pkg) == spec

    def test_git_url(self):
        spec = "git+https://github.com/dummy/dummy.git"
        pkg = PipPackage.from_string(spec)
        assert pkg.name == "dummy"
        spec = "git+https://github.com/dummy/dummy"
        pkg = PipPackage.from_string(spec)
        assert pkg.name == "dummy"

    def test_normal_url(self):
        spec = "https://repo.com/dummy.tar.gz"
        pkg = PipPackage.from_string(spec)
        assert pkg.name == "dummy"
        assert str(pkg) == spec

    def test_editable_git_url(self):
        spec = "-e git+https://github.com/dummy/dummy.git"
        with pytest.raises(RuntimeError, match="editable requirements"):
            PipPackage.from_string(spec)

    def test_editable_file_url(self):
        spec = "-e file:///path/to/package"
        with pytest.raises(RuntimeError, match="editable requirements"):
            PipPackage.from_string(spec)

    def test_editable_file_url_with_marker(self):
        spec = "-e file:///path/to/package; python_version < 1.4"
        with pytest.raises(RuntimeError, match="editable requirements"):
            PipPackage.from_string(spec)

    def test_current_directory(self):
        spec = "."
        pkg = PipPackage.from_string(spec)
        assert pkg.name == 'grid-cli'
        with pytest.raises(NonComparableError):
            PipPackage.from_string("grid-cli==0.1") == pkg  # noqa

    def test_outside_directory(self):
        spec = "/some/path/outside/of/cwd"
        with pytest.raises(RuntimeError, match="not resolve"):
            PipPackage.from_string(spec)

    def test_inside_directory(self, monkeypatch):
        spec = "path/to/wheel.whl"
        with pytest.raises(RuntimeError, match="Error while parsing"):
            PipPackage.from_string(spec)
        monkeypatch.setattr(dependency_manager.Path, "exists", lambda x: True)
        pkg = PipPackage.from_string(spec)
        assert str(pkg) == spec
        assert pkg.name == "wheel"

        with pytest.raises(NonComparableError):
            pkg != PipPackage.from_string("pkg")  # noqa

    def test_string_starts_with_space(self):
        spec = " pkg==1.4.0"
        pkg = PipPackage.from_string(spec)
        assert PipPackage.from_string(spec.strip()) == pkg
        spec = " git+https://github.com/dummy/dummy"
        pkg = PipPackage.from_string(spec)
        with pytest.raises(NonComparableError):
            PipPackage.from_string(spec.strip()) == pkg  # noqa

    def test_invalid_option_at_starting(self):
        spec = "--invalid-option pkg==1.4.0"
        with pytest.raises(RuntimeError, match="Error while parsing"):
            PipPackage.from_string(spec)

    def test_invalid_string(self):
        spec = "invalid:requirement$string"
        with pytest.raises(RuntimeError, match="Valid URL schemes"):
            PipPackage.from_string(spec)


class TestPackageContainer:
    def test_pip_package_creation_from_requirement(self):
        req = Requirement.parse("dummy-name==0.1.0")
        pkg = PipPackage.from_requirement(req)
        assert pkg.name == "dummy-name"
        assert pkg.parsed_name == "dummy_name"

    def test_pip_package_from_distribution(self, monkeypatch):
        class DummyDistribution:
            project_name = "dummy-name"
            as_requirement = lambda x: Requirement.parse("dummy-name==0.1.0"
                                                         )  # noqa

        monkeypatch.setattr(dependency_manager, "_is_dist_editable",
                            lambda x: True)
        with pytest.raises(RuntimeError, match="editable installation"):
            PipPackage.from_distribution(DummyDistribution())  # noqa

        monkeypatch.setattr(dependency_manager, "_is_dist_editable",
                            lambda x: False)
        monkeypatch.setattr(dependency_manager, "_get_distribution_url",
                            lambda x: None)
        pkg1 = PipPackage.from_distribution(DummyDistribution())  # noqa
        assert pkg1.name == "dummy-name"
        assert str(pkg1) == "dummy-name==0.1.0"

        monkeypatch.setattr(dependency_manager, "_get_distribution_url",
                            lambda x: "https://github.com/org/repo")
        pkg2 = PipPackage.from_distribution(DummyDistribution())  # noqa
        assert str(pkg2) == "dummy-name@ https://github.com/org/repo"
        # TODO: self._requirement_obj == other._requirement_obj is
        #  True but it shouldn't be
        assert pkg1 == pkg2  # noqa

    def test_pip_package_equality(self):
        # More granular equality checks are done in
        # TestDifferentRequirementsStringForPIP
        pkg1 = PipPackage.from_string("dummy-name==0.1.0")
        pkg2 = PipPackage.from_string("dummy-name==0.2.0")
        assert pkg1 != pkg2

        # Pip package and conda package
        pkg2 = CondaPackage.from_string("dummy=hash=version")
        assert pkg1 != pkg2

        # Underscore
        pkg1 = PipPackage.from_string("dummy-name")
        pkg2 = PipPackage.from_string("dummy_name")
        assert pkg1 == pkg2

        # version inclusion
        pkg1 = PipPackage.from_string("dummy-name>1.0,<2.0")
        pkg2 = PipPackage.from_string("dummy_name==1.5")
        assert pkg1 == pkg2
        assert pkg2 == pkg1

        # Different version
        pkg3 = PipPackage.from_string("dummy_name==2.5")
        assert pkg1 != pkg3

        pkg4 = PipPackage.from_string("dummy-name>1.5,<2.0")
        assert pkg1 != pkg4

        pkg1 = PipPackage.from_string("dummy-name==2.0")
        pkg2 = PipPackage.from_string("dummy-name")
        pkg3 = PipPackage.from_string("dummy-name>=")
        # first specifier has empty version
        pkg4 = PipPackage.from_string("dummy-name>=, <3.0")
        assert pkg1 != pkg2
        assert pkg1 != pkg3
        assert pkg1 == pkg4

        # different parse_name - should never happen in real world
        pkg1 = PipPackage.from_string("dummy-name==2.0")
        pkg2 = PipPackage.from_string("dummy-name==2.0")
        pkg2.parsed_name = "wrong_parsed_name"
        with pytest.raises(NonComparableError):
            pkg1 != pkg2  # noqa

    def test_conda_package_creation(self):
        pkg = CondaPackage(name="dummy-name", version="0.1.0", build="py1000")
        assert pkg.parsed_name == "dummy_name"

        pkg = CondaPackage.from_string("dummy-name=0.1.0=py1000")
        assert pkg.build == "py1000"

        pkg = CondaPackage.from_string("dummy==0.1")
        assert pkg.name == "dummy"
        assert pkg.build is None
        assert pkg.version == "0.1"

        pkg = CondaPackage.from_string("dummy==0.1==py1000")
        assert pkg.name == "dummy"
        assert pkg.build == "py1000"
        assert pkg.version == "0.1"

        pkg = CondaPackage.from_string("dummy==0.1=py1000")
        assert pkg.name == "dummy"
        assert pkg.build == "py1000"
        assert pkg.version == "0.1"

        pkg = CondaPackage.from_string("dummy=0.1.0")
        assert pkg.name == "dummy"
        assert pkg.build is None
        assert pkg.version == "0.1.0"

        pkg = CondaPackage.from_string("dummy")
        assert pkg.name == "dummy"
        assert pkg.version is None
        assert pkg.build is None

        with pytest.raises(RuntimeError, match="ParsingError"):
            CondaPackage.from_string("dummy=0.1.0=py1000=fake")

    def test_conda_package_to_string(self):
        pkg = CondaPackage(name="dummy-name", version="0.1.0", build="py1000")
        assert str(pkg) == "dummy-name=0.1.0=py1000"
        pkg = CondaPackage(name="dummy-name", version=None, build=None)
        assert str(pkg) == "dummy-name"
        pkg = CondaPackage(name="dummy-name", version="0.1.0", build=None)
        assert str(pkg) == "dummy-name=0.1.0"

    def test_conda_package_equality(self):
        pkg1 = CondaPackage(name="dummy-name", version="0.1.0", build="py100")
        pkg2 = CondaPackage(name="dummy-name", version="0.1.0", build="py100")
        pkg3 = PipPackage.from_string("dummy-name")
        assert pkg1 == pkg2
        assert pkg1 != pkg3

        pkg1.build = "another build"
        assert pkg1 == pkg2  # still equal - build doesn't have any effect

        pkg1.version = "0.2.0"
        assert pkg1 != pkg2


class TestDepsManagerBaseClass:
    def test_read_file_deps_with_no_requirement_file(self, monkeypatch):
        monkeypatch.setattr(PipManager, "_setup", lambda x: None)
        pm = PipManager()
        pm.req_file = None
        monkeypatch.setattr(pm, "req_file", Path("filedoesnotexist"))
        assert pm._read_file_deps() == {}

    def test_get_missing(self, monkeypatch):
        source_deps = ["pkg_a", "pkg_b", "pkg_c"]

        def test_setup(self):
            self.env_deps = {
                "pkg_z": object(),
                "pkg_a": object(),
                "pkg_b": object()
            }
            self.file_deps = {
                "pkg_b": object(),
                "pkg_c": object(),
                "pkg_d": object()
            }
            self._source_deps_list = source_deps

        # No missing keys
        monkeypatch.setattr(PipManager, "_setup", test_setup)
        pm = PipManager()
        assert set() == pm.get_missing()

        # adding missing keys
        source_deps.append("pkg_missing")
        assert {"pkg_missing"} == pm.get_missing()

    def test_has_change(self, monkeypatch):
        source_deps = ["pkg_a", "pkg_b"]

        class DummyFile:
            def __init__(self):
                self.exists = lambda: False

        dummyfile = DummyFile()

        def test_setup(self):
            self.req_file = dummyfile
            self.env_deps = {
                "pkg_z": object(),
                "pkg_a": object(),
                "pkg_b": object()
            }
            self.file_deps = {
                "pkg_b": object(),
                "pkg_c": object(),
                "pkg_d": object()
            }
            self._source_deps_list = source_deps

        # No requirement file exist
        monkeypatch.setattr(PipManager, "_setup", test_setup)
        pm = PipManager()
        assert pm.has_change is True

        # requirement file exist but keys from source is not present in file deps
        dummyfile.exists = lambda: True
        assert pm.has_change is True

        # keys from source is not in env deps which is OK (pkg_d)
        # env deps package != file deps package (pkg_b)
        source_deps.clear()
        source_deps.append("pkg_d")
        source_deps.append("pkg_b")
        assert pm.has_change is True

    def test_collate_final(self, monkeypatch):
        source_deps = ["pkg_a", "pkg_b", "pkg_c", "pkg_d"]
        obja, objb, objc, objd = object(), object(), object(), object()

        def test_setup(self):
            self.env_deps = {"pkg_d": objd}
            self.file_deps = {"pkg_c": objc, "pkg_b": objb, "pkg_a": obja}
            self._source_deps_list = source_deps

        # Adding missing deps & keeping the order of elements in file deps
        monkeypatch.setattr(PipManager, "_setup", test_setup)
        pm = PipManager()
        assert pm.collate_final() == [objc, objb, obja, objd]

        # Updating deps from env if env deps is not same as file deps
        newobjc = object()
        pm.env_deps = {"pkg_d": objd, "pkg_c": newobjc}
        assert pm.collate_final() == [newobjc, objb, obja, objd]

    def test_write_config(self, monkeypatch):
        source_deps = ["pkg_a", "pkg_b", "pkg_c", "pkg_d"]
        # monkeypatching safedump to ease testing
        yamlout = []
        monkeypatch.setattr(yaml, "safe_dump", lambda c, f: yamlout.append(
            (c, f)))

        def test_setup(self):
            self._source_deps_list = source_deps

        # No system deps found
        monkeypatch.setattr(PipManager, "_setup", test_setup)
        pm = PipManager()
        assert pm.write_config({"compute": {}}) is None

        # Empty config
        monkeypatch.setattr(dependency_manager, "_get_system_deps",
                            lambda x: [x])
        with pytest.raises(KeyError, match="compute"):
            pm.write_config({})

        # multiple system deps
        pm.write_config({"compute": {}})
        assert yamlout[0][0] == {
            'compute': {
                'actions': {
                    'on_image_build':
                    ['apt install -y pkg_a pkg_b pkg_c pkg_d']
                }
            }
        }

        configfile = yamlout[0][1]
        configfile.close()
        Path(configfile.name).unlink()

        yamlout.clear()
        pm.write_config({"compute": {"actions": {"on_image_build": []}}})
        assert yamlout[0][0] == {
            'compute': {
                'actions': {
                    'on_image_build':
                    ['apt install -y pkg_a pkg_b pkg_c pkg_d']
                }
            }
        }

        configfile = yamlout[0][1]
        configfile.close()
        Path(configfile.name).unlink()


class TestPipManager:
    def test_read_file_deps_success(self, monkeypatch):
        class DummyFile:
            def __init__(self):
                self.exists = lambda: True
                self.read_text = lambda: "pkg-a==0.2\npkg-b"

        monkeypatch.setattr(PipManager, "_setup", lambda x: None)
        pm = PipManager()
        pm.req_file = None
        dummyfile = DummyFile()
        monkeypatch.setattr(pm, "req_file", dummyfile)
        final = {
            "pkg_a": PipPackage.from_string("pkg-a==0.2"),
            "pkg_b": PipPackage.from_string("pkg-b")
        }
        assert pm._read_file_deps() == final

    def test_read_file_deps_with_invalid_file(self, monkeypatch):
        class DummyFile:
            def __init__(self):
                self.exists = lambda: True
                self.read_text = lambda: "channel:  - pytorch\n"

        monkeypatch.setattr(PipManager, "_setup", lambda x: None)
        pm = PipManager()
        pm.req_file = None
        dummyfile = DummyFile()
        monkeypatch.setattr(pm, "req_file", dummyfile)
        with pytest.raises(RuntimeError, match="Valid URL schemes"):
            pm._read_file_deps()

    def test_get_default_file(self, monkeypatch):
        monkeypatch.setattr(PipManager, "_setup", lambda x: None)
        pm = PipManager()
        assert Path("requirements.txt") == pm._get_default_req_file()


class TestCondaManager:
    def test_read_file_deps_success(self, monkeypatch):
        class DummyFile:
            def __init__(self):
                self.exists = lambda: True
                self.read_text = lambda: 'channels:\n  - pytorch\n  - defaults\ndependencies:\n  - pkg-b=20.1.0=py38\n  - pkg-a=1.10=py_0\n'

        monkeypatch.setattr(CondaManager, "_setup", lambda x: None)
        cm = CondaManager()
        cm.req_file = None
        dummyfile = DummyFile()
        monkeypatch.setattr(cm, "req_file", dummyfile)
        final = {
            "pkg_b": CondaPackage.from_string("pkg-b=20.1.0=py38"),
            "pkg_a": CondaPackage.from_string("pkg-a=1.10=py_0")
        }
        assert cm._read_file_deps() == final

    def test_read_file_deps_with_invalid_file(self, monkeypatch):
        class DummyFile:
            def __init__(self):
                self.exists = lambda: True
                self.read_text = lambda: "pkg-a==0.2\npkg-b"

        monkeypatch.setattr(CondaManager, "_setup", lambda x: None)
        pm = CondaManager()
        pm.req_file = None
        dummyfile = DummyFile()
        monkeypatch.setattr(pm, "req_file", dummyfile)
        with pytest.raises(RuntimeError):
            # generic exception since different python version raises
            # different exception
            pm._read_file_deps()

    def test_get_default_file(self, monkeypatch):
        monkeypatch.setattr(CondaManager, "_setup", lambda x: None)
        pm = CondaManager()
        assert Path("environment.yml") == pm._get_default_req_file()


def test_get_valid_stem():
    with pytest.raises(RuntimeError, match="not portable"):
        _guess_valid_name("file://path/to/dir")
    with pytest.raises(RuntimeError, match="Valid URL schemes are"):
        _guess_valid_name("invalid://path/to/dir")
    with pytest.raises(RuntimeError, match="Error while parsing"):
        _guess_valid_name("invalid;path--with==random+char#%^")
    assert "path" == _guess_valid_name("https://github.com/org/path@branch")
    assert "path" == _guess_valid_name("https://github.com/org/path")
    assert "name" == _guess_valid_name("name @ path")
