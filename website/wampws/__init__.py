###############################################################################
##
##  Copyright 2012 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################


import uuid

from optparse import OptionParser

from flask import Flask, Request, request, session, g, redirect, url_for, \
     abort, render_template, flash

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())


@app.before_request
def before_request():
   session["debug"] = app.debug

@app.after_request
def after_request(response):
   return response


@app.route('/')
def page_home():
   session['tab_selected'] = 'home'
   return render_template('page_t_home.html')

@app.route('/why')
def page_why():
   session['tab_selected'] = 'why'
   return render_template('page_t_why.html')

@app.route('/faq')
def page_faq():
   session['tab_selected'] = 'faq'
   return render_template('page_t_faq.html')

@app.route('/implementations')
def page_implementations():
   session['tab_selected'] = 'implementations'
   return render_template('page_t_implementations.html')

@app.route('/spec')
def page_spec():
   session['tab_selected'] = 'spec'
   return render_template('page_t_spec.html')


if __name__ == "__main__":

   parser = OptionParser ()

   parser.add_option ("-d",
                      "--debug",
                      dest = "debug",
                      action = "store_true",
                      default = False,
                      help = "Enable debug mode for Flask")

   parser.add_option ("-s",
                      "--socketserver",
                      dest = "socketserver",
                      action = "store_true",
                      default = False,
                      help = "Run Flask web app under standard Python SocketServer, instead of under Twisted")

   parser.add_option ("-p",
                      "--port",
                      dest = "port",
                      default = 8080,
                      help = "Listening port for Web server (i.e. 8090).")

   (options, args) = parser.parse_args ()

   if options.socketserver:
      print "Running Flask under standard Python SocketServer"
      app.run(host = "0.0.0.0", port = int(options.port), debug = options.debug)
   else:
      print "Running Flask under Twisted server"
      import sys
      from twisted.python import log
      from twisted.internet import reactor
      from twisted.web.server import Site
      from twisted.web.wsgi import WSGIResource

      app.debug = options.debug
      if options.debug:
         log.startLogging(sys.stdout)
      resource = WSGIResource(reactor, reactor.getThreadPool(), app)
      site = Site(resource)
      reactor.listenTCP(int(options.port), site)
      reactor.run()
