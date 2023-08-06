#
# Copyright ifm electronic, gmbh
# SPDX-License-Identifier: MIT
# 
from __future__ import (absolute_import, division, print_function, unicode_literals)
from builtins import *
import xmlrpc.client
from ifmO3r.rpc.session import *

class Device:
    def __init__(self, address="192.168.0.69", apiPath="/api/rpc/v1/"):
        self.address = address
        self.baseURL = "http://" + address + apiPath
        self.mainURL = self.baseURL + 'com.ifm.efector/'
        self.rpc = xmlrpc.client.ServerProxy(self.mainURL)

    def requestSession(self, password="", sessionID=""):
        self.sessionID = self.rpc.requestSession(password, sessionID)
        self.sessionURL = self.mainURL + 'session_' + self.sessionID + '/'
        self.session = Session(self.sessionURL)
        return self.session

    def __getattr__(self, name):
        # Forward otherwise undefined method calls to XMLRPC proxy
        return getattr(self.rpc, name)


class Imager:
    def __init__(self, address="192.168.0.69", imagerID=0, apiPath="/api/rpc/v1/"):
        self.address = address
        self.baseURL = "http://" + address + apiPath
        self.mainURL = self.baseURL + \
            'com.ifm.imager.i{0:0=3d}/'.format(imagerID)
        self.rpc = xmlrpc.client.ServerProxy(self.mainURL)
        self.paramsProxy = xmlrpc.client.ServerProxy(self.mainURL + 'params')
        self.algoProxy = xmlrpc.client.ServerProxy(self.mainURL + 'algo')
        self.adProxy = xmlrpc.client.ServerProxy(self.mainURL + 'algodebug')
        self.modeProxy = xmlrpc.client.ServerProxy(self.mainURL + 'mode')

    def requestSession(self, password="", sessionID=""):
        self.sessionID = self.rpc.requestSession(password, sessionID)
        self.sessionURL = self.mainURL + 'session_' + self.sessionID + '/'
        self.session = Session(self.sessionURL)
        return self.session

    def __getattr__(self, name):
        # Forward otherwise undefined method calls to XMLRPC proxy
        if name == "params":
            return self.paramsProxy
        if name == "algo":
            return self.algoProxy
        if name == "algodebug":
            return self.adProxy
        if name == "mode":
            return self.modeProxy                
        return getattr(self.rpc, name)
