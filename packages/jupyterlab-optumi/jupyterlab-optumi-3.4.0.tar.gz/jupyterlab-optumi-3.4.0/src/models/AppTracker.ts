/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { App } from './App';
import { Status } from './Module';

import { ISignal, Signal } from '@lumino/signaling';

export class AppTracker {
	private _apps: App[] = [];
	private _appsChanged = new Signal<this, App[]>(this);

	get appsChanged(): ISignal<this, App[]> {
		return this._appsChanged;
	}

	get activeSessions(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() != Status.Completed && app.interactive);
	}

	get finishedSessions(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() == Status.Completed && app.interactive);
	}

	get activeJobs(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() != Status.Completed && !app.interactive);
	}

	get finishedJobs(): App[] {
		return this._apps.filter((app: App) => app.getAppStatus() == Status.Completed && !app.interactive);
	}

	public addApp(app: App) {
		this._apps.unshift(app);
		this._appsChanged.emit(this._apps);
		app.changed.connect(() => this._appsChanged.emit(this._apps), this);
	}

	public removeApp(uuid: string) {
		var app: App = this._apps.filter((app: App) => app.uuid == uuid)[0];
		for (let module of app.modules) {
			module.stopPolling(app.interactive);
		}
		app.stopPolling();
		this._apps = this._apps.filter((app: App) => app.uuid != uuid);
		app.changed.disconnect(() => this._appsChanged.emit(this._apps), this);
		this._appsChanged.emit(this._apps);
	}

	public getDisplayNum() {
		return this._apps.filter((app: App) => app.getAppStatus() != Status.Completed).length;
	}
}
