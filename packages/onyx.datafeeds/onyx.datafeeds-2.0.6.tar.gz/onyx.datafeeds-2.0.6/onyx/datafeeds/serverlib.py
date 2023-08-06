###############################################################################
#
#   Copyright: (c) 2017-2021 Carlo Sbraccia
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

from onyx.core import load_system_configuration
from onyx.core import Date
from onyx.core import CurveField, HlocvCurveField, GCurveField

from .utils import encode_message, decode_message

from .exceptions import DatafeedError, DatafeedFatal, SecurityError, FieldError
from .bloomberg import blp_api as bbg_api

from concurrent import futures

import tornado.ioloop
import tornado.tcpserver
import tornado.httpclient
import tornado.gen
import tornado.netutil

import time
import json
import datetime
import socket
import urllib
import logging

__all__ = ["DataServer"]

API_ERRORS = DatafeedError, SecurityError, FieldError, NotImplementedError
CONN_ERRORS = tornado.gen.TimeoutError, tornado.iostream.StreamClosedError
REREGISTER = 60000*2  # check registration every 2 minutes
BDH_TIMEOUT_MUL = 3


# -----------------------------------------------------------------------------
def cycle(elements):
    while True:
        for element in elements:
            yield element


# -----------------------------------------------------------------------------
def bdp_request(bdp_clt, timeout, request):
    try:
        data = bdp_clt.fetch(timeout=timeout, **request)
        return {
            "type": type(data).__name__,
            "payload": data,
        }
    except API_ERRORS as err:
        return {
            "type": type(err).__name__,
            "payload": str(err),
        }


# -----------------------------------------------------------------------------
def bdh_request(timeout, request):
    try:
        data = bbg_api.BbgBDH(timeout=timeout, **request)
        return {
            "type": type(data).__name__,
            "payload": data,
        }
    except API_ERRORS as err:
        return {
            "type": type(err).__name__,
            "payload": str(err),
        }


# -----------------------------------------------------------------------------
def process_response(resp):
    dtype = resp["type"]
    if dtype == "Curve":
        resp["payload"] = CurveField.to_json(None, resp["payload"])
    elif dtype == "HlocvCurve":
        resp["payload"] = HlocvCurveField.to_json(None, resp["payload"])
    elif dtype == "GCurve":
        resp["payload"] = GCurveField.to_json(None, resp["payload"])
    return resp


# -----------------------------------------------------------------------------
def get_address_port_hostname(sockets, dns_suffix):
    port = sockets[0].getsockname()[1]
    hostname = socket.gethostname()
    for addr in socket.gethostbyname_ex(hostname)[2]:
        info = socket.gethostbyaddr(addr)
        if info[0].endswith(dns_suffix):
            return port, addr, hostname
    raise RuntimeError(
        f"cannot detect IP Address with DNS suffix {dns_suffix!s}")


