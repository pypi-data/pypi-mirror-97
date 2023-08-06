class App {
	/**
	 * @param jQueryInstance: Object
	 * @param mainCOntainerId: String
	 * @param config: Object
	 */
	constructor(jQueryInstance, mainCOntainerId, config){
		this.$ = jQueryInstance;
		this.$mainContainer = this.$(`#${mainCOntainerId}`);
		this.config = config;
		this.config.formatChoices = [
			["jpeg", "JPEG"],
			["png", "PNG"],
			["tiff", "TIFF"],
			["pnm", "PNM"],
		];
		this.config.modeChoices = [
			["Color", "Color"],
			["Gray", "Gray"],
			["Lineart", "Lineart"],
		];
		this.config.resolutionChoices = [
			["600", "600 dpi"],
			["300", "300 dpi"],
			["150", "150 dpi"],
			["200", "200 dpi"],
			["100", "100 dpi"],
			["96", "96 dpi"],
			["75", "75 dpi"],
		];
		this.config.scanerStatusReady = "ready";
		this.config.scanerStatusProcessing = "processing";
		this.config.scanerStatusError = "error";
		this._lastAppStatus = "";
		this._interval = null;
		this._imagePreviewFileName = "";
		this._scanCroppr = null;
		this._scanCropData = [];
		this.config.scanerWidthPx = this.$mainContainer.find("#scan-preview").width();
		this.config.scanerHeightPx = this.$mainContainer.find("#scan-preview").height();
		this.config.scanerWidthMM = 210;
		this.config.scanerHeightMM = 297;

		this._renderUI();
		this._initUI();
		this._renderImageList();
	}

	_renderUI(){
		let ui = `
		<div class="scan">
			<fieldset>
				<legend>Scan preview</legend>
				<div id="scan-preview"></div>
			</fieldset>
			<fieldset>
				<legend>Scan controls</legend>
				<div class="flex-row-container">
					<div class="scan-controls flex-row-item">
						<div><label for="scan-control-select-format">Image file format:</label><select id="scan-control-select-format"></select></div>
						<div><label for="scan-control-select-mode">Image mode</label><select id="scan-control-select-mode"></select></div>
						<div><label for="scan-control-select-resolution">Image resolution</label><select id="scan-control-select-resolution"></select></div>
						<div><button id="scan-control-btn-preview">Scan preview</button></div>
						<div><button id="scan-control-btn-scan">Scan</button></div>
						<div><button id="scan-control-btn-scan-reinit">Reinit scanner</button></div>
						<div><button id="scan-control-btn-rotate-image-left">Rotate image left</button></div>
						<div><button id="scan-control-btn-rotate-image-right">Rotate image right</button></div>
						<div><button id="scan-control-btn-crop-image">Crop image</button></div>
						<div id="scan-preview-crop-info"></div>
					</div>
					<div class="flex-row-item">
						<div id="scan-control-status"></div>
					</div>
				</div>
			</fieldset>
		</div>
			<fieldset>
			<legend>Scaned images</legend>
			<div id="scaned-images"></div>
			<div class="clean"></div>
			<div id="scaned-images-buttons">
				<button id="images-button-delete-all">Delete all images</button>
			</div>
		</fieldset>
		<fieldset>
			<legend>Status [<span id="status"></span>]</legend>
			<div class="history">
				<div>
					<fieldset>
						<legend>Command history</legend>
						<code id="status-command-history"></code>
					</fieldset>
				</div>
				<div>
					<fieldset>
						<legend>Console history</legend>
						<code id="status-console-history"></code>
					</fieldset>
				</div>
			</div>
		</fieldset>`
		this.$mainContainer.html(ui);
	}

	_initUI(){
		Form.setSelectOptions("scan-control-select-format", this.config.formatChoices);
		Form.setSelectOptions("scan-control-select-mode", this.config.modeChoices);
		Form.setSelectOptions("scan-control-select-resolution", this.config.resolutionChoices);
		this.$("#scan-control-btn-preview").click(()=>{
			this._runScanPreview();
			this._startGetAppStatusInterval();
		});

		this.$("#scan-control-btn-scan").click(()=>{
			this._runScan();
			this._startGetAppStatusInterval();
		});

		this.$("#scan-control-btn-scan-reinit").click(()=>{
			this._reinitScanner();
		});

		this.$mainContainer.find("#scan-control-btn-crop-image").click(()=>{
			this._scanCroppr = new Croppr(
				`#scan-preview img.content`,
				{
					startSize: [100, 100, "%"],
					onCropMove: (value) => {
						this._scanCropData = [value.x, value.y, value.x + value.width, value.y + value.height];
						this._renderScanCropData();
					}
				}
			);
		});

		this.$mainContainer.find("#scan-control-btn-rotate-image-left").click(()=>{
			this._callApi("rotateImage",
				{"filename": this._imagePreviewFileName, "angle": 90},
				(data)=>{
					this._renderImagePreview();
					this._renderImageList();
				})
		});

		this.$mainContainer.find("#scan-control-btn-rotate-image-right").click(()=>{
			this._callApi("rotateImage",
				{"filename": this._imagePreviewFileName, "angle": 270},
				(data)=>{
					this._renderImagePreview();
					this._renderImageList();
				})
		});

		this.$mainContainer.find("#images-button-delete-all").click(()=>{
			this._callApi("deleteImage",
				{"filename": "*"},
				(data)=>{
					this._renderImageList();
				})
		});

		this.$(window).on("appStatusChanged", (event, status)=>{
			if(status == this.config.scanerStatusReady) {
				this._stopGetAppStatusInterval();
				this._renderImagePreview();
				this._renderImageList();
			}
		});
	}
	
	_getAppStatus(){
		this._callApi("scanStatus", {}, (data)=>{
			if(data.status) {
				if(this._lastAppStatus != data.status) {
					this.$(window).trigger("appStatusChanged", [data.status]);
				}
				if(data.status == this.config.scanerStatusError){
					this._stopGetAppStatusInterval();
				}
				this.$mainContainer.find("#status,#scan-control-status").text(data.status);
				this._lastAppStatus = data.status;
			}
			if(data.command) this.$mainContainer.find("#status-command-history").append(`<div>${data.command}</div>`);
			if(data.console) this.$("#status-console-history").append(`<div>${data.console}</div>`);
		});
	}
	
	_startGetAppStatusInterval(){
		this._interval = window.setInterval(()=>{
				this._getAppStatus();
			}, 4000);
	}
	
	_stopGetAppStatusInterval(){
		if(this._interval) {
			window.clearInterval(this._interval);
			this._interval = null;
		}
	}

	_runScanPreview(){
		this._callApi("scanPreview", {}, (data)=>{
			this._imagePreviewFileName = data["filename"];
			this._getAppStatus();
		});
	}

	_runScan(){
		let mode = Form.getSelectSelectedOptionValue("scan-control-select-mode");
		let format = Form.getSelectSelectedOptionValue("scan-control-select-format");
		let resolution = Form.getSelectSelectedOptionValue("scan-control-select-resolution");
		this._callApi("scanImage", {"mode": mode, "format": format, "resolution": resolution}, (data)=>{
			this._imagePreviewFileName = data["filename"];
			this._getAppStatus();
		});
	}

	_reinitScanner(){
		this._callApi("initScanner", {}, (data)=>{
		});
	}

	_getScanPreviewFileName(){
		this._callApi("getPreviewImage", {}, (data)=> {
			if (data) {
				this._imagePreviewFileName = data["filename"];
				this._renderImagePreview();
			}
		});
	}


	_renderImagePreview(){
		let rnd = Math.random();
		let container = this.$mainContainer.find(`#scan-preview`);
		let filepath = `${this.config.scanedImagesURL}/${this._imagePreviewFileName}`;
		let imageHTML = `<img class="content" src="${filepath}?${rnd}"/>`;
		container.html(imageHTML);
	}

	_renderImageList(){
		this._callApi("listImages", {}, (data)=>{
			if(data){
				let rnd = Math.random();
				let container = this.$mainContainer.find("#scaned-images"); 
				container.empty();
				for(let index in data) {
					let item = data[index];
					let filename = item.fileName;
					let filepath = `${this.config.scanedImagesURL}/${filename}`;
					let fileSize = Utils.formatFileSize(item.size);
					let imageHTML =
						`<div class="image-container">` +
							`<div class="image">` +
								`<img src="${filepath}?${rnd}"/>` +
							`</div>` +
							`<div class="decs-container">` +
								`<div class="image-desc">` +
									`<div class="filename">${item.fileName}</div><div class="filesize">${fileSize}</div>` +
								`</div>` +
								`<div class="image-buttons">` +
									`<button class="image-button-edit" data-filename="${filename}">Edit</button>` +
									`<button class="image-button-delete" data-filename="${filename}">Delete</button>` +
								`</div>` +
							`</div>` +
						`</div>`
					container.append(imageHTML);
				}
				// add buttons handlers
				this.$mainContainer.find(".image-button-edit").click((event)=>{
					let filename = event.target.getAttribute("data-filename");
					this._imagePreviewFileName = filename;
					this._renderImagePreview();
				});
				this.$mainContainer.find(".image-button-delete").click((event)=>{
					let filename = event.target.getAttribute("data-filename");
					this._callApi("deleteImage", {filename: filename}, (data)=>{this._renderImageList()})
				});
			}
		});
	}

	_renderScanCropData(){
		let container = this.$mainContainer.find("#scan-preview-crop-info");
		container.empty();
		if(this._scanCropData){
			let x1 = this._scanCropData[0];
			let y1 = this._scanCropData[1];
			let x2 = this._scanCropData[2];
			let y2 = this._scanCropData[3];
			let content = `<button id="scan-control-btn-crop-coord">Apply image crop: [${x1}, ${y1}] [${x2}, ${y2}]</button>`;
			container.html(content);
			container.find("#scan-control-btn-crop-coord").click(()=>{
				this._cropImage(x1, y1, x2, y2);
			});
		}
	}
	
	_cropImage(x1, y1, x2, y2){
		this._callApi("cropImage", {"filename": this._imagePreviewFileName, "x1": x1, "y1": y1, "x2": x2, "y2": y2 }, (data)=>{
			let container = this.$mainContainer.find("#scan-preview-crop-info");
			container.html("");
			this._renderImagePreview();
			this._renderImageList();
		})
	}

	_callApi(command, params = {}, callback = null){
		let _this = this;
		let getParams = URL.convertParams(params);
		let apiCall = getParams == "" ? `${this.config.apiURL}/${command}` : `${this.config.apiURL}/${command}?${getParams}`;
		this.$.ajax({
			url: apiCall, 
			success: (data)=>{
				if(callback) callback(data);
			}
		});
	}

}
