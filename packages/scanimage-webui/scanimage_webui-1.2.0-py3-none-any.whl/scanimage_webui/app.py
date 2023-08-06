import json
from flask import Flask, render_template, request, send_from_directory
from .libs.scanner import Scaner
from datetime import datetime


class App:
    PORT = 5000
    SCAN_FOLDER = ""
    app = Flask(__name__)
    scaner = None  # type: Scaner

    @classmethod
    def init(cls, scan_folder_path: str, port: int=5000):
        cls.PORT = port
        cls.SCAN_FOLDER = scan_folder_path
        cls.scaner = Scaner(cls.SCAN_FOLDER)
        print("Serving app at port: {}".format(port))

    @classmethod
    def run(cls):
        cls.app.run(host="0.0.0.0", port=cls.PORT)

    @staticmethod
    @app.route("/")
    def index() -> Flask.response_class:
        return render_template("index.html")

    @staticmethod
    @app.route("/scanimage/<path:filename>")
    def serve_scanimage_folder(filename: str):
        return send_from_directory(App.SCAN_FOLDER, filename, as_attachment=True)

    @staticmethod
    @app.route('/api/scanStatus')
    def scan_status() -> Flask.response_class:
        ret = App.scaner.get_scan_status()
        if ret:
            return App.response_json(ret)
        return App.response500("Error getting scaner status")

    @staticmethod
    @app.route('/api/initScanner')
    def init_scaner():
        ret = App.scaner.reinit_scaner_device()
        if ret:
            return App.response_json(ret)
        return App.response500("Error getting scaner status")

    @staticmethod
    @app.route('/api/scanImage', methods=["GET"])
    def scan_image() -> Flask.response_class:
        """
        GET PARAMS:
        str format: jpg, png, tif
        str mode: Color, Gray, Lineart
        int resolution: 96, 200, 300, 600
        :return: { result: true/
        """
        args = request.args
        format_ = args.get("format", "jpg")
        params = {
            "mode": args.get("mode", "Color"),
            "format": args.get("format", "jpg"),
            "resolution": args.get("resolution", "300")
        }
        base_filename = "scan-{}".format(datetime.now().strftime("%Y%m%d-%H%M%S"))
        filename = "{}.{}".format(base_filename, format_)
        result = App.scaner.scan_image(filename, params)
        ret = {
            "result": result,
            "filename": filename
        }
        return App.response_json(ret)

    @staticmethod
    @app.route('/api/scanPreview', methods=["GET"])
    def scan_preview() -> Flask.response_class:
        filename = "scan-preview.jpeg"
        result = App.scaner.scan_image(filename, {"mode": "Color", "format": "jpeg", "resolution": "75"})
        ret = {
            "result": result,
            "filename": filename
        }
        return App.response_json(ret)

    @staticmethod
    @app.route('/api/getPreviewImage', methods=["GET"])
    def get_preview_image() -> Flask.response_class:
        return App.response_json({
            "filename": App.scaner.get_preview_file_path("scan-preview.jpeg")
        })

    @staticmethod
    @app.route('/api/listImages', methods=["GET"])
    def list_images() -> Flask.response_class:
        return App.response_json(App.scaner.get_file_list())

    @staticmethod
    @app.route('/api/deleteImage', methods=["GET"])
    def delete_image() -> Flask.response_class:
        """
        Avaliable GET args:
        str: filename - * delete all
        :return: 
        """
        args = request.args
        filename = args.get("filename")
        if filename:
            deleted = App.scaner.delete_file(filename)
            return App.response_json({"removed": deleted})
        else:
            return App.response404()

    @staticmethod
    @app.route('/api/cropImage', methods=["GET"])
    def crop_image():
        args = request.args
        filename = args.get("filename")
        x1 = args.get("x1")
        y1 = args.get("y1")
        x2 = args.get("x2")
        y2 = args.get("y2")
        result = App.scaner.crop_image(filename, x1, y1, x2, y2)
        return App.response_json({"result": result})

    @staticmethod
    @app.route('/api/rotateImage', methods=["GET"])
    def rotate_image():
        args = request.args
        filename = args.get("filename")
        angle = args.get("angle")
        result = App.scaner.rotate_image(filename, angle)
        return App.response_json({"result": result})


    @classmethod
    def response_json(cls, data: dict) -> Flask.response_class:
        if data is None:
            cls.response404()
        response = App.app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response

    @classmethod
    def response404(cls):
        response = cls.app.response_class(
            response={"message": "No data for your request"},
            status=404,
            mimetype='application/json'
        )
        return response

    @classmethod
    def response500(cls, message: str = ""):
        response = cls.app.response_class(
            response={"message": message},
            status=500,
            mimetype='application/json'
        )
        return response
