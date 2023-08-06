import IPython
from IPython.core import magic_arguments
from IPython.core.magic import (
    line_magic,
    Magics,
    magics_class,
)
from .helper import execute_on_all_nodes
import sys


@magics_class
class PackageInstallationMagics(Magics):
    """
    Magics to enable installing conda and pip packages
    on all nodes in a cluster.
    """

    def __display_usage_error__(self, err_msg):
        """
        Display a usage error message
        """
        self.shell.show_usage_error(err_msg)

    def __display_error_message__(self, err_msg):
        """
        Display an error message
        """
        print("Error: %s" % err_msg, file=sys.stderr)

    @line_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "pkg_names",
        nargs="+",
        type=str,
        default=[],
        help="name of the packages to install",
    )
    @magic_arguments.argument(
        "-c",
        "--channel",
        nargs="+",
        type=str,
        default=[],
        help="channels to use (same semantics as conda install -c)",
    )
    @magic_arguments.argument(
        "--timeout", type=int, default=None, help="number of seconds to timeout after",
    )
    @magic_arguments.argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Print debug information such as the mpiexec commands being run.",
    )
    def conda_install(self, line="", local_ns=None):
        """
        Bodo IPython Magic to install a conda package on all the cluster nodes.
        """
        # Parse the arguments
        args = magic_arguments.parse_argstring(self.conda_install, line)
        # Error out if no packages are listed
        if not args.pkg_names:
            self.__display_usage_error__("No packages provided")
            return
        # Channel substring based on if args.channel is provided
        channels = f"-c {' '.join(args.channel)}" if args.channel else ""
        # TODO Find a way to abstract /opt/conda/bin/conda away
        command = f"sudo /opt/conda/bin/conda install -y {' '.join(args.pkg_names)} {channels}"
        command = command.strip()
        # Execute on all nodes
        stdout_, stderr_, returncode, timed_out = execute_on_all_nodes(
            command, args.timeout, args.debug,
        )
        # Handle output
        if timed_out:
            self.__display_error_message__("Timed out!")
        print("Output:\n", stdout_)
        if stderr_:
            self.__display_error_message__(stderr_)
        if args.debug:
            print("returncode: ", returncode)

    @line_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "pkg_names",
        nargs="+",
        type=str,
        default=[],
        help="name of the packages to install",
    )
    @magic_arguments.argument(
        "--timeout", type=int, default=None, help="number of seconds to timeout after."
    )
    @magic_arguments.argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Print debug information such as the mpiexec commands being run.",
    )
    def pip_install(self, line="", local_ns=None):
        """
        Bodo IPython Magic to install a pip package on all the cluster nodes.
        """
        # Parse the arguments
        args = magic_arguments.parse_argstring(self.pip_install, line)
        # Error out if no packages are listed
        if not args.pkg_names:
            self.__display_usage_error__("No packages provided")
            return
        # TODO Find a way to abstract /opt/conda/bin/pip away
        command = f"/opt/conda/bin/pip install {' '.join(args.pkg_names)}"
        # Execute on all nodes
        stdout_, stderr_, returncode, timed_out = execute_on_all_nodes(
            command, args.timeout, args.debug,
        )
        # Handle output
        if timed_out:
            self.__display_error_message__("Timed out!")
        print("Output:\n", stdout_)
        if stderr_:
            self.__display_error_message__(stderr_)
        if args.debug:
            print("returncode: ", returncode)


def load_ipython_extension(ipython):
    """
    Register the magics with IPython
    """
    ipython.register_magics(PackageInstallationMagics)


from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
