import datetime
import os
import re
import subprocess
from .threads import CommonThread
from PIL import Image


class Scaner:
    ALLOWED_PARAMS = ["format", "mode", "resolution", "type"]
    ALLOWED_FILETYPES = ["jpg", "jpeg", "png", "tiff", "tif"]

    STATUS_ERROR = "error"
    STATUS_READY = "ready"
    STATUS_PROCESSING = "processing"

    def __init__(self, scans_path: str):
        self._scaner_device = ""
        self._scaner_device_name = ""
        self._command = ""
        self._console = ""
        self._scans_path = scans_path
        self._scan_thread = None  # type: CommonThread

    @property
    def scaner_device(self) -> str:
        if not self._scaner_device:
            self.detect_scaner_device()
        return self._scaner_device

    @property
    def scaner_device_name(self) -> str:
        if not self._scaner_device_name:
            self.detect_scaner_device()
        return self._scaner_device_name

    def reinit_scaner_device(self) -> str:
        self._scaner_device = None
        self._scaner_device_name = None
        return self.scaner_device

    def get_scan_status(self) -> dict:
        ret = {
            "status": self.STATUS_READY if self.scaner_device else self.STATUS_ERROR,
            "scanerDevice": self.scaner_device or "No scaner device found",
            "scanerDeviceName": self.scaner_device_name,
            "command": self._command,
            "console": self._console
        }
        self._command = ""
        self._console = ""
        if self._scan_thread:
            if self._scan_thread.thread_finished:
                self._scan_thread = None
            else:
                ret["status"] = self.STATUS_PROCESSING
        return ret

    def detect_scaner_device(self) -> bool:
        self._command = "scanimage -L"
        subp = subprocess.Popen(self._command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        self._console = subp.communicate()[0].decode("utf-8")
        results = re.search(r"^device .([^']*). is a (.*)", self._console)
        if results and len(results.groups()) == 2:
            self._scaner_device = results.group(1)
            self._scaner_device_name = results.group(2)
            return True
        return False

    def scan_image(self, file_name: str, scan_params: dict) -> bool:
        if self.get_scan_status().get("status") == self.STATUS_READY:
            self._scan_thread = CommonThread("scan", self._scan_image, {"file_name": file_name, "scan_params": scan_params})
            self._scan_thread.start()
            return True
        return False

    def _scan_image(self, file_name: str, scan_params: dict):
        file_path = os.path.join(self._scans_path, file_name)
        cmd_params = self._complete_params(scan_params)
        self._command = "scanimage --device {} {} > {}".format(self.scaner_device, cmd_params, file_path)
        subp = subprocess.Popen(self._command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        self._console = subp.communicate()[0].decode("utf-8")

    @staticmethod
    def _get_file_info(file_path: str) -> dict:
        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            return {
                "fileName": file_name,
                "fileExt": os.path.splitext(file_name)[1],
                "size": os.path.getsize(file_path),
                "ctime": "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.fromtimestamp(os.path.getctime(file_path))),
                "error": 0
            }
        return {"error": 1}

    def get_file_list(self) -> list:
        ret = []
        files = os.listdir(self._scans_path)
        for file in files:
            file_path = os.path.join(self._scans_path, file)
            ret.append(self._get_file_info(file_path))
        ret.sort(key=lambda item: item.get("fileName"))
        return ret

    def get_preview_file_path(self, preview_filename: str) -> str:
        filepath = os.path.join(self._scans_path, preview_filename)
        if os.path.exists(filepath):
            return preview_filename
        return ""

    def delete_file(self, file_name):
        """
        Delete file or all files in directory
        :param file_name: Filename or * to teleto all
        :return: List of removed files
        :rtype: list
        """
        removed = []
        if file_name == "*":
            file_list = os.listdir(self._scans_path)
        else:
            file_list = [file_name]

        for file in file_list:
            file_path = os.path.join(self._scans_path, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                removed.append(file)
        return removed

    def crop_image(self, file_name: str, x1: int, y1: int, x2: int, y2: int) -> bool:
        file_path = os.path.join(self._scans_path, file_name)
        img = Image.open(file_path)
        img_cropped = img.crop((int(x1), int(y1), int(x2), int(y2)))
        img_cropped.save(file_path)
        return True

    def rotate_image(self, file_name: str, angle: int) -> int:
        file_path = os.path.join(self._scans_path, file_name)
        img = Image.open(file_path)
        img_rotated = img.rotate(int(angle), expand=True)
        img_rotated.save(file_path)
        return angle

    def _complete_params(self, params: dict) -> str:
        filtered_params = {key: value for key, value in params.items() if key in self.ALLOWED_PARAMS}
        complete_params = ["--{} \"{}\"".format(key, value) for key, value in filtered_params.items()]
        return " ".join(complete_params)
