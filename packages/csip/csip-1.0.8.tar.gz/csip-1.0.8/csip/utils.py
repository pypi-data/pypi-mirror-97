"""
 * $Id: 1.0+8 utils.py a92a642340f2 2021-02-12 francesco.serafin.3@gmail.com $
 *
 * This file is part of the Cloud Services Integration Platform (CSIP),
 * a Model-as-a-Service framework, API and application suite.
 *
 * 2012-2018, Olaf David and others, OMSLab, Colorado State University.
 *
 * OMSLab licenses this file to you under the MIT license.
 * See the LICENSE file in the project root for more information.
"""
import glob
from os import path
from pathlib import Path
from shutil import make_archive
from time import sleep
from typing import List, Dict, Tuple

import json
import os
import re
import requests
import sys


class Client(object):
    """
    CSIP client class.
    
    (c) 2018, 2019 by Olaf David and others. Colorado State University
    License MIT, see LICENSE for more details.
    """

    PARAMETER = "parameter"
    RESULT = "result"
    METAINFO = "metainfo"

    KEY_NAME = "name"
    KEY_VALUE = "value"
    KEY_UNIT = "unit"
    KEY_DESCRIPTION = "description"
    KEY_PATH = "path"
    KEY_TYPE = "type"
    KEY_COORD = "coordinates"

    META_KEY_SUID = "suid"
    META_KEY_STATUS = "status"
    META_KEY_ERROR = "error"
    META_KEY_STACKTRACE = "stacktrace"
    META_KEY_MODE = "mode"
    META_KEY_SERVICE_URL = "service_url"
    META_KEY_FIRST_POLL = "first_poll"
    META_KEY_NEXT_POLL = "next_poll"
    META_VAL_SYNC = "sync"
    META_VAL_ASYNC = "async"
    META_KEY_PROGRESS = "progress"

    REQ_PARAM = "param"
    REQ_FILE = "file"
    REQ_JSON = "request.json"

    STATUS_FINISHED = "Finished"
    STATUS_SUBMITTED = "Submitted"
    STATUS_FAILED = "Failed"
    STATUS_RUNNING = "Running"
    STATUS_QUEUED = "Queued"

    HDR_CSIP_WEBHOOK = "X-CSIP-Webhook"
    HDR_CSIP_REQUESTFILE = "X-CSIP-Request-File"

    def __init__(self, data: Dict = None, metainfo: Dict = None,
                 parent: 'Client' = None, url: str = None, name: str = '', descr: str = ''):
        # parameter data or result data
        self.data = Client.__create_dict(data or [])
        # metainfo 
        self.metainfo = metainfo or {}
        # the parent CSIP payload (request)
        self.parent = parent

        # p/s delay for staggering pubsub submission, default none
        self._delay = 0

        # p/s batch subset to run, default all
        self._batch = (1, sys.maxsize)

        if self.KEY_PATH in self.metainfo:
            self.metainfo[self.META_KEY_SERVICE_URL] = self.metainfo[self.KEY_PATH]
        else:
            self.metainfo[self.META_KEY_SERVICE_URL] = self.metainfo.get(self.META_KEY_SERVICE_URL, url)

        self.metainfo[self.KEY_DESCRIPTION] = self.metainfo.get(self.KEY_DESCRIPTION, descr)
        self.metainfo[self.KEY_NAME] = self.metainfo.get(self.KEY_NAME, name)

    #### static
    @staticmethod
    def load_json(file: str) -> Dict:
        """Load a json file as dict"""
        with open(file) as f:
            data = json.load(f)
        return data

    @staticmethod
    def save_json(file: str, data: Dict) -> None:
        """Save the file"""
        with open(file, 'w') as outfile:
            json.dump(data, outfile)

    @staticmethod
    def __create_dict(json: List[Dict]) -> Dict:
        """Create dict key:name, value: whole json"""
        return {i[Client.KEY_NAME]: i for i in json}

    @staticmethod
    def __remove(d: Dict, names: List[str]) -> None:
        """ Removes entries from a dict"""
        if names is None:
            d.clear()
            return
        """ Remove entries by name"""
        for i in names:
            if i in d:
                del d[i]

    @staticmethod
    def __get(url: str, section: str = PARAMETER) -> "Client":
        """HTTP GET to generate a Client"""
        response = requests.get(url, allow_redirects=True)
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
        response_json = response.json()

        # print(json_response)
        # check if suid error happens
        # This handles  /q/<suid>
        data = {} if not section in response_json else response_json[section]
        return Client(data, metainfo=response_json[Client.METAINFO])

    @staticmethod
    def from_file(file) -> "Client":
        """Create a client from a file"""
        d = Client.load_json(file)
        data = d[Client.PARAMETER]
        mi = d[Client.METAINFO]
        return Client(data, mi)

    @staticmethod
    def load(file: str, section: str = PARAMETER) -> "Client":
        """Use a json file to create a client"""
        if not path.exists(file):
            raise Exception("File not found")

        with open(file) as json_file:
            response_json = json.load(json_file)

        # print(json_response)
        # check if suid error happens
        data = {} if not section in response_json else response_json[section]
        return Client(data, metainfo=response_json[Client.METAINFO])

    @staticmethod
    def get_catalog(url: str) -> List['Client']:
        """ Get the list of services fron an endpoint"""

        response = requests.get(url, allow_redirects=True)
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
        response_json = response.json()
        return [Client(metainfo=service) for service in response_json]

    @staticmethod
    def get_capabilities(c) -> "Client":
        """Get the parameter of a service. Creates a request Client"""
        if isinstance(c, str):
            return Client.__get(c)
        if isinstance(c, Client):
            url = c.get_url()
            if url is None:
                raise Exception("No url info in client argument")
            cl = Client.__get(url)
            c.add_all_metainfo(cl)
            c.add_data(cl)
            return c
        raise Exception("Illegal argument type: " + type(c))

    def pubsub(self, url: str, callback=None, extra_metainfo: Dict = None) -> None:
        """Publish/subscribe execution """

        def cb(client: 'Client', file: str, counter: int):
            pass

        callback = callback or cb

        if not hasattr(self, "webhook"):
            raise Exception("No webhook provided.")
        if not hasattr(self, "files"):
            raise Exception("No request files provided.")

        # convert into tuple when only one webhook is given
        if isinstance(self._webhook, str):
            self._webhook = (self._webhook,)

        webhook_count = len(self.webhook)

        header = {}
        if hasattr(self, "bearertoken"):
            header["Authorization"] = 'Bearer ' + self.bearertoken

        for i, file in enumerate(glob.iglob(self._files)):
            if i + 1 < self._batch[0]:
                continue  # before min
            if i + 1 <= self._batch[1]:  # within range
                header[Client.HDR_CSIP_REQUESTFILE] = Path(file).name
                header[Client.HDR_CSIP_WEBHOOK] = self.webhook[i % webhook_count]
                c = Client.from_file(file)
                if extra_metainfo is not None:
                    c.add_metainfo(extra_metainfo)
                resp = c.execute(url, True, None, header)
                callback(resp, file, i + 1)
                if self._delay > 0:
                    sleep(self._delay / 1000)
            else:
                break  # after max, we are done

    def execute(self, url: str = None, sync: bool = True, files: List[str] = None, headers: Dict = None) -> 'Client':
        """Executes a service as HTTP/POST. This method returns when service is finished if sync
           argument is set to True (default). Creates a reponse client.
           Use execute_async to call a service asynchronously.
        """
        self.metainfo[self.META_KEY_MODE] = self.META_VAL_SYNC if sync else self.META_VAL_ASYNC
        request_json = {self.METAINFO: self.metainfo, self.PARAMETER: list(self.data.values())}

        multipart = {self.REQ_PARAM: (self.REQ_JSON, json.dumps(request_json))}
        for i, file in enumerate(files or [], start=1):
            if not os.path.exists(file):
                Exception("Not found: " + file)
            if os.path.isdir(file):
                file = make_archive(file, 'zip', file)
            multipart[self.REQ_FILE + str(i)] = open(file, 'rb')

        if url is None:
            url = self.get_url()
            if url is None:
                raise Exception('No url provided.')
        # print(multipart)

        response = requests.post(url, files=multipart, allow_redirects=True, headers=headers)

        if response.status_code != requests.codes.ok:
            response.raise_for_status()

        response_json = response.json()

        # print(response_json)
        # async handling
        data = {} if not self.RESULT in response_json else response_json[self.RESULT]
        return Client(data, parent=self, metainfo=response_json[self.METAINFO])

    def execute_async(self, url: str = None, files: List[str] = None,
                      first_poll: int = None, next_poll: int = None,
                      callback=None) -> 'Client':
        """Executes a service as HTTP/POST. This method runs the service asynchronously and
           returns when the service is done. It 'pings' the service run for completion in the
           frequency provided by 'fist_poll' and 'next_poll'. Provide a callback method to capture
           the query results.
           
           Creates a reponse client.
           Use execute to call a service synchronously.
           
           :first_poll: time in milli sec to poll the first time
           :next_poll: time in milli sec to poll from then on
        """
        if first_poll is not None and first_poll < 2000:
            raise Exception("first_poll must be greater that 2000")
        if next_poll is not None and next_poll < 2000:
            raise Exception("next_poll must be greater that 2000")

        def cb(c: 'Client', progress: str):
            pass

        callback = callback or cb

        # -> Submitted
        resp = self.execute(url, files=files, sync=False)
        callback(resp, "")

        fp = (first_poll or resp.get_first_poll()) / 1000
        np = (next_poll or resp.get_next_poll()) / 1000

        if fp < 2.0:
            fp = 2.0

        if np < 2.0:
            np = 2.0

        sleep(fp)

        # Submitted -> Running
        r = resp.query_execute()
        progress = r.get_progress()
        callback(r, progress)
        while r.get_status() == Client.STATUS_RUNNING:
            sleep(np)
            # Running -> Running | Finished | Failed
            r = resp.query_execute()
            progress = r.get_progress()
            callback(r, progress)
        return r

    def query_execute(self, suid: str = None) -> 'Client':
        """Queries the service execution for completion status. 
           The service must run in 'async' mode"""

        if suid is not None:
            # skip ckecking the async mode
            if not self.is_async():
                raise Exception("not async.")
        service = self.get_service_url()
        if service is None:
            raise Exception("no service_url.")
        a = re.search("/[md]/", service)
        if a is None:
            raise Exception("not a model/data service_url.")

        suid = suid or self.get_suid()
        if suid is None:
            raise Exception("no suid.")
        query_url = service[:a.start()] + "/q/" + suid
        # print(query_url)
        c = Client.__get(query_url, section=self.RESULT)
        c.parent = self
        return c

    #### files handling

    def get_data_files(self) -> List[str]:
        """Get a list of data entries that are file urls to download"""
        suid = self.get_suid()
        if suid is None:
            raise Exception("Not a response, nothing to download.")

        files = []
        for name in self.data:
            val = self.get_data_value(name)
            if isinstance(val, str) and ("/q/" + suid + "/") in val and val.endswith(name):
                files.append(name)
        return files

    def download_data_files(self, files: List[str] = None, dir: str = ".") -> None:
        """ Downloads file(s) if this Client object is a valid response and a query url as value.
            If no 'file' argument is provided, all files will be dowloaded.
            If no 'dir' is provided, the current directory will be used.
        """
        if files is None or not files:
            return

        dir = os.path.abspath(dir)
        if not os.path.isdir(dir):
            raise Exception("Not a folder or does not exist: " + dir)

        suid = self.get_suid()
        if suid is None:
            raise Exception("No suid.")

        print("downloading to '" + dir + "':")
        for name in files:
            if name not in self.data:
                raise Exception("Not in data: " + name)
            val = self.get_data_value(name)
            print("  --> " + name)
            r = requests.get(val, allow_redirects=True)
            open(os.path.join(dir, name), "wb").write(r.content)

    #### pubsub related properties

    @property
    def bearertoken(self) -> str:
        return self._bearertoken

    @bearertoken.setter
    def bearertoken(self, token: str) -> None:
        self._bearertoken = token

    @property
    def webhook(self) -> Tuple:
        return self._webhook

    @webhook.setter
    def webhook(self, hook: Tuple) -> None:
        self._webhook = hook

    @property
    def files(self) -> str:
        """For pubsub"""
        return self._files

    @files.setter
    def files(self, f: str) -> None:
        """For pubsub"""
        self._files = f

    @property
    def batch(self) -> Tuple:
        """For pubsub"""
        return self._batch

    @batch.setter
    def batch(self, b: Tuple) -> None:
        """For pubsub"""
        assert b[0] < b[1], "Invalid batch range"
        self._batch = b

    @property
    def delay(self) -> int:
        """Get the delay between p/s submissions in ms"""
        return self._delay

    @delay.setter
    def delay(self, d: int) -> None:
        """Set the delay between p/s submissions in ms"""
        self._delay = d

    #### metainfo

    def get_metainfo(self, name: str) -> str:
        """Get a metainfo entry"""
        return self.metainfo.get(name, None)

    def set_metainfo(self, name: str, value: str) -> None:
        """Set a metainfo entry"""
        self.metainfo[name] = value

    def add_metainfo(self, d: Dict) -> None:
        """Add a dict as metainfo"""
        self.metainfo.update(d)

    def get_metainfo_names(self) -> List[str]:
        """Get all the entry names"""
        return list(self.metainfo.keys())

    def has_metainfo(self, name: str) -> bool:
        """Check if data entry exists """
        return name in self.metainfo

    def add_all_metainfo(self, csip: "Client") -> None:
        """Add all entries from the other Client"""
        self.metainfo = csip.metainfo.copy()

    def remove_metainfo(self, names: List[str] = None) -> None:
        """Remove metainfo entries by names, or all if name is None"""
        Client.__remove(self.metainfo, names)

    def metainfo_tostr(self, indent: int = 2) -> str:
        """Print the metainfo  """
        return json.dumps(self.metainfo, indent=indent)

    #### data

    def get_data_attr(self, name: str, key: str) -> str:
        """Get the entry value for any key"""
        return self.data[name].get(key, None)

    def set_data_attr(self, name: str, key: str, value: str) -> None:
        """Add a metainfo entry to data"""
        self.data[name][key] = value

    def remove_data(self, names: List[str] = None) -> None:
        """Remove data entries by names, or all if name is None"""
        Client.__remove(self.data, names)

    def get_data_names(self) -> List[str]:
        """Get all the entry names"""
        return list(self.data.keys())

    def set_data_value(self, name: str, value: object) -> None:
        """Set a value on an existing data entry without changing anything else.
            The entry must exist"""
        self.data[name][self.KEY_VALUE] = value

    def add_data(self, name, value=None, descr: str = None, unit: str = None, geometry_type: str = None, coord: [] = None) -> None:
        """Add a new entry to the data"""
        if isinstance(name, Dict):
            # name is the the json data object 
            self.data[name[Client.KEY_NAME]] = name
            return
        if isinstance(name, Client):
            # name is the CSIP data object 
            self.data = {**self.data, **name.data}
            return
        if value is None:
            raise Exception("missing value.")
        self.data[name] = {self.KEY_NAME: name, self.KEY_VALUE: value}
        if unit is not None:
            self.data[name][self.KEY_UNIT] = unit
        if descr is not None:
            self.data[name][self.KEY_DESCRIPTION] = descr
        if geometry_type is not None:
            self.data[name][self.KEY_TYPE] = geometry_type
        if coord is not None:
            self.data[name][self.KEY_COORD] = coord

    def has_data(self, name: str) -> bool:
        """Check if data entry exists """
        return name in self.data

    def get_data(self, name: str) -> Dict:
        """Get the whole entry as dict"""
        return self.data.get(name, {})

    def get_data_value(self, name: str, def_value=None) -> object:
        """Get the entry value """
        return self.get_data(name).get(self.KEY_VALUE, def_value)

    def get_data_description(self, name: str) -> str:
        """Get the entry description"""
        return self.get_data(name).get(self.KEY_DESCRIPTION, None)

    def get_data_unit(self, name: str) -> str:
        """Get the data unit"""
        return self.get_data(name).get(self.KEY_UNIT, None)

    def data_tostr(self, indent: int = 2) -> str:
        """Print the entries as json"""
        return json.dumps(list(self.data.values()), indent=indent)

    #### metainfo content mapping

    def get_parent(self) -> "Client":
        """Get the parent data set, which is the request """
        return self.parent

    def get_url(self) -> str:
        """Get the url"""
        return self.metainfo.get(self.META_KEY_SERVICE_URL, None)

    def get_name(self) -> str:
        """Get the name of the service"""
        return self.metainfo.get(self.KEY_NAME, None)

    def get_description(self) -> str:
        """Get the description of the service"""
        return self.metainfo.get(self.KEY_DESCRIPTION, None)

    def get_status(self) -> str:
        """Get the status from metainfo, returns None is there is none """
        return self.metainfo.get(self.META_KEY_STATUS, None)

    def get_suid(self) -> str:
        """Get the simulation id (suid) from metainfo, returns None is there is none """
        return self.metainfo.get(self.META_KEY_SUID, None)

    def get_service_url(self) -> str:
        """Get the service url from metainfo, returns None is there is none """
        return self.metainfo.get(self.META_KEY_SERVICE_URL, None)

    def get_error(self) -> str:
        """Get the error message from metainfo, returns None is there is none """
        return self.metainfo.get(self.META_KEY_ERROR, None)

    def get_progress(self) -> str:
        return self.metainfo.get(self.META_KEY_PROGRESS, None)

    def get_stacktrace(self) -> List[str]:
        """Get the error stacktrace from metainfo, returns None is there is none """
        return self.metainfo.get(self.META_KEY_STACKTRACE, None)

    def get_mode(self) -> str:
        """Get the execution mode from metainfo, returns 'sync' or 'async' , default is sync"""
        return self.metainfo.get(self.META_KEY_MODE, self.META_VAL_SYNC)

    def is_async(self) -> bool:
        """Check if execution mode is async """
        return self.metainfo.get(self.META_KEY_MODE, self.META_VAL_SYNC) == self.META_VAL_ASYNC

    def get_first_poll(self) -> int:
        return self.metainfo.get(self.META_KEY_FIRST_POLL, 2000)

    def get_next_poll(self) -> int:
        return self.metainfo.get(self.META_KEY_NEXT_POLL, 2000)

    #### printing support

    def get_entry_asstr(self, name) -> str:
        d = self.get_data_description(name)
        if d is not None:
            d = " (" + d + ")"
        else:
            d = ""
        u = self.get_data_unit(name)
        if u is not None:
            u = " [" + u + "]"
        else:
            u = ""

        v = self.get_data_value(name)
        v = json.dumps(v, indent=2).replace("\n", "\n       ")

        return ("  " + name + d + "\n" + "      " + v + u + "\n")

    def get_entries_asstr(self) -> str:
        s = ""
        for i in self.get_data_names():
            s += self.get_entry_asstr(i)
        return s

    def __str__(self):
        """String representation."""
        return (
            "SERVICE: '{name}' \n url: {url}\n description: {description}\n parent: {parentsuid} \n metainfo: {metainfo}\n data:\n{data}".format(
                name=self.get_name(), suid=self.get_suid(), url=self.get_url(),
                description=self.get_description(),
                parentsuid=(self.parent.get_suid() if self.parent is not None else 'None'),
                metainfo=self.metainfo_tostr(indent=2).replace("\n", "\n           "), data=self.get_entries_asstr()))
