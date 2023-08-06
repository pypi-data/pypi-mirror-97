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

from onyx.core import load_system_configuration, Date

from .utils import encode_message, request_to_uid
from .exceptions import NoDataserverAvailable

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.tcpclient
import tornado.gen

import asyncmc
import socket
import datetime
import random
import logging
import os
import json

RT_TIMEOUT = 300  # in seconds
TCP_TIMEOUT = 5  # in seconds
PENALTY_TIME = 0*60  # in seconds


###############################################################################
class DataRouter(tornado.web.Application):
    # -------------------------------------------------------------------------
    def __init__(self, logger=None, *args, **kwds):
        super().__init__(*args, **kwds)
        self.logger = logger or logging.getLogger(__name__)

        config = load_system_configuration()
        self.mc_servers = [config.get("memcache", "url")]
        self.dataservers = []
        self.penalty_box = {}
        self.timeouts = {}

        self.tcp_timeout = datetime.timedelta(seconds=TCP_TIMEOUT)

    # -------------------------------------------------------------------------
    def max_timeouts_exceeded(self, server_id):
        curr_time = Date.now()
        ntimeouts, last_timeout = self.timeouts.get(server_id, (0, curr_time))

        if (curr_time - last_timeout).seconds < 1:
            ntimeouts += 1
        else:
            ntimeouts = 1

        self.timeouts[server_id] = (ntimeouts, curr_time)
        return ntimeouts > 10

    # -------------------------------------------------------------------------
    def add_dataserver(self, addr, port, hostname):
        server_id = (addr, port, hostname)

        # --- don't register the same server multiple times
        if server_id in self.dataservers:
            return False

        # --- if server was put in the penalty box, check that penalty time has
        #     expired (this to avoid adding the same unresponsive server over
        #     and over)
        if addr in self.penalty_box:
            dt = Date.now() - self.penalty_box[addr]
            if dt.seconds > PENALTY_TIME:
                del self.penalty_box[addr]
            else:
                self.logger.info(
                    f"Registration of {addr!s} ({hostname:s}) refused")
                return False

        self.dataservers.append(server_id)
        self.logger.info(f"{server_id!s} registered as available server")
        return True

    # -------------------------------------------------------------------------
    def drop_dataserver(self, server_id, msg):
        self.logger.info(f"dropping dataserver {server_id!s}: {msg:s}")
        try:
            self.dataservers.remove(server_id)
            self.penalty_box[server_id[0]] = Date.now()
        except ValueError:
            pass

    # -------------------------------------------------------------------------
    def select_dataserver(self):
        try:
            return random.choice(self.dataservers)
        except IndexError:
            raise NoDataserverAvailable()

    # -------------------------------------------------------------------------
    def start(self, port=None):
        config = load_system_configuration()
        port = port or config.getint("datafeed", "router_port")

        # --- windows-specific hack: increase the file descriptor limit to
        #     circumvent "too many file descriptors in select()" error
        if os.name == "nt":
            import win32file
            win32file._setmaxstdio(2048)
            assert win32file._getmaxstdio() == 2048

        http_server = tornado.httpserver.HTTPServer(self)
        http_server.listen(port)

        # --- start the memcache-client
        self.cache = asyncmc.Client(
            servers=self.mc_servers, loop=tornado.ioloop.IOLoop.current())

        address = socket.gethostbyname(socket.gethostname())
        self.logger.info("listening on {0!s}:{1!s}".format(address, port))

        try:
            tornado.ioloop.IOLoop.current().start()
        except KeyboardInterrupt:
            tornado.ioloop.IOLoop.current().stop()
        finally:
            self.cleanup()

    # -------------------------------------------------------------------------
    def cleanup(self):
        self.logger.info("shutting down router")

    # -------------------------------------------------------------------------
    async def with_timeout(self, future):
        return await tornado.gen.with_timeout(self.tcp_timeout, future)

    # -------------------------------------------------------------------------
    async def fetch(self, req, addr, port):
        req = encode_message(req)

        client = tornado.tcpclient.TCPClient()
        stream = await self.with_timeout(client.connect(addr, port))

        try:
            await self.with_timeout(stream.write(req))
            response = await self.with_timeout(stream.read_until(b"\n"))
        finally:
            try:
                stream.close()
            except tornado.iostream.StreamClosedError:
                # --- this will ignore StreamClosedError raised when closing
                #     the connection, but StreamClosedErrors raised before will
                #     still be propagated
                pass

        return response

    # -------------------------------------------------------------------------
    async def process_request(self, req, real_time):
        # --- determine the unique request id, used for caching
        req_uid = request_to_uid(req, real_time)

        # --- first try fetching response from cache
        try:
            while True:
                response = await self.cache.get(req_uid)
                if response == "CacheLocked":
                    await tornado.gen.sleep(0.25)
                else:
                    break
        except:
            # --- if this fails assume memcache is not available, move on
            response = None

        if response is None:
            # --- no valid data stored in cache, send request to datafeed
            #     router.
            #     NB: we first lock the cache with a timeout (longer than the
            #         one used for requests) and then we only set the cache if
            #         the response is valid.
            try:
                await self.cache.set(
                    req_uid, "CacheLocked", 10*TCP_TIMEOUT, noreply=True)
            except:
                pass

            while True:
                # --- select dataserver or return error if none is available
                try:
                    addr, port, hostname = self.select_dataserver()
                except NoDataserverAvailable:
                    resp = {
                        "type": "NoDataserverAvailable",
                        "payload": "Dataservers not available or unresponsive",
                    }
                    return 503, encode_message(resp)

                # --- request data from datafeed server.
                #     if the data provider is unresponsive we get a message
                #     with the appropriate error in it (to be processed by the
                #     client)
                #     if the datafeed server itself is unresponsive we get a
                #     timeout error that needs to be managed here.
                try:
                    response = await self.fetch(req, addr, port)
                    break
                except (tornado.gen.TimeoutError,
                        tornado.iostream.StreamClosedError) as err:
                    if self.max_timeouts_exceeded((addr, port, hostname)):
                        # --- dataserver unresponsive: drop it from the list
                        self.drop_dataserver(
                            (addr, port, hostname), msg=str(err))

            if real_time:
                expiry = RT_TIMEOUT
            else:
                expiry = int(Date.today().eod().timestamp())

            try:
                await self.cache.set(req_uid, response, expiry, noreply=True)
            except:
                pass

            self.logger.debug(
                "returning value from dataserver "
                "(rt={0!s}), req_uid='{1!s}'".format(real_time, req_uid))

        else:
            self.logger.debug(
                "returning value from cache (rt={0!s})".format(real_time))

        #######################################################################
        # import random
        # if random.random() < 0.5:
        #     print("simulating unresponsive bloomberg")
        #     return 200, encode_message(
        #         {"type": "TimeoutError", "payload": "test"})
        #######################################################################

        return 200, response

    # -------------------------------------------------------------------------
    async def clear_cache(self, req, real_time):
        # --- determine the unique request id, used for caching
        req_uid = request_to_uid(req, real_time)
        try:
            await self.cache.delete(req_uid, noreply=True)
        except:
            pass


