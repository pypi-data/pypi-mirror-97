
///<reference path="../../node_modules/@types/node/index.d.ts"/>

/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';

import { ProgressMessage } from './ProgressMessage';
import { Module, Status } from './Module';

import { ISignal, Signal } from '@lumino/signaling';

import { ServerConnection } from '@jupyterlab/services';

import { AppTracker } from './AppTracker';
import { OptumiMetadata } from './OptumiMetadata';
import { FileUploadMetadata } from './FileUploadMetadata';
import { Machine, NoMachine } from './machine/Machine';
import { Global } from '../Global';
import { InfoSkirt } from '../components/InfoSkirt';
import { StatusColor, StatusWrapper } from '../components/StatusWrapper';
import { IconButton, CircularProgress } from '@material-ui/core';

import ClearIcon from '@material-ui/icons/Clear';
import CheckIcon from '@material-ui/icons/Check';
import DeleteIcon from '@material-ui/icons/Delete';
import StopIcon from '@material-ui/icons/Stop';
import { DetailsDialog } from '../components/monitor/DetailsDialog';
import { Tag } from '../components/Tag';
import { Update } from './Update';
import { OutputFile } from './OutputFile';
import { Snackbar } from './Snackbar';
import WarningPopup from '../core/WarningPopup';
import FileServerUtils from '../utils/FileServerUtils';
import NotebookUtils from '../utils/NotebookUtils';
import FormatUtils from '../utils/FormatUtils';
import ExtraInfo from '../utils/ExtraInfo';

export enum Phase {
	Initializing = 'initializing',
	Uploading = 'uploading',
	Requisitioning = 'requisitioning',
	Running = 'running',
}
export class App {
	private _changed = new Signal<this, App>(this);

	get changed(): ISignal<this, App> {
		return this._changed;
	}

	private _notebook: any;
	// Extract this from the metadata so we don't have to parse it every time we check
	private _interactive: boolean;

	// Callback for module to add output to the notebook
	private formatForNotebook = (text: string[]) => {
		// We will not fix overwritten characters in the last line, in case the last line we have wipes out all the characters without writing new ones
		// We will leave the task of removing backspace characters from the last line to the component that renders the lines
		var lastLine = text.pop()
		// Remove overwritten characters and split into lines
		const formatted = NotebookUtils.fixOverwrittenChars(text).split('\n').map(x => x + '\n')
		// Remove the extra '\n'
		formatted[formatted.length-1] = formatted[formatted.length-1].substr(0, formatted[formatted.length-1].length-1);
		// Add the last line back
		formatted.push(lastLine);
		return formatted
	}

	private addOutput = (line: string, modifier: string) => {
		// We do not want to add output to the notebook for an interactive session
		if (!this._interactive) {
			// TODO:JJ If modifier is input, we can not parse it
			if (modifier == 'input') return;
			// TODO:JJ We could get the info that this line is error from either the modifier or the metadata
			try {
				const parsed = JSON.parse(line);
				const metadata = parsed.metadata;
				const outputs: any[] = this._notebook.cells[metadata.cell].outputs;
				// Ignore messages for markdown or raw cells
				if (this._notebook.cells[metadata.cell].cell_type != 'code') return;
				if (metadata.status) {
					if (metadata.status == 'started') {
						this._notebook.cells[metadata.cell].execution_count = '*';
					} else if (metadata.status == 'ended') {
						var count = 1;
						for (let i = 0; i < metadata.cell; i++) {
							if (this._notebook.cells[i].cell_type == ['code']) count++;
						}
						this._notebook.cells[metadata.cell].execution_count = count;
					}
				} else {
					if (modifier == 'output') {
						// We will write our other status updates to output
						if (outputs.length == 0 || outputs[outputs.length-1].name != 'stdout') {
							outputs.push({
								name: 'stdout',
								output_type: 'stream',
								text: this.formatForNotebook([parsed.text]),
							});
						} else {
							const text: string[] = outputs[outputs.length-1].text;
							text.push(parsed.text);
							outputs[outputs.length-1].text = this.formatForNotebook(text)
						}
					} else if (modifier == 'error') {
						// This could be a print to stderr (like a log message) or it could be a caught and formatted exception
						if (parsed.text) {
							if (outputs.length == 0 || outputs[outputs.length-1].name != 'stderr') {
								outputs.push({
									name: 'stderr',
									output_type: 'stream',
									text: this.formatForNotebook([parsed.text]),
								});
							} else {
								const text: string[] = outputs[outputs.length-1].text;
								text.push(parsed.text);
								outputs[outputs.length-1].text = this.formatForNotebook(text)
							}
						} else {
							outputs.push({
								"ename": parsed.ename,
								"evalue": parsed.evalue,
								"output_type": "error",
								"traceback": parsed.traceback,
							});
						}
					} else if (modifier == 'input') {
						// TODO:JJ
					} else {
						console.error('Unknown modifier' + modifier);
					}
				}
			} catch (err) {
				// Add this to the top cell as raw output
				if (this._notebook.cells[0].execution_count == null) {
					this._notebook.cells[0].execution_count = '*';
				}
				var outputs = this._notebook.cells[0].outputs;
				if (outputs.length == 0) {
					outputs.push({
						name: 'stdout',
						output_type: 'stream',
						text: this.formatForNotebook([line]),
					});
				} else {
					const text: string[] = outputs[outputs.length-1].text;
					text.push(line);
					outputs[outputs.length-1].text = this.formatForNotebook(text)
				}
			}
		}
	}

