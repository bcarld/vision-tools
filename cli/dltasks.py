#!/usr/bin/env python
# IBM_PROLOG_BEGIN_TAG
#
# Copyright 2019,2020 IBM International Business Machines Corp.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#  implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  IBM_PROLOG_END_TAG


import sys
import paiv
import paiv_cli_utils
from paiv_cli_utils import reportSuccess, reportApiError, translate_flags

# All of the PAIV CLI requires python 3.6 due to format string
# Make the check in a common location
if sys.hexversion < 0x03060000:
    sys.exit("Python 3.6 or newer is required to run this program.")

server = None

# ---  Create Operation  ---------------------------------------------
create_usage = """
Usage:
  Creating of training tasks is performed via the command 'datasets train'.

Use 'datasets train --help' for details."""


def create(params):
    """ Creating of training tasks is performed via the command 'datasets train"""

    print("Create training tasks by using the 'datasets train' command.", file=sys.stderr)


# ---  Delete Operation  ---------------------------------------------
delete_usage = """
Usage:
  dltasks delete --taskid=<task-id>

Where:
  --taskid   A required parameter that identifies the dltask to be
           deleted.

Deletes the indicated dltask. At this time, only 1 dltask can be 
deleted at a time."""


def delete(params):
    """Deletes one dltask identified by the --taskid parameter.

    Future work should allow a list of dltasks."""

    taskid = params.get("--taskid", "missing_id")
    rsp = server.dl_tasks.delete(taskid)
    if rsp is None:
        reportApiError(server, f"Failure attempting to delete dataset id '{taskid}'")
    else:
        reportSuccess(server, f"Deleted dataset id '{taskid}'")


# ---  List Operation  -----------------------------------------------
list_usage = """
Usage:
  dltasks list [--pgid=<project-group-id>...] [--status=<status>] [--summary]

Where:
  --pgid   An optional parameter that identifies 1 or more project groups
           on which to filter the list.  Multiple project groups must
           be comma separated
  --status An optional parameter to identifies the status by which to filter
           the list.
  --summary Flag requesting only summary output for each dataset returned

Generates a JSON list of dltasks matching the input criteria."""


def report(params):
    """Handles the 'list' operation.
    'params' flags are translated into query-parameter variable names."""

    summaryFields = None
    if params["--summary"]:
        summaryFields = ["_id", "usage", "status", "nn_arch", "name"]

    expectedArgs = {
        '--pgid': 'pg_id',
        '--status': 'status'
    }
    kwargs = translate_flags(expectedArgs, params)

    rsp = server.dl_tasks.report(**kwargs)

    if rsp is None:
        reportApiError(server, "Failure attempting to list dltasks")
    else:
        reportSuccess(server, None, summaryFields=summaryFields)


# ---  Show Operation  -----------------------------------------------
show_usage = """
Usage:
  dltasks show --taskid=<dltask-id>

Where:
  --taskid  A required parameter that identifies the dltask to be
            shown.

Shows detail metadata information for the indicated dltask."""


def show(params):
    """Handles the 'show' operation to show details of a single dltask"""

    dltask = params.get("--taskid", "missing_id")
    rsp = server.dl_tasks.show(dltask)
    if rsp is None:
        reportApiError(server, f"Failure attempting to get dltask id '{dltask}'")
    else:
        reportSuccess(server)


# ---  Status Operation  ---------------------------------------------
status_usage = """
Usage:
  dltasks status --taskid=<dltask-id>

Where:
  --taskid  A required parameter that identifies the dltask whose
            status records are to be retrieved.

Shows training status messages for the indicated dltask."""


def status(params):
    """Handles the 'status' operation to show training status messages of a dltask"""

    dltask = params.get("--taskid", "missing_id")
    rsp = server.dl_tasks.status(dltask)
    if rsp is None:
        reportApiError(server, f"Failure attempting to get dltask id '{dltask}'")
    else:
        reportSuccess(server)


cmd_usage = f"""
Usage:  dltasks {paiv_cli_utils.common_cmd_flags} <operation> [<args>...]

Where:
{paiv_cli_utils.common_cmd_flag_descriptions}

   <operation> is required and must be one of:
      create  -- creates a new dltask
      list    -- report a list of dltasks
      delete  -- delete one or more dltasks
      show    -- show a specific dltask
      status  -- show training status messages for a dltask

Use 'dltasks <operation> --help' for more information on a specific command."""

usage_stmt = {
    "usage": cmd_usage,
    "create": create_usage,
    "list": list_usage,
    "delete": delete_usage,
    "show": show_usage,
    "status": status_usage
}

operation_map = {
    "create": create,
    "list": report,
    "delete": delete,
    "show": show,
    "status": status
}


def main(params, cmd_flags=None):
    global server

    args = paiv_cli_utils.get_valid_input(usage_stmt, operation_map, argv=params, cmd_flags=cmd_flags)
    if args is not None:
        server = paiv.connect_to_server(paiv_cli_utils.host_name, paiv_cli_utils.token)
        args.operation(args.op_params)


if __name__ == "__main__":
    main(None)