###############################################################################
class BaseHandler(tornado.web.RequestHandler):
    # -------------------------------------------------------------------------
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods",
            "POST, GET, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers",
            "Content-Type,Authorization,accept,Cache-Control,x-requested-with")

    # -------------------------------------------------------------------------
    def options(self, *args, **kwds):
        self.set_status(204)
        self.finish()


###############################################################################
class RegistrationHandler(BaseHandler):
    # -------------------------------------------------------------------------
    def put(self):
        addr = self.get_argument("address")
        port = self.get_argument("port")
        hostname = self.get_argument("hostname", "unknown")

        added = self.application.add_dataserver(addr, port, hostname)
        if added:
            self.set_status(201)
        else:
            self.set_status(205)

    # -------------------------------------------------------------------------
    async def get(self):
        self.write(json.dumps(self.application.dataservers))


###############################################################################
class BbgBDPHandler(BaseHandler):
    # -------------------------------------------------------------------------
    async def get(self):
        #######################################################################
        # import random
        # if random.random() < 0.25:
        #     print("simulating unresponsive router")
        #     self.request.connection.close()
        #     return
        #######################################################################

        rt = self.get_argument("rt", False)
        request = {
            "type": "BDP",
            "sec": self.get_argument("sec"),
            "field": self.get_argument("field"),
            "overrides": self.get_argument("overrides", "null"),
        }

        status, resp = await self.application.process_request(request, rt)

        self.set_status(status)
        self.write(resp)

    # -------------------------------------------------------------------------
    async def delete(self):
        self.set_header("Access-Control-Allow-Origin", "*")

        rt = self.get_argument("rt", False)
        request = {
            "type": "BDP",
            "sec": self.get_argument("sec"),
            "field": self.get_argument("field"),
            "overrides": self.get_argument("overrides", "null"),
        }

        await self.application.clear_cache(request, rt)
        self.set_status(204)


###############################################################################
class BbgBDHHandler(BaseHandler):
    # -------------------------------------------------------------------------
    async def get(self):
        rt = self.get_argument("rt", False)
        request = {
            "type": "BDH",
            "sec": self.get_argument("sec"),
            "field": self.get_argument("field"),
            "start": self.get_argument("start"),
            "end": self.get_argument("end"),
            "adjusted": self.get_argument("adjusted", True),
            "overrides": self.get_argument("overrides", "null"),
        }

        status, resp = await self.application.process_request(request, rt)

        self.set_status(status)
        self.write(resp)

    # -------------------------------------------------------------------------
    async def delete(self):
        rt = self.get_argument("rt", False)
        request = {
            "type": "BDH",
            "sec": self.get_argument("sec"),
            "field": self.get_argument("field"),
            "start": self.get_argument("start"),
            "end": self.get_argument("end"),
            "adjusted": self.get_argument("adjusted", True),
            "overrides": self.get_argument("overrides", "null"),
        }

        await self.application.clear_cache(request, rt)
        self.set_status(204)


###############################################################################
class BbgUniqueIdHandler(BaseHandler):
    # -------------------------------------------------------------------------
    def get(self):
        reqtype = self.get_argument("type")
        rt = self.get_argument("rt", False)

        if reqtype == "BDP":
            request = {
                "type": "BDP",
                "sec": self.get_argument("sec"),
                "field": self.get_argument("field"),
                "overrides": self.get_argument("overrides", None),
            }
        elif reqtype == "BDH":
            request = {
                "type": "BDH",
                "sec": self.get_argument("sec"),
                "field": self.get_argument("field"),
                "start": self.get_argument("start"),
                "end": self.get_argument("end"),
                "adjusted": self.get_argument("adjusted", True),
                "overrides": self.get_argument("overrides", None),
            }

        req_uid = request_to_uid(request, rt)

        self.set_status(200)
        self.write(req_uid)
