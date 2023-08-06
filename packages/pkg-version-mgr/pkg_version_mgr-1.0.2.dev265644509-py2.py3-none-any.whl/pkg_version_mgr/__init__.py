"""Python package version mgr."""
from __future__ import print_function
# noinspection PyPackageRequirements
from future.utils import raise_from
import os

SUFFIX = 'PKG_VER_SUFFIX'
"""Environment variable to specify the value for the `suffix`"""

SUFFIX_NUM = 'PKG_VER_SUFFIX_NUM'
"""Environment variable to specify the value for the `suffix_num`"""

PIPELINE_ID_GL = 'CI_PIPELINE_ID'
"""Environment variable for Gitlab pipeline ID"""

PIPELINE_ID_GH = 'GITHUB_RUN_NUMBER'
"""Environment variable for GitHub pipeline repository workflow"""

MAJOR = 'PKG_VER_MAJOR'
"""Environment variable to specify the value for the `major`"""

MINOR = 'PKG_VER_MINOR'
"""Environment variable to specify the value for the `minor`"""

MICRO = 'PKG_VER_MICRO'
"""Environment variable to specify the value for the `micro`"""

SKIP_UPDATE_VERSION = 'PKG_VER_SKIP_TARGET_MODULE'
"""Environment variable to signal to skip updating the target_module (for dev/local builds)"""


class InvalidParameterError(Exception):
    """Raised on invalid parameters to :class:`PkgVersionMgr`."""

    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return "InvalidParameterError: {}".format(self.__str__())


class CustomFuncError(Exception):
    """On exception by optional custom func parameter."""

    def __init__(self):
        pass


