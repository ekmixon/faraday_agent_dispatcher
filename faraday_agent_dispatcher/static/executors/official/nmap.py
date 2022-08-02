#!/usr/bin/env python3

import os
import subprocess
from urllib.parse import urlparse

"""You need to clone and install faraday plugins"""
from faraday_plugins.plugins.repo.nmap.plugin import NmapPlugin


def command_create(target_list):
    my_envs = os.environ
    cmd = ["nmap"]
    cmd_end = ["-oX", "-", "--"]

    # when the frontend bug is solved leave it this way
    # if 'EXECUTOR_CONFIG_PORT_LIST' in my_envs:
    #     cmd.append(f'-p {os.environ.get("EXECUTOR_CONFIG_PORT_LIST")}')
    #
    # if 'EXECUTOR_CONFIG_OPTION_SC' in my_envs:
    #     cmd.append('-sC')
    #
    # if 'EXECUTOR_CONFIG_OPTION_SV' in my_envs:
    #     cmd.append('-sV')
    #
    # if 'EXECUTOR_CONFIG_OPTION_PN' in my_envs:
    #     cmd.append('-Pn')
    #
    # if 'EXECUTOR_CONFIG_SCRIPT_TIMEOUT' in my_envs:
    #     cmd.append(f'--script-timeout '
    #                f'{os.environ.get("EXECUTOR_CONFIG_SCRIPT_TIMEOUT")}')
    #
    # if 'EXECUTOR_CONFIG_HOST_TIMEOUT' in my_envs:
    #     cmd.append(f'--host-timeout '
    #                f'{os.environ.get("EXECUTOR_CONFIG_HOST_TIMEOUT")}')

    port_list = my_envs.get("EXECUTOR_CONFIG_PORT_LIST")
    cmd += ["-p", f"{port_list}"] if port_list else ""

    top_ports = my_envs.get("EXECUTOR_CONFIG_TOP_PORTS")
    cmd += ["--top-ports", f"{top_ports}"] if top_ports else ""

    cmd += ["-sC"] if my_envs.get("EXECUTOR_CONFIG_OPTION_SC") else ""

    cmd += ["-sV"] if my_envs.get("EXECUTOR_CONFIG_OPTION_SV") else ""

    cmd += ["-Pn"] if my_envs.get("EXECUTOR_CONFIG_OPTION_PN") else ""

    script_timeout = my_envs.get("EXECUTOR_CONFIG_SCRIPT_TIMEOUT")
    cmd += ["--script-timeout", script_timeout] if script_timeout else ""

    host_timeout = my_envs.get("EXECUTOR_CONFIG_HOST_TIMEOUT")
    cmd += ["--host-timeout", host_timeout] if host_timeout else ""

    script_cmd = my_envs.get("EXECUTOR_CONFIG_SCRIPT_CMD")
    cmd += ["--script", f"{script_cmd}"] if script_cmd else ""

    cmd += cmd_end

    cmd += target_list
    return cmd


def main():
    targets = os.environ.get("EXECUTOR_CONFIG_TARGET")

    if " " in targets:
        target_list = targets.split(" ")
    elif "," in targets:
        target_list = targets.split(",")
    else:
        target_list = [targets]

    urls = []
    for target in target_list:
        url = urlparse(target)
        if url.scheme:
            urls.append(url.hostname)
        else:
            urls.append(target)

    cmd = command_create(target_list=urls)
    results = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    nmap = NmapPlugin()
    nmap.parseOutputString(results.stdout.encode())
    print(nmap.get_json())


if __name__ == "__main__":
    main()