	private _name: string;
	private _uuid: string = "";
	private _modules: Module[] = [];

	private _initializing: ProgressMessage;
	private _uploading: ProgressMessage;
	private _requisitioning: ProgressMessage;
	private _running: ProgressMessage;

	private _timestamp: Date;

	// Polling timer
	private _polling: boolean;

	constructor(name: string, notebook: any, uuid: string = "",
		initializing: Update[] = [], uploading: Update[] = [], requisitioning: Update[] = [], running: Update[] = [], timestamp = new Date()) {		

		this._notebook = notebook;

		const optumi: OptumiMetadata = new OptumiMetadata(this._notebook["metadata"]["optumi"] || {});
		this._interactive = optumi.interactive;

		this._name = name;
		this._uuid = uuid;

		this._initializing = new ProgressMessage(Phase.Initializing, initializing);
		this._uploading = new ProgressMessage(Phase.Uploading, uploading);
		this._requisitioning = new ProgressMessage(Phase.Requisitioning, requisitioning);
		this._running = new ProgressMessage(Phase.Running, running);
		
		if (this._uuid != "") {
			this._initializing.appUUID = this._uuid;
			this._uploading.appUUID = this._uuid;
			this._requisitioning.appUUID = this._uuid;
			this._running.appUUID = this._uuid;
		}

		this._timestamp = timestamp;

		this._polling = false;

		// Handle errors where we were unable to load some of the updates
		if (this._running.started) {
			if (!this._requisitioning.completed) {
				this._requisitioning.addUpdate(new Update("Unable to retrieve requisitioning updates", ""));
				this._requisitioning.addUpdate(new Update("stop", ""));
			}
			if (!this._uploading.completed) {
				this._uploading.addUpdate(new Update("Unable to retrieve uploading updates", ""));
				this._uploading.addUpdate(new Update("stop", ""));
			}
			if (!this._initializing.completed) {
				this._initializing.addUpdate(new Update("Unable to retrieve initializing updates", ""));
				this._initializing.addUpdate(new Update("stop", ""));
			}
		} else if (this._requisitioning.started) {
			if (!this._uploading.completed) {
				this._uploading.addUpdate(new Update("Unable to retrieve uploading updates", ""));
				this._uploading.addUpdate(new Update("stop", ""));
			}
			if (!this._initializing.completed) {
				this._initializing.addUpdate(new Update("Unable to retrieve initializing updates", ""));
				this._initializing.addUpdate(new Update("stop", ""));
			}
		} else if (this._uploading.started) {
			if (!this._initializing.completed) {
				this._initializing.addUpdate(new Update("Unable to retrieve initializing updates", ""));
				this._initializing.addUpdate(new Update("stop", ""));
			}
		}

		// Handle some errors with requests failing while we get an application up and running
		if (initializing != null) {
			if (this._initializing.started && !this._initializing.completed) {
				if (this._initializing.message == "Compressing files...") this._initializing.total = -1;
				this.getCompressionProgress();
				return;
			}
		}

		if (uploading != null) {
			if (this._uploading.started && !this._uploading.completed) {
				this.getUploadProgress();
				return;
			}
		}

		if (requisitioning != null) {
			if (this._requisitioning.started && !this._requisitioning.completed) {
				if (this._requisitioning.message == "Waiting for cloud provider...") this._requisitioning.total = -1;
				return;
			}
		}
	}