###############################################################################
class DataServer(tornado.tcpserver.TCPServer):
    """
    NB:
        - a BDP roundtrip should take at most:
                blp_timeout + 2*tcp_timeout + cpu time
        - a BDH roundtrip should take at most:
                BDH_TIMEOUT_MUL*blp_timeout + 2*tcp_timeout + cpu time
    """
    # -------------------------------------------------------------------------
    def __init__(
        self,
        logger=None,
        nthreads=10,
        blp_timeout=1000, # milliseconds
        tcp_timeout=100   # milliseconds
    ):
        super().__init__()
        self.logger = logger or logging.getLogger(__name__)
        self.tpool = futures.ThreadPoolExecutor(max_workers=nthreads)
        self.blp_timeout = blp_timeout
        self.tcp_timeout = datetime.timedelta(milliseconds=tcp_timeout)
        self.bdp_clients = cycle([
            bbg_api.bdp_client() for thread in range(nthreads)])

    # -------------------------------------------------------------------------
    def start(
        self,
        dns_suffix=None,
        router_addr=None,
        router_port=None,
        stop_at=None
    ):
        config = load_system_configuration()
        dns_suffix = dns_suffix or config.get("datafeed", "dns_suffix")
        router_addr = router_addr or config.get("datafeed", "router_address")
        router_port = router_port or config.getint("datafeed", "router_port")

        # --- connect to a random port from the available pool
        sockets = tornado.netutil.bind_sockets(0, address="")
        self.add_sockets(sockets)

        # --- get the port, the IP address and the host name
        port, addr, hostname = get_address_port_hostname(sockets, dns_suffix)

        # --- create the request object used to notify the router that this
        #     server is available
        self.subreq = tornado.httpclient.HTTPRequest(
            f"http://{router_addr!s}:{router_port!s}/register/",
            method="PUT",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            body=urllib.parse.urlencode({
                "address": addr,
                "port": port,
                "hostname": hostname}),
            request_timeout=self.tcp_timeout.seconds
        )

        ioloop = tornado.ioloop.IOLoop.current()

        ioloop.add_callback(self.subscribe_to_router)
        if tornado.version < "5.0.0":
            args = (self.subscribe_to_router, REREGISTER, ioloop)
        else:
            args = (self.subscribe_to_router, REREGISTER)
        tornado.ioloop.PeriodicCallback(*args).start()

        if stop_at is not None:
            seconds = (stop_at - Date.now()).seconds
            ioloop.call_later(seconds, lambda: self.stop_server())

        try:
            ioloop.start()
        except KeyboardInterrupt:
            self.stop_server()
        finally:
            # --- make sure all pending tasks have been terminated
            while ioloop.asyncio_loop.is_running():
                self.logger.info("ioloop still running, wait for it to stop")
                time.sleep(2)
            self.logger.info("server has been stopped")

    # -------------------------------------------------------------------------
    def thrd_async(self, func, *args):
        ioloop = tornado.ioloop.IOLoop.instance()
        return ioloop.run_in_executor(self.tpool, func, *args)

    # -------------------------------------------------------------------------
    async def with_timeout(self, future):
        return await tornado.gen.with_timeout(self.tcp_timeout, future)

    # -------------------------------------------------------------------------
    def stop_server(self):
        self.logger.info("shutting down server...")
        # --- stop listening for new connections
        super().stop()
        # --- then stop the threadpool (this will not return until all the
        #     pending futures are done)
        self.tpool.shutdown(wait=True)
        # --- finally stop the ioloop itself
        tornado.ioloop.IOLoop.current().stop()

    # -------------------------------------------------------------------------
    async def handle_stream(self, stream, address):
        # --- use time.time to monitor time needed to process request
        t_start = time.time()

        self.logger.debug(f"connection received from {address!s}")

        try:
            request = await self.with_timeout(stream.read_until(b"\n"))
        except CONN_ERRORS as err:
            self.logger.error(
                f"couldn't read request from {address!s}: {err!s}")
            return

        request = decode_message(request)
        self.logger.debug(f"processing request {request!s}")

        request_type = request.pop("type")

        # --- overrides, which are sent by clients as json strings, are decoded
        #     here 'in-place'
        request["overrides"] = json.loads(request["overrides"])

        try:
            if request_type == "BDP":
                # --- pull a bbg-bdp client from the clients pool
                clt = next(self.bdp_clients)
                resp = await self.thrd_async(
                    bdp_request, clt, self.blp_timeout, request)
            else:
                # --- for BDH requests allow for much longer timeout
                resp = await self.thrd_async(
                    bdh_request, BDH_TIMEOUT_MUL*self.blp_timeout, request)
        except TimeoutError:
            err_msg = \
                f"bloomberg request timed out after {self.blp_timeout!s} ms"
            self.logger.info(err_msg)
            resp = {
                "type": "TimeoutError",
                "payload": err_msg
            }
            # --- try re-initializing client
            clt.stop()
            clt.initialize_session_and_service()
        except DatafeedFatal as err:
            # --- unrecoverable bloomberg error: don't send a reply so that
            #     the datafeed router knows this server is currently unable
            #     to respond to requests.
            self.logger.error(err, exc_info=True)
            return

        resp = process_response(resp)
        resp = encode_message(resp)

        try:
            await self.with_timeout(stream.write(resp))
        except CONN_ERRORS as err:
            self.logger.error(
                f"couldn't send resp to {address!s}: {err!s}")
            return

        time_total = (time.time() - t_start)*1000.0
        self.logger.info(
            f"request {request!s} processed in {time_total:f}ms")

    # -------------------------------------------------------------------------
    async def subscribe_to_router(self):
        # --- register only if bloomberg service is available
        active = bbg_api.test_bbg_data_service()
        if not active:
            self.logger.info(
                "couldn't register server "
                "with router: bloomberg service currently unavailable")
            return

        self.logger.debug(
            f"trying to register with datafeed router on {self.subreq.url!s}")

        client = tornado.httpclient.AsyncHTTPClient()
        try:
            res = await client.fetch(self.subreq)
        except ConnectionRefusedError:
            self.logger.info(
                "couldn't register with "
                f"datafeed router  {self.subreq.url!s}: connection refused")
            return
        except tornado.httpclient.HTTPError as err:
            self.logger.info(
                "couldn't register with "
                f"datafeed router {self.subreq.url!s}: {err!s}")
            return

        if res.code == 201:
            self.logger.info("router accepted subscription")
        elif res.code == 205:
            # --- server already registered with router
            pass
        else:
            raise res.error
