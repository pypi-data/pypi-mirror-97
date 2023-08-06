import argparse
import re
from typing import List, Optional

from .parse_shell import get_command_as_args_list


class DockerArgumentParserError(Exception):
    pass


class DockerArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise DockerArgumentParserError(message)


class VolumeArgument:
    def __init__(self, host_path: Optional[str], container_path: str, options: Optional[str]):
        self.host_path = host_path
        self.container_path = container_path
        self.options = options

    def is_anonymous_volume(self) -> bool:
        return self.host_path is None

    def is_named_volume(self) -> bool:
        named_pattern = r"[a-zA-Z0-9][a-zA-Z0-9_.-]+"
        return not self.is_anonymous_volume() and re.fullmatch(named_pattern, self.host_path) is not None

    def is_bind_mount_volume(self) -> bool:
        return not self.is_anonymous_volume() and not self.is_named_volume()

    def __repr__(self):
        return f"VolumeArgument(host_path={self.host_path}, container_path={self.container_path}, options={self.options})"

    @staticmethod
    def parse(arg: str) -> 'VolumeArgument':
        pieces = arg.split(":")
        if 1 <= len(pieces) <= 3:
            options = None
            host_path = None
            if len(pieces) == 1:
                # '-v /CONTAINER_PATH' case
                container_path = pieces[0]
            else:
                # '-v HOST_PATH:/CONTAINER_PATH[:OPTIONS]' case
                host_path = pieces[0]
                container_path = pieces[1]
                if len(pieces) == 3:
                    options = pieces[2]
            return VolumeArgument(host_path, container_path, options)
        raise ValueError("invalid argument for -v/--volume")


class PortArgument:
    def __init__(self, ip_address: str, host_ports: Optional[List[int]], container_ports: List[int]):
        self.ip_address = ip_address
        self.host_ports = host_ports
        self.container_ports = container_ports

    def __repr__(self):
        return f"PortArgument(ip_address={self.ip_address}, host_port={self.host_ports}, container_port={self.container_ports})"

    @staticmethod
    def _expand_port_range(arg: str) -> List[int]:
        pieces = arg.split("-")
        if len(pieces) != 2:
            raise ValueError("invalid")
        begin, end = tuple(map(int, pieces))
        return list(range(begin, end + 1))

    @staticmethod
    def parse(arg: str) -> 'PortArgument':
        pieces = arg.split(":")
        if 1 <= len(pieces) <= 3:
            ip_address = None
            raw_host_ports = None
            ip_address_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
            if re.fullmatch(ip_address_pattern, pieces[0]) is not None:
                ip_address = pieces[0]
                pieces = pieces[1:]
            if len(pieces) < 3:
                if len(pieces) == 2:
                    raw_host_ports = pieces[0]
                    raw_container_ports = pieces[1]
                else:
                    raw_container_ports = pieces[0]
                try:
                    host_ports = None
                    if raw_host_ports is not None:
                        if "-" in raw_host_ports:
                            host_ports = PortArgument._expand_port_range(raw_host_ports)
                        else:
                            host_ports = [int(raw_host_ports)]
                    if "-" in raw_container_ports:
                        container_ports = PortArgument._expand_port_range(raw_container_ports)
                    else:
                        container_ports = [int(raw_container_ports)]

                    if host_ports is None or len(host_ports) == len(container_ports):
                        return PortArgument(ip_address, host_ports, container_ports)
                except ValueError:
                    pass
        raise ValueError("invalid argument for -p/--publish")