	// Static function for generating an app from controller synchronization structure
	public static reconstruct(appMap: any): App {
		// Reconstruct the app
        const initializing: Update[] = [];
        for (let i = 0; i < appMap.initializing.length; i++) {
            initializing.push(new Update(appMap.initializing[i], appMap.initializingmod[i]));
        }
        const uploading: Update[] = [];
        for (let i = 0; i < appMap.uploading.length; i++) {
            uploading.push(new Update(appMap.uploading[i], appMap.uploadingmod[i]));
        }
        const requisitioning: Update[] = [];
        for (let i = 0; i < appMap.requisitioning.length; i++) {
            requisitioning.push(new Update(appMap.requisitioning[i], appMap.requisitioningmod[i]));
        }
        const running: Update[] = [];
        for (let i = 0; i < appMap.running.length; i++) {
            running.push(new Update(appMap.running[i], appMap.runningmod[i]));
        }
		var app: App = new App(appMap.name, JSON.parse(appMap.notebook), appMap.uuid, initializing, uploading, requisitioning, running, new Date(appMap.timestamp));
		// Add modules
		for (let module of appMap.modules) {
            const output: Update[] = [];
            for (let i = 0; i < module.output.length; i++) {
				output.push(new Update(module.output[i], module.outputmod[i]));
            }
            const files: OutputFile[] = [];
            for (let i = 0; i < module.files.length; i++) {
                if (module.files[i] != '') {
                    files.push(new OutputFile(module.files[i], module.filesmod[i], module.filessize[i]));
                }
			}
			var mod: Module = new Module(module.uuid, appMap.uuid, app.addOutput, module.machine ? Object.setPrototypeOf(module.machine, Machine.prototype) : null, module.token, output, module.updates, files);
			app.addModule(mod);
			if (mod.modStatus == Status.Running) {
                // The module is still running
                if (!app._initializing.completed || !app._uploading.completed || !app._requisitioning.completed || !app._running.completed) {
                    // Don't poll the module if the app is not running
					mod.startPolling(app.interactive);
                }
			}
		}
		if (!app._initializing.completed || !app._uploading.completed || !app._requisitioning.completed || !app._running.completed) {
			app.startPolling();
		}
		return app;
	}

	get notebook(): any {
		return this._notebook;
	}

	get name(): string {
		return this._name;
	}

	get uuid(): string {
		return this._uuid;
	}

	get modules(): Module[] {
		return this._modules;
	}

	get initializing(): ProgressMessage {
		return this._initializing;
	}

	get uploading(): ProgressMessage {
		return this._uploading;
	}

	get requisitioning(): ProgressMessage {
		return this._requisitioning;
	}

	get running(): ProgressMessage {
		return this._running;
	}

	get timestamp(): Date {
		return this._timestamp;
	}

	get failed(): boolean {
		for (let mod of this.modules) {
			if (mod.error) return true;
		}
		return this._initializing.error || this._uploading.error || this._requisitioning.error || this._running.error;
	}

	get interactive(): boolean {
		return this._interactive;
	}

	get sessionToken(): string {
        for (let mod of this.modules) {
			if (mod.sessionToken) return mod.sessionToken;
        }
        return undefined;
	}
	
	get sessionPort(): string {
        for (let mod of this.modules) {
			if (mod.sessionPort) return mod.sessionPort;
        }
        return undefined;
    }

    get machine(): Machine {
        for (let mod of this.modules) {
			if (mod.machine) return mod.machine;
        }
        return undefined;
	}

	public addModule(mod: Module) {
		mod.changed.connect(() => this._changed.emit(this), this);
		this._modules.push(mod);
	}
	
