#!/usr/bin/env python

import os
import rospkg
import rospy
import threading
import SimpleHTTPServer
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass


class SrHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    pass


if __name__ == "__main__":
    rospy.init_node("sr_teleop_polhemus_documentation_webserver")

    port = rospy.get_param('~port', 8080)
    address = ("", port)

    # Changing directory to html folder
    page_path = rospkg.RosPack().get_path('sr_teleop_polhemus_documentation') + "/html"
    os.chdir(page_path)

    # Starting server in a thread
    server = ThreadedHTTPServer(address, SrHandler)
    rospy.loginfo("Serving Teleop Polhemus Documentation at port %s" % port)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    rospy.spin()

    # Kill server before shutdown
    rospy.loginfo("sr_teleop_polhemus_documentation server is going down")
    server.shutdown()
