import logging
import shutil

import nox
from pathlib import Path
import os
import sys

# add parent folder to python path so that we can import noxfile_utils.py
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from noxfile_utils import PY27, PY37, PY36, PY35, PY38, session_run, power_session, install_reqs, session_install_any

ALL_PY_VERSIONS = [PY38, PY37, PY36, PY35, PY27]

ENVS = {
    PY27: {"coverage": False, "pkg_specs": {"pip": ">10"}},
    PY35: {"coverage": False, "pkg_specs": {"pip": ">10"}},
    PY36: {"coverage": False, "pkg_specs": {"pip": ">19"}},
    PY37: {"coverage": True, "pkg_specs": {"pip": ">19"}},  # , "pytest-html": "1.9.0"
    PY38: {"coverage": False, "pkg_specs": {"pip": ">19"}},
}


# set the default activated sessions, minimal for CI
nox.options.sessions = ["tests"]  # , "docs", "gh_pages"
nox.options.reuse_existing_virtualenvs = True  # this can be done using -r
nox.options.default_venv_backend = "conda"
# os.environ["NO_COLOR"] = "True"  # nox.options.nocolor = True does not work
# nox.options.verbose = True

nox_logger = logging.getLogger("nox")
nox_logger.setLevel(logging.INFO)


class Folders:
    root = Path(__file__).parent
    runlogs = root / Path(nox.options.envdir or ".nox") / "_runlogs"
    runlogs.mkdir(parents=True, exist_ok=True)
    dist = root / "dist"
    site = root / "site"
    site_reports = site / "reports"
    test_reports = "docs/reports/junit"


@power_session(envs=ENVS, logsdir=Folders.runlogs)
def tests(session, coverage, pkg_specs):
    """Run the test suite, including test reports generation and coverage reports. """

    # uncomment and edit if you wish to uninstall something without deleting the whole env
    # session_run(session, "pip uninstall pytest-asyncio --yes")

    # install all requirements
    install_reqs(session, setup=True, install=True, tests=True, versions_dct=pkg_specs)

    # install self so that it is recognized by pytest
    session_run(session, "pip install -e . --no-deps")

    # finally run all tests
    if not coverage:
        # simple: pytest only
        session_run(session, "python -m pytest -v makefun/tests/")
    else:
        # coverage + junit html reports + badge generation
        install_reqs(session, phase="coverage", phase_reqs=["coverage", "pytest-html", "requests", "xunitparser"],
                     versions_dct=pkg_specs)

        # --coverage + html reports
        session_run(session, "coverage run --source makefun -m "
                             "pytest --junitxml={dst}/junit.xml --html={dst}/report.html"
                             " -v makefun/tests/".format(dst=Folders.test_reports))

        # --generates the badge for the test results and fail build if less than x% tests pass
        nox_logger.info("Generating badge for tests coverage")
        session_run(session, "python ci_tools/generate-junit-badge.py 100 %s" % Folders.test_reports)

        # TODO instead of pushing to codecov we could generate the cov reports ourselves
        # session.run(*"coverage run".split(' '))     # this executes pytest + reporting
        # session.run(*"coverage report".split(' '))  # this shows in terminal + fails under XX%, same than --cov-report term --cov-fail-under=70
        # session.run(*"coverage html".split(' '))    # same than --cov-report html:<dir>
        # session.run(*"coverage xml".split(' '))     # same than --cov-report xml:<file>


@nox.session(python=[PY37])
def docs(session):
    """Generates the doc and serves it on a local http server. You can pass -- build instead or any other mkdocs arg."""

    install_reqs(session, phase="docs", phase_reqs=["mkdocs-material", "mkdocs", "pymdown-extensions", "pygments"])

    if session.posargs:
        # use posargs instead of "serve"
        session_run(session, "mkdocs -f .\docs\mkdocs.yml %s" % " ".join(session.posargs))
    else:
        session_run(session, "mkdocs serve -f .\docs\mkdocs.yml")


@nox.session(python=[PY37])
def publish(session):
    """Deploy the docs on github pages + pushes the coverage. Note: this rebuilds the docs"""

    # check that the doc has been generated with coverage
    if not Folders.site.exists():
        raise ValueError("Documentation has not been built yet. Please run 'nox -s docs'")

    if not Folders.site_reports.exists():
        raise ValueError("Test reports have not been built yet. Please run 'nox -s tests-3.7 docs'")

    # publish the docs
    install_reqs(session, phase="mkdocs", phase_reqs=["mkdocs-material", "mkdocs", "pymdown-extensions", "pygments"])
    session_run(session, "mkdocs gh-deploy -f .\docs\mkdocs.yml")

    # publish the coverage
    install_reqs(session, phase="codecov", phase_reqs=["codecov"])
    session_run(session, "codecov")


@nox.session(python=[PY37])
def release(session):
    """Create a release on github corresponding to the latest tag"""

    # TODO get current tag using setuptools_scm and make sure this is not a dirty/dev one
    from setuptools_scm import get_version
    from setuptools_scm.version import guess_next_dev_version
    version = []
    def my_scheme(version_):
        version.append(version_)
        return guess_next_dev_version(version_)
    current_tag = get_version(".", version_scheme=my_scheme)

    # create the package
    install_reqs(session, phase="setup.py#dist", phase_reqs=["setuptools_scm"])
    if Folders.dist.exists():
        shutil.rmtree(str(Folders.dist))
    session_run(session, "python setup.py sdist bdist_wheel")

    if version[0].dirty or not version[0].exact:
        raise ValueError("You need to execute this action on a clean tag version with no local changes.")

    # publish the package on PyPi
    # keyring set https://upload.pypi.org/legacy/ your-username
    # keyring set https://test.pypi.org/legacy/ your-username
    install_reqs(session, phase="PyPi", phase_reqs=["twine"])
    session_run(session, "twine upload dist/* -u smarie")  # -r testpypi

    # create the github release
    session_run(session, "python ci_tools/github_release.py "
                         "--repo-slug smarie/python-makefun -cf ./docs/changelog.md "
                         "-d https://smarie.github.io/python-makefun/changelog/ {tag}".format(tag=current_tag))


# if __name__ == '__main__':
#     # allow this file to be executable for easy debugging in any IDE
#     nox.run(globals())