	public async previewNotebook(printRecommendations: boolean): Promise<Machine[]> {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/preview-notebook";
		const notebook = {
			content: JSON.stringify(this._notebook),
				path: this.name,
		};
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				notebook: notebook,
			}),
		};
		return ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (printRecommendations) {
				console.log("////");
				console.log("///  Start Recommendations: ");
				console.log("//");

				for (let machine of body.machines) {
					console.log(Object.setPrototypeOf(machine, Machine.prototype));
				}

				console.log("//");
				console.log("///  End Recommendations: ");
				console.log("////");
			}
            if (body.machines.length == 0) return [new NoMachine()]; // we have no recommendations
            const machines: Machine[] = [];
            for (let machine of body.machines) {
                machines.push(Object.setPrototypeOf(machine, Machine.prototype));
            }
			return machines;
		});
	}

	// We only want to add this app to the app tracker if the initialization succeeds
	public async setupNotebook(appTracker: AppTracker) {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/setup-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				name: this._name,
				timestamp: this._timestamp.toISOString(),
				notebook: {
					path: this._name,
					content: JSON.stringify(this._notebook),
				},
			}),
		};
		return ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			Global.jobLaunched.emit(void 0);
			this._uuid = body.uuid;
			this._initializing.appUUID = this._uuid;
			this._uploading.appUUID = this._uuid;
			this._requisitioning.appUUID = this._uuid;
			this._running.appUUID = this._uuid;
			this._initializing.addUpdate(new Update("Initializing...", ""));
			appTracker.addApp(this);
			this._changed.emit(this);
			this.launchNotebook();
		});
	}

	private getLaunchStatus() {
        // If there is an unsigned agreement, do not poll
        if (Global.user != null && Global.user.unsignedAgreement) {
            if (!this.failed) setTimeout(() => this.getLaunchStatus(), 500);
            return;
        }
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/get-launch-status";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				uuid: this._uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			if (response.status == 204) {
				if (!this.failed) setTimeout(() => this.getLaunchStatus(), 500);
				return;
			}
			return response.json();
		}).then((body: any) => {
			if (body) {
				if (body.status == "Finished") {
					for (let i = 0; i < body.modules.length; i++) {
						const mod = new Module(body.modules[i], this._uuid, this.addOutput);
						this.addModule(mod);
						mod.startPolling(this.interactive);
					}
				} else if (body.status == "Failed") {
					if (!this._initializing.completed) {
						this._initializing.addUpdate(new Update(body.message || 'Initialization failed', ""));
						this._initializing.addUpdate(new Update("error", ""));
						this._initializing.addUpdate(new Update("stop", ""));
					} else if (!this._uploading.completed) {
						this._uploading.addUpdate(new Update(body.message || 'File upload failed', ""));
						this._uploading.addUpdate(new Update("error", ""));
						this._uploading.addUpdate(new Update("stop", ""));
					}
					if (body.snackbar) {
						Global.snackbarChange.emit(new Snackbar(
                            body.snackbar,
                            { variant: 'error', }
                        ));
					}
				} else {
					if (!this.failed) setTimeout(() => this.getLaunchStatus(), 500);
                }
                this._changed.emit(this);
            }
		}, (error: ServerConnection.ResponseError) => {
			if (!this.failed) setTimeout(() => this.getLaunchStatus(), 500);
		});
	}

	private getCompressionProgress() {
        // If there is an unsigned agreement, do not poll
        if (Global.user != null && Global.user.unsignedAgreement) {
            if (!this.failed) setTimeout(() => this.getCompressionProgress(), 500);
            return;
        }
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/get-launch-compression-progress";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				uuid: this._uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			if (response.status == 204) {
				if (!this.failed) setTimeout(() => this.getCompressionProgress(), 500);
				return;
			}
			return response.json();
		}).then((body: any) => {
			if (body) {
				if (this._initializing.message != "Compressing files...") {
					this._initializing.addUpdate(new Update("Compressing files...", ""));
				}
				this._initializing.loaded = body.read;
				this._initializing.total = body.total;
				if (body.read != 0 && body.read == body.total) {
                    // Do nothing
                } else {
					if (!this.failed) setTimeout(() => this.getCompressionProgress(), 500);
				}
				this._changed.emit(this);
			}
		}, (error: ServerConnection.ResponseError) => {
			if (!this.failed) setTimeout(() => this.getLaunchStatus(), 500);
		});
	}

	private getUploadProgress() {
        // If there is an unsigned agreement, do not poll
        if (Global.user != null && Global.user.unsignedAgreement) {
            if (!this.failed) setTimeout(() => this.getUploadProgress(), 500);
            return;
        }
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/get-launch-upload-progress";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				uuid: this._uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			if (response.status == 204) {
				if (!this.failed) setTimeout(() => this.getUploadProgress(), 500);
				return;
			}
			return response.json();
		}).then((body: any) => {
			if (body) {
				if (!this._initializing.completed) {
					this._initializing.total = 0;
					this._initializing.addUpdate(new Update("stop", ""));
					this._uploading.addUpdate(new Update("Uploading files...", ""));
				}
				this._uploading.loaded = body.read;
				this._uploading.total = body.total;
				if (body.read != 0 && body.read == body.total) {
					this._uploading.addUpdate(new Update("stop", ""));
					this.startPolling();
				} else {
					if (!this.failed) setTimeout(() => this.getUploadProgress(), 500);
				}
				this._changed.emit(this);
			}
		}, (error: ServerConnection.ResponseError) => {
			if (!this.failed) setTimeout(() => this.getLaunchStatus(), 500);
		});
	}

	// Convert and send a python notebook to the REST interface for deployment
	private async launchNotebook() {
		const optumi: OptumiMetadata = new OptumiMetadata(this._notebook["metadata"]["optumi"] || {});
		const uploadFiles: FileUploadMetadata[] = optumi.upload.files;
		const requirements: string = optumi.upload.requirements;
		const compressFiles = Global.user.compressFilesEnabled;

		var data: any = {};

		if (requirements != null) {
			data.requirementsFile =  requirements;
		}

		data.dataFiles = [];
		for (var uploadEntry of uploadFiles) {
			if (uploadEntry.type == 'directory') {
				for (var file of (await FileServerUtils.getRecursiveTree(uploadEntry.path))) {
					data.dataFiles.push(file);
				}
			} else {
				data.dataFiles.push(uploadEntry.path);
			}
		}
		data.compress = compressFiles;

		data.uuid = this._uuid;
		data.notebook = {
			path: this._name,
			content: JSON.stringify(this._notebook),
		}
		data.timestamp = this._timestamp.toISOString();

		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/launch-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify(data),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
		}, (error: ServerConnection.ResponseError) => {
			this._initializing.addUpdate(new Update('Initialization failed', ""));
			this._initializing.addUpdate(new Update('error', ""));
			this._initializing.addUpdate(new Update('stop', ""));
		});
		this.getLaunchStatus();
		if (compressFiles && data.dataFiles.length != 0) this.getCompressionProgress();
		this.getUploadProgress();
	}

	getAppStatus(): Status {
		if (this.initializing.error) return Status.Completed;
		if (this.uploading.error) return Status.Completed;
		if (this.requisitioning.error) return Status.Completed;
		if (this.running.completed) return Status.Completed;
		if (this.uploading.completed) return Status.Running;
		return Status.Initializing;
	}

	getAppMessage(): string {
		var message = "";
		if (this._initializing.message != "") message = this._initializing.message;
		if (this._uploading.message != "") message = this._uploading.message;
		if (this._requisitioning.message != "") message = this._requisitioning.message;
		if (this._running.message != "") message = this._running.message;
		// We will say a session is starting until we can connect to it
		if (this.interactive && message == 'Running...' && !(this.modules.length > 0 && this.modules[0].sessionReady)) return 'Starting...';
		// We call a terminated app 'closed'
		if (this.interactive && message == 'Terminated') return 'Closed';
		return message;
    }
    
    getTimeElapsed(): string {
        if (!this._initializing.completed) return undefined;
		if (!this._uploading.completed) return undefined;
		if (!this._requisitioning.completed) return undefined;
        return this._running.elapsed;
	}
	
	getEndTime(): Date {
		if (!this._initializing.completed) return undefined;
		if (!this._uploading.completed) return undefined;
		if (!this._requisitioning.completed) return undefined;
        return this._running.endTime;
	}


    getCost(): string {
		if (this.getTimeElapsed() == undefined) return undefined;
		if (this.machine == undefined) return undefined;
		var rate = this.machine.rate;
		const split = this.getTimeElapsed().split(':');
		if (split.length == 3) {
			const hours = +split[0]
			const minutes = +split[1];
			const seconds = +split[2];
			const cost = ((hours * rate) + (minutes * rate / 60) + (seconds * rate / 3600));
        	return (cost.toFixed(2) == '0.00' ? '< $0.01' : '~ $' + cost.toFixed(2));
		} else {
			const minutes = +split[0];
			const seconds = +split[1];
			const cost = ((minutes * rate / 60) + (seconds * rate / 3600));
			return (cost.toFixed(2) == '0.00' ? '< $0.01' : '~ $' + cost.toFixed(2));
		} 
    }

	getShowLoading(): boolean {
		if (!this._initializing.completed) return this._initializing.loaded != this._initializing.total;
		if (!this._uploading.completed) return this._uploading.loaded != this._uploading.total;
		if (!this._requisitioning.completed) return this._requisitioning.loaded != this._requisitioning.total;
		if (!this._running.completed) return this._running.loaded != this._running.total;
		return false;
	}

	getPercentLoaded(): number {
		if (!this._initializing.completed) return undefined;
		if (!this._uploading.completed) return this._uploading.total == -1 ? undefined : this._uploading.loaded / this._uploading.total;
		if (!this._requisitioning.completed) return this._requisitioning.total == -1 ? undefined : this._requisitioning.loaded / this._requisitioning.total;
		if (!this._running.completed) return this._running.total == -1 ? undefined : this._running.loaded / this._running.total;
		return undefined;
	}

	getLoadingTooltip(): string {
		if (!this.getShowLoading()) return undefined;
		if (!this._initializing.completed) return this._initializing.loaded + '/' + this._initializing.total + ' files';
		if (!this._uploading.completed) return this._uploading.total == -1 ? '' : FormatUtils.styleCapacityUnitValue()(this._uploading.loaded) + '/' + FormatUtils.styleCapacityUnitValue()(this._uploading.total);
		if (!this._requisitioning.completed) return this._requisitioning.total == -1 ? '' : FormatUtils.styleCapacityUnitValue()(this._requisitioning.loaded / Math.pow(1024, 2)) + '/' + FormatUtils.styleCapacityUnitValue()(this._requisitioning.total / Math.pow(1024, 2));
		if (!this._running.completed) return this._running.total == -1 ? '' : FormatUtils.styleCapacityUnitValue()(this._running.loaded / Math.pow(1024, 2)) + '/' + FormatUtils.styleCapacityUnitValue()(this._running.total / Math.pow(1024, 2));
	}

	getError() {
		if (this.failed) {
			return true;
		}
		for (var mod of this._modules) {
			if (mod.error) {
				return true;
			}
		}
		return false;
	}

	private receiveUpdate() {
		// If there is an unsigned agreement, do not poll
        if (Global.user != null && Global.user.unsignedAgreement) {
            setTimeout(() => this.receiveUpdate(), 500);
            return;
        }
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/pull-workload-status-update";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				uuid: this._uuid,
				lastInitializingLine: this._initializing.length.toString(),
				lastUploadingLine: this._uploading.length.toString(),
				lastRequisitioningLine: this._requisitioning.length.toString(),
				lastRunningLine: this._running.length.toString(),
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			if (this._polling) {
				// If we are polling, send a new request in 2 seconds
				setTimeout(() => this.receiveUpdate(), 2000);
			}
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (body.initializing != null) {
				for (let i = 0; i < body.initializing.length; i++) {
					this._initializing.addUpdate(new Update(body.initializing[i], body.initializingmod[i]), false);
				}
			}
			if (body.uploading != null) {
				for (let i = 0; i < body.uploading.length; i++) {
					this._uploading.addUpdate(new Update(body.uploading[i], body.uploadingmod[i]), false);
				}
			}
			if (body.requisitioning != null) {
				for (let i = 0; i < body.requisitioning.length; i++) {
					this._requisitioning.addUpdate(new Update(body.requisitioning[i], body.requisitioningmod[i]), false);
                    // Special case a warning when we fail to get a machine and start trying a new one
                    if (body.requisitioning[i] == 'Machine unavailable, trying another') {
                        Global.snackbarChange.emit(new Snackbar(
                            body.requisitioning[i],
                            { variant: 'warning', }
                        ));
                    }
                    // Special case loading bar while waiting for a server
					if (this._requisitioning.message == "Waiting for cloud provider...") {
						this._requisitioning.total = -1;
					} else {
						this._requisitioning.total = 0;
					}
				}
			}
			if (body.running != null) {
				for (let i = 0; i < body.running.length; i++) {
                    if (body.running[i] == 'Completed') {
                        Global.snackbarChange.emit(new Snackbar(
                            body.running[i],
                            { variant: 'success', }
                        ));
                    } else if (body.running[i] == 'Failed') {
                        Global.snackbarChange.emit(new Snackbar(
                            body.running[i],
                            { variant: 'error', }
                        ));
                    }
					this._running.addUpdate(new Update(body.running[i], body.runningmod[i]), false);
				}
			}
			if (this.getAppStatus() == Status.Completed) {
				this.stopPolling();
			}
			this._changed.emit(this);
		});
	}

	public startPolling() {
		this._polling = true;
		this.receiveUpdate();
	}

	public stopPolling() {
        this._polling = false;
        for (let module of this._modules) {
            module.stopPolling(this.interactive);
        }
	}

	public getComponent(): React.CElement<IProps, AppComponent> {
		return React.createElement(AppComponent, {key: this._uuid, app: this});
	}

	private formatTime = (): string => {
		var app: App = this
		var yesterday: Date = new Date()
		yesterday.setDate(yesterday.getDate() - 1)
		if (app.timestamp == undefined) return undefined;
		var startTime = app.timestamp < yesterday ? app.timestamp.toLocaleDateString() : app.timestamp.toLocaleTimeString();
		if (app.getEndTime() == undefined) return startTime;
		var endTime = app.getEndTime() < yesterday ? app.getEndTime().toLocaleDateString() : app.getEndTime().toLocaleTimeString();
		return startTime == endTime ? startTime : startTime + " - " + endTime;
	};

	public getIdentityComponent() {
		var app: App = this
		return (
			<ExtraInfo reminder={app.name}>
				<div style={{paddingLeft: '3px'}}> {/* the padding is 7px because the height it needs to take up is 36 and the height of this 16px font is 22px */}
					<div style={{paddingBottom: '3px', fontSize: '13px', lineHeight: '1', fontWeight: 'normal', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>
						{app.name.split('/').pop()}
					</div>
					<span style={{fontSize: '13px', lineHeight: '1', fontWeight: 'normal', color: 'gray'}}>
						{this.formatTime()}
					</span>
				</div>
			</ExtraInfo>
		)
	}
}

interface IProps {
	app: App,
}

interface IState {
	waiting: boolean;
	spinning: boolean;
	showDeleteJobPopup: boolean;
	showStopJobPopup: boolean;
}

class AppComponent extends React.Component<IProps, IState> {
	_isMounted = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
			waiting: false,
			spinning: false,
			showDeleteJobPopup: false,
			showStopJobPopup: false,
        };
    }

	private getDeleteJobPreventValue = (): boolean => {
		return Global.user.deleteJobPreventEnabled;
	}

	private saveDeleteJobPreventValue = (prevent: boolean) => {
		Global.user.deleteJobPreventEnabled = prevent;
	}

	private handleDeleteClicked = () => {
		this.checkAndSetState({ waiting: true, spinning: false });
		setTimeout(() => this.checkAndSetState({ spinning: true }), 1000);
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/teardown-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				uuid: this.props.app.uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init,
			settings
		).then((response: Response) => {
			this.checkAndSetState({ waiting: false });
			Global.handleResponse(response);
			Global.user.appTracker.removeApp(this.props.app.uuid);
		});
    }
	
	private getStopJobPreventValue = (): boolean => {
		return Global.user.stopJobPreventEnabled;
	}

	private saveStopJobPreventValue = (prevent: boolean) => {
		Global.user.stopJobPreventEnabled = prevent;
	}

    private handleStopClicked = () => {
		this.checkAndSetState({ waiting: true, spinning: false });
		setTimeout(() => this.checkAndSetState({ spinning: true }), 1000);
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/stop-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				uuid: this.props.app.uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init,
			settings
		).then((response: Response) => {
			this.checkAndSetState({ waiting: false })
			Global.handleResponse(response);
		});
	}

	private getStatusColor = (): StatusColor => {
		if (this.props.app.getAppMessage() == 'Closed' || this.props.app.getAppMessage() == 'Terminated') {
			return StatusColor.DARK_GRAY;
		}
		if (this.props.app.getError()) {
			return StatusColor.RED;
		} else {
			const appStatus = this.props.app.getAppStatus();
			if (appStatus == Status.Initializing) {
				return StatusColor.BLUE;
			} else {
				return StatusColor.GREEN;
			}
		}
	}

	public render = (): JSX.Element => {
		var tags: JSX.Element[] = []
		var app: App = this.props.app

		// Get the right progress message...
		var appMessage = app.getAppMessage();
		const loadingTooltip = this.props.app.getLoadingTooltip()
		tags.push(
			<ExtraInfo reminder={(loadingTooltip === '' || loadingTooltip === undefined) ? 'Status' : loadingTooltip}>
				<Tag id={app.uuid + appMessage} key={'appMessage' + appMessage}
					icon={app.getAppStatus() == Status.Completed ? (app.getError() ? (
						(app.getAppMessage() == 'Closed' || app.getAppMessage() == 'Terminated' ? (
							<ClearIcon style={{
								height: '14px',
								width: '14px',
								fill: 'gray',
							}} />
						) : (
							<ClearIcon style={{
								height: '14px',
								width: '14px',
								fill: '#f48f8d',
							}} />
						))
					) : (
						<CheckIcon style={{
							height: '14px',
							width: '14px',
							fill: '#68da7c',
						}} />
					)) : undefined}
					label={appMessage}
					color={(this.props.app.getShowLoading() || app.getAppStatus() == Status.Completed) ? this.getStatusColor() : undefined}
					showLoading={this.props.app.getShowLoading()}
					percentLoaded={this.props.app.getPercentLoaded()}
				/>
			</ExtraInfo>
		)
        var appElapsed = app.getTimeElapsed();
		tags.push(
			<ExtraInfo reminder='Duration'>
				<Tag key={'appElapsed' + appElapsed} label={appElapsed} />
			</ExtraInfo>
		)
		var appCost = app.getCost();
		if (appCost) {
			tags.push(
				<ExtraInfo reminder='Cost'>
					<Tag key={'appCost' + appCost} label={appCost} />
				</ExtraInfo>
			)
		}
        return (
			<>
                <StatusWrapper key={this.props.app.uuid} statusColor={app.getAppStatus() == Status.Completed ? 'var(--jp-layout-color2)' : this.getStatusColor()}>
                    <InfoSkirt
                        leftButton={
							<ExtraInfo reminder='See details'>
								<DetailsDialog app={this.props.app} />
							</ExtraInfo>
						}
                        rightButton={(this.props.app.requisitioning.completed && !this.props.app.requisitioning.error) && !this.props.app.running.completed ? (
							<>
								<WarningPopup
									open={this.state.showStopJobPopup}
									headerText="Are you sure?"
									bodyText={(() => {
										if (this.props.app.interactive) {
											return "This session is active. If you close it, the session cannot be resumed."
										} else {
											return "This job is running. If you terminate it, the job cannot be resumed."
										}
									})()}
									preventText="Don't ask me again"
									cancel={{
										text: `Cancel`,
										onCancel: (prevent: boolean) => {
											// this.saveStopJobPreventValue(prevent)
											this.checkAndSetState({ showStopJobPopup: false })
										},
									}}
									continue={{
										text: (() => {
											if (this.props.app.interactive) {
												return "Close it"
											} else {
												return "Terminate it"
											}
										})(),
										onContinue: (prevent: boolean) => {
											this.checkAndSetState({ showStopJobPopup: false })
											this.saveStopJobPreventValue(prevent)
											this.handleStopClicked()
										},
										color: `error`,
									}}
								/>
								<IconButton
									disabled={this.state.waiting}
									onClick={() => {
										if (this.getStopJobPreventValue()) {
											this.handleStopClicked()
										} else {
											this.checkAndSetState({ showStopJobPopup: true })
										}
									}}
									style={{
										position: 'relative',
										display: 'inline-block',
										width: '36px',
										height: '36px',
										padding: '3px',
									}}
								>
									<ExtraInfo reminder={this.props.app.interactive ? 'Stop' : 'Terminate'}>
										<StopIcon style={{
											position: 'relative',
											width: '30px',
											height: '30px',
											padding: '3px',
										}} />
									</ExtraInfo>
									{this.state.waiting && this.state.spinning && <CircularProgress size='30px' style={{position: 'absolute'}}/>}
								</IconButton>
							</>
						) : (
							<>
								<WarningPopup
									open={this.state.showDeleteJobPopup}
									headerText="Are you sure?"
									bodyText={(() => {
										if (this.props.app.interactive) {
											return "You will lose all session information and any files that have not been downloaded. This cannot be undone."
										} else {
											return "You will lose all job information and any files that have not been downloaded. This cannot be undone."
										}
									})()}
									preventText="Don't ask me again"
									cancel={{
										text: `Cancel`,
										onCancel: (prevent: boolean) => {
											// this.saveDeleteJobPreventValue(prevent)
											this.checkAndSetState({ showDeleteJobPopup: false })
										},
									}}
									continue={{
										text: `Delete it`,
										onContinue: (prevent: boolean) => {
											this.checkAndSetState({ showDeleteJobPopup: false })
											this.saveDeleteJobPreventValue(prevent)
											this.handleDeleteClicked()
										},
										color: `error`,
									}}
								/>
								<ExtraInfo reminder='Delete'>
									<IconButton
										disabled={this.state.waiting || !this.props.app.initializing.completed}
										onClick={() => {
											if (this.getDeleteJobPreventValue() || !this.props.app.running.started) {
												this.handleDeleteClicked()
											} else {
												this.checkAndSetState({ showDeleteJobPopup: true })
											}
										}}
										style={{position: 'relative', display: 'inline-block', width: '36px', height: '36px', padding: '3px'}}
									>
										<DeleteIcon style={{position: 'relative', width: '30px', height: '30px', padding: '3px'}} />
										{this.state.waiting && this.state.spinning && <CircularProgress size='30px' style={{position: 'absolute'}}/>}
									</IconButton>
								</ExtraInfo>
							</>
						)}
                        tags={tags}
                    >
                        {this.props.app.getIdentityComponent()}
                    </InfoSkirt>
                </StatusWrapper>
            </>
		)
	}

	public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender')
            return false;
        } catch (error) {
            return true;
        }
    }

	private checkAndSetState = (map: any) => {
		if (this._isMounted) {
			this.setState(map);
		}
	}

	// Will be called automatically when the component is mounted
	componentDidMount = () => {
        this._isMounted = true;
	}

	// Will be called automatically when the component is unmounted
	componentWillUnmount = () => {
		this._isMounted = false;
	}
}
