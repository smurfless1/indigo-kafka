#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dave Brown
#
# config reference
# http://wiki.indigodomo.com/doku.php?id=indigo_6_documentation:plugin_guide#configuration_dialogs
#
#
import indigo

import os
import sys
import time as time_
import json
from indigo_adaptor import IndigoAdaptor
from kafka import KafkaProducer
from kafka.errors import KafkaError

class Connection:
    def __init__(self):
        self.topic = 'indigo-json'
        pass

    # call this with a LIST of host:port strings
    def connect(self, hostports):
        indigo.server.log(u'starting kafka connection')
        servers = hostports.split(',')
        if (len(servers) < 2):
            servers = [hostports]
        self.producer = KafkaProducer(
            bootstrap_servers = servers,
            value_serializer = lambda m: json.dumps(m).encode('utf-8')
        )
        indigo.server.log(u'kafka connection succeeded')

    def syncsend(self, what):
        try:
            future = self.producer.send(self.topic, what)
            record_metadata = future.get(timeout=10)
        except KafkaError:
            pass

    def send(self, what):
        try:
            self.producer.send(self.topic, what)
        except KafkaError:
            pass

    def stop(self):
        indigo.server.log(u'stopping kafka connection')
        self.producer.flush(timeout=5)

class Plugin(indigo.PluginBase):
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        # http://forums.indigodomo.com/viewtopic.php?f=108&t=14647
        indigo.devices.subscribeToChanges()
        self.adaptor = IndigoAdaptor()

    def startup(self):
        try:
            self.connection = Connection()
            target = self.pluginPrefs.get('hostport', 'localhost:9092')
            self.connection.connect(target)
            self.connection.topic = self.pluginPrefs.get('topic', 'indigo-json')

        except:
            indigo.server.log(u'Failed to connect in startup')
            pass

    # called after runConcurrentThread() exits
    def shutdown(self):
        self.connection.stop()

    def deviceUpdated(self, origDev, newDev):
        # call base implementation
        indigo.PluginBase.deviceUpdated(self, origDev, newDev)

        # custom add to kafka work
        newjson = self.adaptor.diff_to_json(newDev)

        if self.pluginPrefs.get('debug', False):
            indigo.server.log(json.dumps(newjson).encode('utf-8'))

        self.connection.send(newjson)
