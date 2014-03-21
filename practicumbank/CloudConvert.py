import requests
import time
import json


class CloudConvert():
    """
    Low level interface to the CloudConvert service
    """

    def __init__(self, apikey):
        pass

    @staticmethod
    def start(inputformat, outputformat, apikey):
        """
        Inits the process in the remote server
        """
        url = (
            "https://api.cloudconvert.org/process?"
            "inputformat={inputf}&outputformat={outputf}&apikey={api}"
            ).format(
            inputf=inputformat,
            outputf=outputformat,
            api=apikey)

        dictstarter = requests.get(url).text[1:-1].split(",")
        pairs={}
        for pair in dictstarter:
            x,y=pair.split(":",1)
            pairs[x.replace("\"","")]=y.replace("\"","")
        return pairs

    @staticmethod
    def upload(fname, outformat, pid, host, options=None):
        """
        Uploads a file to be converted
        """
        url = (
            "https://{host}/process/{pid}"
            ).format(pid=pid,
                     host=host)

        if options is None:
            options = {}  # TODO

        with open(fname, "rb") as f:
            requests.post(url,
                          data={
                              "outputformat": outformat,
                              "input":"upload"
                              },
                          files={
                              "file": f},
                          verify=False)

    @staticmethod
    def status(pid, host):
        """
        Checks the conversion status of a process
        """
        url = (
            "https://{host}/process/{pid}"
            ).format(pid=pid,
                     host=host)

        dictstarter = requests.get(url, verify=False).text.replace(" ","").replace("\n","").replace("\t","")
        return json.loads(dictstarter)
        #=======================================================================
        # print dictstarter
        # pairs={}
        # for pair in dictstarter:
        #     x,y=pair.split(":",1)
        #     pairs[x.replace("\"","").strip()]=y.replace("\"","").strip()
        # print pairs
        # return pairs
        #=======================================================================

    @staticmethod
    def download(pid, host):
        """
        Returns a file-like object containing the file
        """
        url = "https:" + CloudConvert.status(pid, host)["output"]["url"]

        return requests.get(url, verify=False).raw

    @staticmethod
    def cancel(pid, host):
        """
        Cancels the conversion methon ath any point.
        Currently there is no way of resuming
        """
        url = (
            "https://{host}/process/{pid}/cancel"
            ).format(pid=pid,
                     host=host)

        requests.get(url,
                     verify=False)

    @staticmethod
    def delete(pid, host):
        """
        Deletes files of a conversion process
        """
        url = (
            "https://{host}/process/{pid}/delete"
            ).format(pid=pid,
                     host=host,
                     verify=False)

        requests.get(url)

    @staticmethod
    def list(apikey):
        """
        Returns the history of the conversions of the supplied apikey.
        """

        url = (
            "https://api.cloudconvert.org/processes?apikey={api}"
            ).format(api=apikey)

        return requests.get(url).json()

    @staticmethod
    def conversion_types(inputformat=None, outputformat=None):
        """
        Returns a dict with all te possible conversions and
        conversion specific options.

        Arguments:
            inputformat(str) -> input format to lookup [optional]
            outputformat(str) -> outpu format to lookup [optional]
        """
        kwargs = {"inputformat": inputformat,
                  "outputformat": outputformat}

        url = "https://api.cloudconvert.org/conversiontypes"

        if inputformat or outputformat:
            toappend = [param+"="+kwargs[param]
                        for param in kwargs
                        if kwargs[param] is not None]
            url += "?" + "&".join(toappend)

        return requests.get(url).json()


class ConversionProcess():
    def __init__(self, apikey):
        self.apikey = apikey

        self.pid = None
        self.host = None

        self.fromfile = None
        self.fromformat = None

        self.tofile = None
        self.toformat = None

    def _get_format(self, f):
        return f.split(".")[-1]

    def init(self, fromfile, tofile):
        """
        Prepares the conversion
        """
        self.fromfile = fromfile
        self.tofile = tofile

        # If this doesn't get resolved right,
        # user has to provide the correct ones.
        self.fromformat = self._get_format(fromfile)
        self.toformat = self._get_format(tofile)

        j = CloudConvert.start(self.fromformat, self.toformat, self.apikey)
        self.pid = j["id"]
        self.host = j["host"]

        return self.pid

    def start(self):
        """
        Uploads the file hence starting the conversion process
        """
        CloudConvert.upload(self.fromfile, self.toformat, self.pid, self.host)

    def status(self):
        """
        Returns the status of the process
        """
        # TODO: Make it more beautiful, not just raw json response
        return CloudConvert._status(self.pid, self.host)

    def cancel(self):
        """
        Cancels the process. Currently there is no way of resuming.
        """
        CloudConvert.cancel(self.pid, self.host)

    def delete(self):
        """
        Deletes the files from the current process.

        Note: files will get automatically deleted after a fixed period of time
            available trough status()
        Note: if the process is alredy running, it's first cancelled
        """
        CloudConvert.delete(self.pid, self.host)

    def wait_for_completion(self, check_interval=1):
        """
        This blocks until the process status["step"] changes to "finished"
        when returns True or "error", in which case, returns False.

        Arguments:
            check_interval(int) -> seconds to wait between each check.
        """
        while True:
            time.sleep(check_interval)

            step = CloudConvert.status(self.pid, self.host)["step"]
            if step == "finished":
                return True
            elif step == "error":
                return False

    def download(self):
        """
        Returns a file-like object with the output file, fro download.
        """
        # File-like object
        return CloudConvert.download(self.pid, self.host)