class PkgVersionMgr(object):
    """For managing the build version of the package.

    This will manage the <major>.<minor>.<micro>.<suffix><suffix_num> version for setup builds
    with an eye on CI pipelines (by default, Gitlab).

    **Environment Vars Supported:**

    * CI_COMMIT_TAG: Gitlab CI commit tag
    * CI_PIPELINE_ID: Gitlab CI pipeline ID

    To use major.minor version only, set `micro=None`. The ``suffix`` parameter should follow
    the `"pip" conventions <https://www.python.org/dev/peps/pep-0440/>`_.

    **Usage Example**

    See this project's "setup.py" for a live example.

    .. code-block:: python

        from pkg_version_mgr import PkgVersionMgr

        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

        import pkg_version_mgr.version as version
        from pkg_version_mgr import PkgVersionMgr

        version_mgr = PkgVersionMgr(major=0, minor=1, micro=0, suffix='dev')

        # The setup.cfg contains metadata keywords
        setup(
            version=version_mgr.version(target_module=version),
        )

    .. seealso::

        * https://www.python.org/dev/peps/pep-0440/
        * https://packaging.python.org/guides/single-sourcing-package-version/

    """

    FMT_PYTHON = 'python'
    """Write as Python with format: __version__ = <version>"""
    FMT_BASH = 'bash'
    """Write as bash variable with format: VERSION=<version>"""
    FMT_STR = 'str'
    """Write just the version string to a target file"""
    FMT_FUNCTION = 'function'
    """To call a user-supplied function to write version."""

    def __init__(self,
                 major,
                 minor,
                 micro=None,
                 suffix=SUFFIX,
                 suffix_num=SUFFIX_NUM,
                 pipeline_id_name='CI_PIPELINE_ID',
                 commit_tag_name='CI_COMMIT_TAG'):
        """Construct.

        :param major: Major build version or :py:data:`MAJOR`
        :param minor: Minor build version or :py:data:`MINOR`
        :param micro: Optional micro/patch version or :py:data:`MICRO`
        :param suffix: The suffix str prefix. (i.e., "a" or "dev") or SUFFIX
        :param suffix_num: The suffix number, or SUFFIX_NUM
        :param pipeline_id_name: The env variable for the pipeline ID.
        :param commit_tag_name: The env variable name for commit tag.
        """
        self.pipeline_id_name = pipeline_id_name
        self.commit_tag_name = commit_tag_name

        self.major = self._parm_env_var_value(major)
        self.minor = self._parm_env_var_value(minor)
        self.micro = self._parm_env_var_value(micro)
        self.suffix = self._parm_env_var_value(suffix)
        self.suffix_num = self._parm_env_var_value(suffix_num)

    def _parm_env_var_value(self, parm, default=None):
        """Return environment variable value for build vars or default.

        :param parm:
        :param default:
        :return:
        """
        if parm in [SUFFIX,
                    SUFFIX_NUM,
                    self.pipeline_id_name,
                    self.commit_tag_name,
                    MAJOR,
                    MINOR,
                    MICRO]:
            return os.environ.get(parm) or default

        # if parm == SUFFIX:
        #     return os.environ.get(SUFFIX) or default
        #
        # if parm == SUFFIX_NUM:
        #     return os.environ.get(SUFFIX_NUM) or default
        #
        # if parm == self.pipeline_id_name:
        #     return os.environ.get(self.pipeline_id_name) or default
        #
        # if parm == self.commit_tag_name:
        #     return os.environ.get(self.commit_tag_name) or default

        return str(parm) if parm is not None else default

    @staticmethod
    def _parm_str_value(parm, default=None):
        """To default a str or int parm to None if not supplied

        :return: String value
        :rtype: str
        """
        return str(parm) if parm is not None else default

    def version(self,
                target_file=None,
                target_module=None,
                target_fmt=FMT_PYTHON,
                custom_func=None):
        """Get the version and optionally written to a target file.

        This will use the member variables as well as the CI environment variables to calculate the
        version string for building our wheels, and optionally writes the version to a target
        file or module.

        **Write Version File(s)**

        This method can optionally write the calculated version to a file and call a user-supplied
        custom function. Any, or all, of the parameters `target_file`, `target_module`
        and `custom_func` may be supplied. All that are supplied will be handled.

        The `target_fmt` specifies the format for `target_file`.

        The intention of this is primarily to include the updated version file for inclusion in the
        built wheel.

        *target_file*

        This is a full path/name of a file to write the version to. This uses `target_fmt` to
        indicate the type of file to write.

        To write to a Python module file, supply only the `target_module` parameter.

        *target_module*

        WARNING: This will regenerate the module file.

        This is a module reference to write/update the version to. The referenced Python module
        will be re-generated with just the lines:

        .. code-block:: python

            # Auto-generated by pkg_version_mgr.
            __version__ = "1.2.3.a1"

        *target_fmt*

        This is one of the supported "FMT\\_" strings and specifies the output format of the
        of the file specified in ``target_file``.

        FMT_PYTHON: Generate a python module with "__version__ = x.x.x"
        FMT_BASH: Generate a bash script file with "VERSION=x.x.x"
        FMT_STR: Writes just the version string to the file

        *custom_func*

        This provides support for writing or performing custom actions on getting the version.
        This function is called after generating `target_file` and `target_module`.

        NOTE: This fit a need where I wanted a way to hack-update a field in static content

        The expected function signature is `foo(version: str)`.

        .. code-block:: python

            from pkg_version_mgr import PkgVersionMgr

            def custom_writer(version: str):
                print('Build version: {}'.format(version))

            mgr = PkgVersionMgr(major=5, minor=1, micro=0)
            mgr.version(target_fmt=mgr.FMT_FUNCTION, custom_func=custom_writer)

            # Prints to console: "Build version: 5.1.0.a1"

        :param target_file: Filename to optionally write version to
        :param target_module: A module reference
        :param target_fmt: The format of target file to optionally write
        :param custom_func: A user-define function with signature: foo(version: str)

        :return: Version
        :rtype: str
        :raises InvalidParameterError: For invalid parameter type or content
        """
        real_version = self._get_version()

        if target_fmt not in [self.FMT_STR, self.FMT_BASH, self.FMT_PYTHON]:
            raise InvalidParameterError('Unsupported "target_fmt" parameter: {}'.format(target_fmt))

        if target_file:
            self._write_file(version=real_version, filename=target_file, fmt=target_fmt)

        if target_module:
            from types import ModuleType
            if not isinstance(target_module, ModuleType):
                raise InvalidParameterError('Invalid "version_module" parameter type')

            self._write_module(version=real_version, version_module=target_module)

        if custom_func:
            try:
                custom_func(real_version)
            except Exception as ex:
                raise_from(CustomFuncError(), ex)

        return real_version

    def _get_version(self):
        """Get the version.

        The version is obtain from one of:

        * CI_COMMIT_TAG
        * Constructed

        :return:
        :rtype: str
        """
        import os

        pipeline_id = os.environ.get(self.pipeline_id_name)
        commit_tag = os.environ.get(self.commit_tag_name)

        if commit_tag:
            return commit_tag

        return self._build_version(pipeline_id=pipeline_id)

    def _build_version(self, pipeline_id):
        """Construct the version string.

        :param pipeline_id:
        :type: str|None

        :return:
        :rtype: str
        """
        if not any([self.suffix, self.suffix_num]):
            suffix = None
        else:
            # If there is a suffix defined, but not the suffix_num, default to
            # the pipeline ID or "1" (like for local building)
            if self.suffix and not self.suffix_num:
                self.suffix_num = pipeline_id or "1"

            segments = [self.suffix, self.suffix_num]
            suffix = ''.join([s for s in segments if s])

        segments = [
            self.major,
            self.minor,
            self.micro,
            suffix
        ]
        # print('\n\n\n**** {} ****\n\n\n'.format(segments))

        return '.'.join([s for s in segments if s])

    @classmethod
    def _write_module(cls, version, version_module):
        """Write or update a version module.

        If the environment variable PKG_VER_SKIP_TARGET_MODULE is set (to any
        value) this will skip the write and do nothing.

        :param version: The version
        :type version: str

        :param version_module: Module to update

        :return: None
        """
        if os.environ.get(SKIP_UPDATE_VERSION):
            print('Skipping write target_module on {} set'.format(SKIP_UPDATE_VERSION))
            return

        filename = version_module.__file__
        cls._write_file(version=version, filename=filename, fmt=cls.FMT_PYTHON)

    @classmethod
    def _write_file(cls, version, filename, fmt):
        """Write the version to a file.

        FORMATS:

        * python: Writes to the Python module file for programmatic (or otherwise) access.
        * bash: Writes "VERSION=<version>" to a file for use by bash.
        * str: Write just <version> to the file

        :param version: Version as string
        :type version: str

        :param fmt: Format - one of "python", "bash", "str"
        :type fmt: str

        :return:
        """
        with open(filename, 'w+') as fp:
            if fmt == cls.FMT_PYTHON:
                print('"""Auto-generated by pkg_version_mgr."""\n', file=fp)
                print('__version__ = "{}"'.format(version), file=fp)

            elif fmt == cls.FMT_BASH:
                fp.write('VERSION={}'.format(version))

            elif fmt == cls.FMT_STR:
                fp.write(version)

            else:
                raise ValueError('Unrecognized file format: {}'.format(fmt))

    def _get_ci_vars(self):
        """Check for and return the "CI_" environment variables.

        :return: Tuple with (commit_tag, pipeline_id). Both, or either might be None
        :rtype: tuple
        """
        import os

        commit_tag = os.environ.get(self.commit_tag_name)
        pipeline_id = os.environ.get(self.pipeline_id_name)

        return commit_tag, pipeline_id
