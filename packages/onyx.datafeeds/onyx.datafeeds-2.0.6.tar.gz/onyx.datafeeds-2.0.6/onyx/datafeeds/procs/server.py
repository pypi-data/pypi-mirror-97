###############################################################################
#
#   Copyright: (c) 2017 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

from ..serverlib import DataServer

from onyx.core import Date
from onyx.core.utils.logging import setup_logging_from_json_config

from dateutil.relativedelta import relativedelta

import argh
import logging


# -----------------------------------------------------------------------------
def run(
    dns_suffix=None,
    router_addr=None,
    router_port=None,
    logging_config_file=None,
    max_run_time=None,  # in minutes
    verbose=False
):
    setup_logging_from_json_config(logging_config_file)
    logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel(logging.DEBUG)

    if max_run_time is None:
        server = DataServer(logger=logger)
        server.start(dns_suffix, router_addr, router_port)
    else:
        # --- loop forever, shutting down the server and restarting it once
        #     the max_run_time has been reached
        while True:
            stop_at = Date.now() + relativedelta(minutes=int(max_run_time))
            server = DataServer(logger=logger)
            server.start(dns_suffix, router_addr, router_port, stop_at)


# -----------------------------------------------------------------------------
def main():
    argh.dispatch_command(run)


# -----------------------------------------------------------------------------
#  for interactive use
if __name__ == "__main__":
    run()
