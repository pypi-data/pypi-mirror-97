import subprocess
import os


def execute_on_all_nodes(command: str, timeout=None, debug=False):
    """
    Execute the given command on all nodes in the cluster
    via mpiexec.
    """
    args = [
        "mpiexec",
        "--machinefile",  # Use machinefile to specify the nodes
        f"{os.getenv('HOME')}/machinefile",
        "-prepend-rank",  # To make the output easier to parse through
        "-ppn",  # Run once per node
        "1",
    ]
    args += command.split()
    if debug:
        print("Command: ", " ".join(args))

    stdout_ = ""
    stderr_ = ""
    returncode = None
    timed_out = False

    try:
        res = subprocess.run(args, capture_output=True, timeout=timeout)
        stdout_ = res.stdout.decode("utf-8")
        stderr_ = res.stderr.decode("utf-8")
        returncode = res.returncode
    except subprocess.TimeoutExpired as e:
        stdout_ = e.stdout.decode("utf-8") if e.stdout else e.stdout
        stderr_ = e.stderr.decode("utf-8") if e.stderr else e.stderr
        returncode = 124  # Usual shell error code for timeouts
        timed_out = True
    # TODO Handle other types of exceptions

    return stdout_, stderr_, returncode, timed_out
