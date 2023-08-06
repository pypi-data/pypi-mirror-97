/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { User } from "./models/User";
import { Signal } from '@lumino/signaling';
import { ILabShell, JupyterFrontEnd } from "@jupyterlab/application";
import { IThemeManager } from "@jupyterlab/apputils";
import { IDocumentManager } from '@jupyterlab/docmanager';
import { Machine } from "./models/machine/Machine";
import { OptumiMetadataTracker } from "./models/OptumiMetadataTracker";
import { NotebookTracker } from "@jupyterlab/notebook";
import { Snackbar } from "./models/Snackbar";
import { ServerConnection } from '@jupyterlab/services';
import LogScaleUtils from "./utils/LogScaleUtils";
import { DataConnectorMetadata } from "./components/deploy/dataConnectorBrowser/DataConnectorBrowser";

export class Global {
    private static emitter: Global = new Global()

    private static _version: string = undefined;
    public static get version(): string { return Global._version }
    public static set version(version: string) {
        Global._version = version
        Global._onVersionSet.emit(void 0);
    }

    private static _onVersionSet: Signal<Global, string> = new Signal<Global, string>(Global.emitter)
    public static get onVersionSet(): Signal<Global, string> { return Global._onVersionSet }

    private static canvas: HTMLCanvasElement = document.createElement("canvas");
    public static getStringWidth(text: string, font: string): number {
        // re-use canvas object for better performance
        var context: CanvasRenderingContext2D = this.canvas.getContext("2d");
        context.font = font;
        var metrics: TextMetrics = context.measureText(text + ' ');
        return metrics.width + 1;
    }

    private static _domain: string = ""
    public static get domain(): string { return Global._domain }
    public static set domain(domain: string) {
        Global._domain = domain
        Global._onDomainChange.emit(domain);
    }

    private static _onDomainChange: Signal<Global, string> = new Signal<Global, string>(Global.emitter)
    public static get onDomainChange(): Signal<Global, string> { return Global._onDomainChange }

    private static _shouldLogOnRender: boolean = false
    public static get shouldLogOnRender(): boolean { return Global._shouldLogOnRender }

    private static _inQuestionMode: boolean = false
    public static get inQuestionMode(): boolean { return Global._inQuestionMode }
    public static set inQuestionMode(inQuestionMode: boolean) {
        Global._inQuestionMode = inQuestionMode
        Global._onInQuestionModeChange.emit(inQuestionMode)
    }

    private static _jobLaunched: Signal<Global, void> = new Signal<Global, void>(Global.emitter)
    public static get jobLaunched(): Signal<Global, void> { return Global._jobLaunched }

    private static _onInQuestionModeChange: Signal<Global, boolean> = new Signal<Global, boolean>(Global.emitter)
    public static get onInQuestionModeChange(): Signal<Global, boolean> { return Global._onInQuestionModeChange }

    private static _lab: JupyterFrontEnd = undefined
    public static get lab(): JupyterFrontEnd { return Global._lab }
    public static set lab(lab: JupyterFrontEnd) { Global._lab = lab }

    private static _labShell: ILabShell = undefined
    public static get labShell(): ILabShell { return Global._labShell }
    public static set labShell(labShell: ILabShell) { Global._labShell = labShell }

    private static _themeManager: IThemeManager = undefined
    public static get themeManager(): IThemeManager { return Global._themeManager }
    public static set themeManager(themeManager: IThemeManager) { Global._themeManager = themeManager }

    private static _tracker: NotebookTracker = undefined
    public static get tracker(): NotebookTracker { return Global._tracker }
    public static set tracker(tracker: NotebookTracker) { Global._tracker = tracker }

    private static _metadata: OptumiMetadataTracker = undefined
    public static get metadata(): OptumiMetadataTracker { return Global._metadata }
    public static set metadata(metadata: OptumiMetadataTracker) { Global._metadata = metadata }

    private static _docManager: IDocumentManager = undefined
    public static get docManager(): IDocumentManager { return Global._docManager }
    public static set docManager(docManager: IDocumentManager) { Global._docManager = docManager }

    private static _user: User = null // If we are logged in we will have a user, otherwise it will be null
    public static get user(): User { return Global._user }
    public static set user(user: User) {
        if (this._user != null) {
            // Stop polling for apps if user is logging out/ being logged out
            for (let app of this._user.appTracker.activeJobs) {
                app.stopPolling();
            }
            for (let app of this._user.appTracker.activeSessions) {
                app.stopPolling();
            }
        }
        if (user == null) Global._onNullUser.emit(null);
        Global._user = user;
        // Reset 401 counter
        Global.consecutive401s = 0;
        // Reset cached info
        Global.lastMachines = []
        Global.lastMachineRate = 0;
        Global.lastCreditsCost = 0;
        Global.lastCreditsBalance = 0;
        Global.lastBudgetCost = 0;
        Global.lastDataConnectors = [];
        // Signal
        Global._onUserChange.emit(user)
    }

    private static _onUserChange: Signal<Global, User> = new Signal<Global, User>(Global.emitter)
    public static get onUserChange(): Signal<Global, User> { return Global._onUserChange }

    private static _onNullUser: Signal<Global, User> = new Signal<Global, User>(Global.emitter)
    public static get onNullUser(): Signal<Global, User> { return Global._onNullUser }

    public static agreementURL: string;

    public static snackbarChange: Signal<Global, Snackbar> = new Signal<Global, Snackbar>(Global.emitter);

    // We will keep some state here to avoid having no information to show before a request returns
    public static lastMachines: Machine[] = [];
    public static lastMachineRate: number = 0;
    public static lastCreditsCost: number = 0;
    public static lastCreditsBalance: number = 0;
    public static lastBudgetCost: number = 0;
    public static lastDataConnectors: DataConnectorMetadata[] = [];

    // We will use these for the steps for fractions
    private static generateFractionSteps = () => {
        const steps = new LogScaleUtils(0, 1, 0.01, 1, true).getMarks();
        steps.unshift(
            {
                value: -1,
            }
        );
        return steps;
    }
    public static fractionMarks: any[] = Global.generateFractionSteps();

    private static consecutive401s = 0;

    // This function will update the consecutive 401s properly and throw exceptions if the request failed
    public static handleResponse = (response: Response) => {
        if (response.status == 401) {
            Global.consecutive401s++;
            if (Global.consecutive401s > 5) {
                Global.user = null;
            }
            throw new ServerConnection.ResponseError(response);
        } else {
            Global.consecutive401s = 0;
            if (response.status >= 300) {
                throw new ServerConnection.ResponseError(response);
            }
        } 
    }

    // Poll for machines in the background
    public static updateMachines = () => {
        setTimeout(Global.updateMachines, 30000);
        if (Global.user != null) {
            const settings = ServerConnection.makeSettings();
            const url = settings.baseUrl + "optumi/get-machines";
            const init = {
                method: 'GET',
            };
            ServerConnection.makeRequest(
                url,
                init, 
                settings
            ).then((response: Response) => {
                Global.handleResponse(response);
                return response.json();
            }).then((body: any) => {
                var machines: Machine[] = []
                for (var i = 0; i < body.machines.length; i++) {
                    machines.push(Object.setPrototypeOf(body.machines[i], Machine.prototype));
                }
                Global.lastMachines = machines;
            });
        }
    }
}