def _add_run_subparser(subparsers):
    run_parser = subparsers.add_parser("run", add_help=False)
    run_parser.add_argument("-a", "--attach", type=str)
    run_parser.add_argument("--add-host", type=str, action="append")
    run_parser.add_argument("--blkio-weight", type=int)
    run_parser.add_argument("--blkio-weight-device", type=str)
    run_parser.add_argument("--cap-add", type=str, action="append")
    run_parser.add_argument("--cap-drop", type=str, action="append")
    run_parser.add_argument("--cgroup-parent", type=str)
    run_parser.add_argument("--cidfile", type=str)
    run_parser.add_argument("--cpu-count", type=int)
    run_parser.add_argument("--cpu-percent", type=int)
    run_parser.add_argument("--cpu-period", type=int)
    run_parser.add_argument("--cpuset-cpus", type=str)
    run_parser.add_argument("--cpuset-mems", type=str)
    run_parser.add_argument("-d", "--detach", action='store_true')
    run_parser.add_argument("--device", type=str)
    run_parser.add_argument("--device-cgroup-rule", type=str)
    run_parser.add_argument("--dns", type=str, action="append")
    run_parser.add_argument("-e", "--env", type=str, action="append")
    run_parser.add_argument("--entrypoint", type=str)
    run_parser.add_argument("--env-file", type=str)
    run_parser.add_argument("--expose", type=str)
    run_parser.add_argument("--help", action="store_true")
    run_parser.add_argument("-h", "--hostname", type=str)
    run_parser.add_argument("-i", "--interactive", action='store_true')
    run_parser.add_argument("--init", action="store_true")
    run_parser.add_argument("--ipc", type=str)
    run_parser.add_argument("--isolation", type=str)
    run_parser.add_argument("-l", "--label", type=str, action="append")
    run_parser.add_argument("--label-file", type=str)
    run_parser.add_argument("--link", type=str, action="append")
    run_parser.add_argument("--mac-address", type=str)
    run_parser.add_argument("-m", "--memory", type=str)
    run_parser.add_argument("--memory-reservation", type=str)
    run_parser.add_argument("--name", type=str)
    run_parser.add_argument("--network", type=str)
    run_parser.add_argument("--oom-kill-disable", action='store_true')
    run_parser.add_argument("--pids-limit", type=int)
    run_parser.add_argument("-P", "--publish-all", action='store_true')
    run_parser.add_argument("-p", "--publish", type=PortArgument.parse, action="append")
    run_parser.add_argument("--privileged", action='store_true')
    run_parser.add_argument("--read-only", action='store_true')
    run_parser.add_argument("--rm", action='store_true')
    run_parser.add_argument("--stop-signal", type=str)
    run_parser.add_argument("--stop-timeout", type=int)
    run_parser.add_argument("--memory-swappiness", type=int)
    run_parser.add_argument("-t", "--tty", action='store_true')
    run_parser.add_argument("-u", "--user", type=str)
    run_parser.add_argument("-v", "--volume", type=VolumeArgument.parse, action="append")
    run_parser.add_argument("--volumes-from", type=str, action="append")
    run_parser.add_argument("-w", "--workdir", type=str)
    run_parser.add_argument("image", type=str)
    run_parser.add_argument("args", type=str, nargs=argparse.REMAINDER)


def docker_run_argument_parser() -> DockerArgumentParser:
    """
    Returns a parser suitable for parsing the docker-run subcommand
    """

    ap = DockerArgumentParser(prog="docker", add_help=False)
    subparsers = ap.add_subparsers()
    _add_run_subparser(subparsers)
    return ap


def docker_container_run_parser():
    """
    Returns a parser suitable for parsing the docker-container-run subcommand
    """

    ap = DockerArgumentParser(prog="docker", add_help=False)
    subparsers = ap.add_subparsers()
    container = subparsers.add_parser("container", add_help=False)
    container_subparsers = container.add_subparsers()
    _add_run_subparser(container_subparsers)
    return ap


def parse_args_as_run_command(args: List[str]):
    """
    Parses a list of arguments as a docker-run or docker-container-run command

    Raises ValueError if the command is not either of 'docker run' or 'docker container run'
    """
    if args[0] == "run":
        return docker_run_argument_parser().parse_args(args)
    elif args[0] == "container" and args[1] == "run":
        return docker_container_run_parser().parse_args(args)
    cmd = args[0] if args[0] != "container" else f"{args[0]} {args[1]}"
    raise ValueError(
        f"expected 'docker run' or 'docker container run', got 'docker {cmd}'"
    )


def parse_as_run_command(command):
    """
    Parses a command as a docker-run or docker-container-run command

    Raises ValueError if the command is not either of 'docker run' or 'docker container run'
    """
    command_words = get_command_as_args_list(command)
    return parse_args_as_run_command(command_words[1:])
