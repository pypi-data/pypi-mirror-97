/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { ISignal, Signal } from '@lumino/signaling';

import { ServerConnection } from '@jupyterlab/services';
import { Global } from '../Global';
import { Update } from './Update';
import { OutputFile } from './OutputFile';
import { Machine } from './machine/Machine';

export enum Status {
	Initializing,
	Running,
	Completed,
}

export class Module {
	private _changed = new Signal<this, Module>(this);

	get changed(): ISignal<this, Module> {
		return this._changed;
	}

	private _sessionReady: boolean = false;

	get sessionReady(): boolean {
		return this._sessionReady;
	}

	private addOutput: (line: string, modifier: string) => void;

	private readonly _uuid: string;
	private readonly _workloadUUID: string;

	private _sessionToken: string;
	private _sessionPort: string;

    private _machine: Machine;
    
    private _output: Update[];
    private _files: OutputFile[];
    private _updates: string[];

	// Polling timer
	private _polling: boolean;

	constructor(uuid: string, workloadUUID: string, addOutput: (line: string, modifier: string) => void, machine: Machine = null, sessionToken: string = null, output: Update[] = [], updates: string[] = [], files: OutputFile[] = []) {
		this._uuid = uuid;
		this._workloadUUID = workloadUUID;
		this.addOutput = addOutput;

		this._sessionToken = sessionToken;

        this._machine = machine;

		this._output = output;
		for (var l of this._output) {
			this.addOutput(l.line, l.modifier);
		}
		this._sessionReady = output.map(x => x.line.includes('Jupyter Server ') && x.line.includes(' is running at:')).includes(true);

		this._files = files;
		this._updates = updates;

		this._polling = false;
	}

	get uuid(): string {
		return this._uuid;
	}

	////
	/// We are not using the module stdin yet
	//

	get sessionToken(): string {
        return this._sessionToken;
	}
	
	get sessionPort(): string {
        return this._sessionPort;
    }

    get machine(): Machine {
        return this._machine;
    }

    get output(): Update[] {
        return this._output;
    }

	get files(): OutputFile[] {
		return this._files;
	}

	get modStatus(): Status {
		return (this._updates.includes("closed") || this._updates.includes("stop")) ? Status.Completed : Status.Running;
	}

	get error(): boolean {
		return this._updates.includes("error");
    }

	private async receiveUpdate() {
        // If there is an unsigned agreement, do not poll
        if (Global.user != null && Global.user.unsignedAgreement) {
            if (this._polling) setTimeout(() => this.receiveUpdate(), 500);
            return;
        }
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/pull-module-status-update";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				workloadUUID: this._workloadUUID,
				moduleUUID: this._uuid,
				lastUpdateLine: this._updates.length.toString(),
				lastOutputLine: this._output.length.toString(),
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			if (this._polling) {
				// If we are polling, send a new request in half a second
				setTimeout(() => this.receiveUpdate(), 500);
			}
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (body.output != null) {
				for (let i = 0; i < body.output.length; i++) {
					this.addOutput(body.output[i], body.outputmod[i]);
					this._output.push(new Update(body.output[i], body.outputmod[i]));
					if (body.output[i].includes('Jupyter Server ') && body.output[i].includes(' is running at:')) {
						this._sessionReady = true;
						window.open('http://localhost:' + this._sessionPort + '?token=' + this._sessionToken, '_blank');
					}
				}
            }
            if (body.files != null) {
                this._files = [];
				for (let i = 0; i < body.files.length; i++) {
                    if (body.files[i] != '') {
                        this._files.push(new OutputFile(body.files[i], body.filesmod[i], body.filessize[i]));
                    }
				}
			}
			if (body.token != null) {
				this._sessionToken = body.token;
			}
			if (body.updates != null) {
				for (var update of body.updates) {
					this._updates.push(update);
					if (update == "stop") {
                        this._updates.push("stop");
					} else if (update == "launched") {
					} else if (update == "closed") {
					}
				}
            }
            if (body.machine != null) {
                this._machine = Object.setPrototypeOf(body.machine, Machine.prototype);
            }
			this._changed.emit(this);
		});
    }

    public pushModuleInput = (line: string) => {
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/push-module-input";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				workloadUUID: this._workloadUUID,
				moduleUUID: this._uuid,
                line: line,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
		});
    }

	public startPolling(interactive = false) {
		this._polling = true;
		this.receiveUpdate();

		// Start a session handler if necessary
		if (interactive) {
			const settings = ServerConnection.makeSettings();
			const url = settings.baseUrl + "optumi/connect-session";
			const init: RequestInit = {
				method: 'POST',
				body: JSON.stringify({
					module: this._uuid,
				}),
			};
			ServerConnection.makeRequest(
				url,
				init, 
				settings
			).then((response: Response) => {
				Global.handleResponse(response);
				return response.json();
			}).then((body: any) => {
				if (body.port) {
					this._sessionPort = body.port;
				}
			});
		}
	}

	public stopPolling(interactive = false) {
		this._polling = false;

		// Stop a session handler if necessary
		if (interactive) {
			const settings = ServerConnection.makeSettings();
			const url = settings.baseUrl + "optumi/disconnect-session";
			const init: RequestInit = {
				method: 'POST',
				body: JSON.stringify({
					module: this._uuid,
				}),
			};
			ServerConnection.makeRequest(
				url,
				init, 
				settings
			).then((response: Response) => {
				Global.handleResponse(response);
				return response.text();
			});
		}
	}
}
