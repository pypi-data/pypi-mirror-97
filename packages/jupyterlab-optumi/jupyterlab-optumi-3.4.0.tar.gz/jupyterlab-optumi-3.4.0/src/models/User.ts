/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { App } from './App';
import { AppTracker } from './AppTracker';

import { ServerConnection } from '@jupyterlab/services';

import { ISignal, Signal } from '@lumino/signaling';
import { Machines } from './Machines';
import { Machine } from './machine/Machine';
import { Page } from '../components/deploy/RequirementsBar';
import { Global } from '../Global';

export class User {
	
	// Helper function to avoid duplicate code when logging in
	public static handleLogin(responseData: any): User {
        var machines: Machine[] = []
        for (var i = 0; i < responseData.machines.length; i++) {
            machines.push(Object.setPrototypeOf(responseData.machines[i], Machine.prototype));
        }
        const newUser = new User(
            responseData.newAgreement,
            responseData.name,
            responseData.intent,
            responseData.userBudget,
            responseData.maxBudget,
            responseData.budgetCap,
            responseData.userRate,
            responseData.maxRate,
            responseData.rateCap,
            responseData.userAggregateRate,
            responseData.maxAggregateRate,
            responseData.aggregateRateCap,
            responseData.userHoldoverTime,
            responseData.maxHoldoverTime,
            responseData.holdoverTimeCap,
            responseData.userRecommendations,
            responseData.maxRecommendations,
            responseData.recommendationsCap,
            responseData.maxJobs,
            responseData.jobsCap,
            responseData.maxMachines,
            responseData.machinesCap,
            responseData.userExpertise,
            responseData.proactiveUploadsEnabled,
			responseData.compressFilesEnabled,
			responseData.lastPage,
			responseData.stopJobPreventEnabled,
			responseData.deleteJobPreventEnabled,
			responseData.noRequirementsPreventEnabled,
			responseData.noFileUploadsPreventEnabled,
			responseData.startSessionPreventEnabled,
            new AppTracker(),
            new Machines(machines, responseData.maxRate)
        );
        if (!newUser.unsignedAgreement) newUser.synchronize(responseData);
        return newUser;
	}
	
	private _deploySubMenuChanged = new Signal<this, User>(this);

	get deploySubMenuChanged(): ISignal<this, User> {
		return this._deploySubMenuChanged;
	}

	private _selectedSettingsSubMenuChanged = new Signal<this, User>(this);

	get selectedSettingsSubMenuChanged(): ISignal<this, User> {
		return this._selectedSettingsSubMenuChanged;
	}

    private _unsignedAgreement: boolean;

	private _name: string;
	private _intent: number;
	private _userBudget: number;
	private _maxBudget: number;
	private _budgetCap: number;
    private _userRate: number;
	private _maxRate: number;
    private _rateCap: number;
    private _userAggregateRate: number;
	private _maxAggregateRate: number;
    private _aggregateRateCap: number;
    private _userHoldoverTime: number;
	private _maxHoldoverTime: number;
    private _holdoverTimeCap: number;
    private _userRecommendations: number;
	private _maxRecommendations: number;
    private _recommendationsCap: number;
    private _maxJobs: number;
    private _jobsCap: number;
    private _maxMachines: number;
    private _machinesCap: number;
	private _userExpertise: number;
	private _proactiveUploadsEnabled: boolean;
	private _compressFilesEnabled: boolean;
	private _lastPage: number;
	private _stopJobPreventEnabled: boolean;
	private _deleteJobPreventEnabled: boolean;
	private _noRequirementsPreventEnabled: boolean;
	private _noFileUploadsPreventEnabled: boolean;
	private _startSessionPreventEnabled: boolean;

	private _appTracker: AppTracker;
	private _machines: Machines;

	private _deploySubMenu: Page = Page.RESOURCES;

    constructor(unsignedAgreement: boolean, name: string, intent: number, 
        userBudget: number, maxBudget: number, budgetCap: number, 
        userRate: number, maxRate: number, rateCap: number, 
        userAggregateRate: number, maxAggregateRate: number, aggregateRateCap: number, 
        userHoldoverTime: number, maxHoldoverTime: number, holdoverTimeCap: number, 
        userRecommendations: number, maxRecommendations: number, recommendationsCap: number, 
        maxJobs: number, jobsCap: number, 
        maxMachines: number, machinesCap: number, 
		userExpertise: number, proactiveUploadsEnabled: boolean, compressFilesEnabled: boolean, lastPage: number, 
		stopJobPreventEnabled: boolean, deleteJobPreventEnabled: boolean, noRequirementsPreventEnabled: boolean, noFileUploadsPreventEnabled: boolean, 
		startSessionPreventEnabled: boolean,
		appTracker: AppTracker, machines: Machines) {
        this._unsignedAgreement = unsignedAgreement === undefined ? true : unsignedAgreement;
        this._name = name;
		this._intent = intent;
        this._userBudget = userBudget;
        this._maxBudget = maxBudget;
        this._budgetCap = budgetCap;
        this._userRate = userRate;
        this._maxRate = maxRate;
        this._rateCap = rateCap;
        this._userAggregateRate = userAggregateRate;
        this._maxAggregateRate = maxAggregateRate;
        this._aggregateRateCap = aggregateRateCap;
        this._userHoldoverTime = userHoldoverTime;
        this._maxHoldoverTime = maxHoldoverTime;
        this._holdoverTimeCap = holdoverTimeCap;
        this._userRecommendations = userRecommendations;
        this._maxRecommendations = maxRecommendations;
        this._recommendationsCap = recommendationsCap;
        this._maxJobs = maxJobs;
        this._jobsCap = jobsCap;
        this._maxMachines = maxMachines;
        this._machinesCap = machinesCap;

		this._userExpertise = userExpertise;
		this._proactiveUploadsEnabled = proactiveUploadsEnabled;
		this._compressFilesEnabled = compressFilesEnabled;
		this._lastPage = lastPage;
		this._stopJobPreventEnabled = stopJobPreventEnabled;
		this._deleteJobPreventEnabled = deleteJobPreventEnabled;
		this._noRequirementsPreventEnabled = noRequirementsPreventEnabled;
		this._noFileUploadsPreventEnabled = noFileUploadsPreventEnabled;
		this._startSessionPreventEnabled = startSessionPreventEnabled;

		this._appTracker = appTracker;
        this._machines = machines;
    }
    
    get unsignedAgreement(): boolean {
		return this._unsignedAgreement;
    }
    
    set unsignedAgreement(unsignedAgreement: boolean) {
		if (unsignedAgreement === this._unsignedAgreement) {
			return;
		}
		this._unsignedAgreement = unsignedAgreement;
	}

	get name(): string {
		return this._name;
	}

	set name(name: string) {
		if (name === this._name) {
			return;
		}
		this._name = name;
	}

	get deploySubMenu(): Page {
		return this._deploySubMenu;
	}

	set deploySubMenu(deploySubMenu: Page) {
		if (deploySubMenu === this._deploySubMenu) {
			return;
		}
		this._deploySubMenu = deploySubMenu;
		this._deploySubMenuChanged.emit(this);
	}

	get intent(): number {
		return this._intent;
	}

	set intent(intent: number) {
		if (intent === this._intent) {
			return;
		}
		this._intent = intent;
		this.setUserInformation("intent", intent.toString());
	}

	get userBudget(): number {
		return this._userBudget;
	}

	set userBudget(userBudget: number) {
		if (userBudget === this._userBudget) {
			return;
		}
		this._userBudget = userBudget;
		this.setUserInformation("userBudget", userBudget.toString());
    }
    
    get maxBudget(): number {
		return this._maxBudget;
	}

	set maxBudget(maxBudget: number) {
		if (maxBudget === this._maxBudget) {
			return;
		}
		this._maxBudget = maxBudget;
		this.setUserInformation("maxBudget", maxBudget.toString());
    }
    
    get budgetCap(): number {
		return this._budgetCap;
	}
    
    get userRate(): number {
		return this._userRate;
	}

	set userRate(userRate: number) {
		if (userRate === this._userRate) {
			return;
		}
		this._userRate = userRate;
		this.setUserInformation("userRate", userRate.toString());
    }
    
    get maxRate(): number {
		return this._maxRate;
	}

	set maxRate(maxRate: number) {
		if (maxRate === this._maxRate) {
			return;
		}
		this._maxRate = maxRate;
		this.setUserInformation("maxRate", maxRate.toString());
    }
    
    get rateCap(): number {
		return this._rateCap;
	}
    
    get userAggregateRate(): number {
		return this._userAggregateRate;
	}

	set userAggregateRate(userAggregateRate: number) {
		if (userAggregateRate === this._userAggregateRate) {
			return;
		}
		this._userAggregateRate = userAggregateRate;
		this.setUserInformation("userAggregateRate", userAggregateRate.toString());
    }
    
    get maxAggregateRate(): number {
		return this._maxAggregateRate;
	}

	set maxAggregateRate(maxAggregateRate: number) {
		if (maxAggregateRate === this._maxAggregateRate) {
			return;
		}
		this._maxAggregateRate = maxAggregateRate;
		this.setUserInformation("maxAggregateRate", maxAggregateRate.toString());
    }
    
    get aggregateRateCap(): number {
		return this._aggregateRateCap;
    }
    
    get userHoldoverTime(): number {
		return this._userHoldoverTime;
	}

	set userHoldoverTime(userHoldoverTime: number) {
		if (userHoldoverTime === this._userHoldoverTime) {
			return;
		}
		this._userHoldoverTime = userHoldoverTime;
		this.setUserInformation("userHoldoverTime", userHoldoverTime.toString());
    }
    
    get maxHoldoverTime(): number {
		return this._maxHoldoverTime;
	}

	set maxHoldoverTime(maxHoldoverTime: number) {
		if (maxHoldoverTime === this._maxHoldoverTime) {
			return;
		}
		this._maxHoldoverTime = maxHoldoverTime;
		this.setUserInformation("maxHoldoverTime", maxHoldoverTime.toString());
    }
    
    get holdoverTimeCap(): number {
		return this._holdoverTimeCap;
	}
    get userRecommendations(): number {
		return this._userRecommendations;
	}

	set userRecommendations(userRecommendations: number) {
		if (userRecommendations === this._userRecommendations) {
			return;
		}
		this._userRecommendations = userRecommendations;
		this.setUserInformation("userRecommendations", userRecommendations.toString());
    }
    
    get maxRecommendations(): number {
		return this._maxRecommendations;
	}

	set maxRecommendations(maxRecommendations: number) {
		if (maxRecommendations === this._maxRecommendations) {
			return;
		}
		this._maxRecommendations = maxRecommendations;
		this.setUserInformation("maxRecommendations", maxRecommendations.toString());
    }
    
    get recommendationsCap(): number {
		return this._recommendationsCap;
	}
    get maxJobs(): number {
		return this._maxJobs;
	}

	set maxJobs(maxJobs: number) {
		if (maxJobs === this._maxJobs) {
			return;
		}
		this._maxJobs = maxJobs;
		this.setUserInformation("maxJobs", maxJobs.toString());
    }

    get jobsCap(): number {
		return this._jobsCap;
	}

    get maxMachines(): number {
		return this._maxMachines;
	}

	set maxMachines(maxMachines: number) {
		if (maxMachines === this._maxMachines) {
			return;
		}
		this._maxMachines = maxMachines;
		this.setUserInformation("maxMachines", maxMachines.toString());
    }
    
    get machinesCap(): number {
		return this._machinesCap;
	}

	get userExpertise(): number {
		return this._userExpertise;
	}

	set userExpertise(userExpertise: number) {
		if (userExpertise === this._userExpertise) {
			return;
		}
		this._userExpertise = userExpertise;
		this.setUserInformation("userExpertise", userExpertise.toString());
	}

	get proactiveUploadsEnabled(): boolean {
		return this._proactiveUploadsEnabled;
	}

	set proactiveUploadsEnabled(proactiveUploadsEnabled: boolean) {
		if (proactiveUploadsEnabled === this._proactiveUploadsEnabled) {
			return;
		}
		this._proactiveUploadsEnabled = proactiveUploadsEnabled;
		this.setUserInformation("proactiveUploadsEnabled", proactiveUploadsEnabled.toString());
	}

	get compressFilesEnabled(): boolean {
		return this._compressFilesEnabled;
	}

	set compressFilesEnabled(compressFilesEnabled: boolean) {
		if (compressFilesEnabled === this._compressFilesEnabled) {
			return;
		}
		this._compressFilesEnabled = compressFilesEnabled;
		this.setUserInformation("compressFilesEnabled", compressFilesEnabled.toString());
	}
	
	get lastPage(): number {
		return this._lastPage;
	}

	set lastPage(lastPage: number) {
		if (lastPage === this.lastPage) {
			return;
		}
		this._lastPage = lastPage;
		this.setUserInformation("lastPage", lastPage.toString());
	}
	
	get stopJobPreventEnabled(): boolean {
		return this._stopJobPreventEnabled;
	}

	set stopJobPreventEnabled(stopJobPreventEnabled: boolean) {
		if (stopJobPreventEnabled === this._stopJobPreventEnabled) {
			return;
		}
		this._stopJobPreventEnabled = stopJobPreventEnabled;
		this.setUserInformation("stopJobPreventEnabled", stopJobPreventEnabled.toString());
	}

	get deleteJobPreventEnabled(): boolean {
		return this._deleteJobPreventEnabled;
	}

	set deleteJobPreventEnabled(deleteJobPreventEnabled: boolean) {
		if (deleteJobPreventEnabled === this._deleteJobPreventEnabled) {
			return;
		}
		this._deleteJobPreventEnabled = deleteJobPreventEnabled;
		this.setUserInformation("deleteJobPreventEnabled", deleteJobPreventEnabled.toString());
	}

	get noRequirementsPreventEnabled(): boolean {
		return this._noRequirementsPreventEnabled;
	}

	set noRequirementsPreventEnabled(noRequirementsPreventEnabled: boolean) {
		if (noRequirementsPreventEnabled === this._noRequirementsPreventEnabled) {
			return;
		}
		this._noRequirementsPreventEnabled = noRequirementsPreventEnabled;
		this.setUserInformation("noRequirementsPreventEnabled", noRequirementsPreventEnabled.toString());
	}

	get noFileUploadsPreventEnabled(): boolean {
		return this._noFileUploadsPreventEnabled;
	}

	set noFileUploadsPreventEnabled(noFileUploadsPreventEnabled: boolean) {
		if (noFileUploadsPreventEnabled === this._noFileUploadsPreventEnabled) {
			return;
		}
		this._noFileUploadsPreventEnabled = noFileUploadsPreventEnabled;
		this.setUserInformation("noFileUploadsPreventEnabled", noFileUploadsPreventEnabled.toString());
	}
	
	get startSessionPreventEnabled(): boolean {
		return this._startSessionPreventEnabled;
	}

	set startSessionPreventEnabled(startSessionPreventEnabled: boolean) {
		if (startSessionPreventEnabled === this._startSessionPreventEnabled) {
			return;
		}
		this._startSessionPreventEnabled = startSessionPreventEnabled;
		this.setUserInformation("startSessionPreventEnabled", startSessionPreventEnabled.toString());
	}

	get appTracker(): AppTracker {
		return this._appTracker;
	}

	set machines(machines: Machines) {
		if (machines === this._machines) {
			return;
		}
		this._machines = machines;
	}

	get machines(): Machines {
		return this._machines;
	}

	public synchronize(responseData: any) {
		// Add apps from user information if they don't already exist
		if (responseData.jobs) {
			NEW_APPS:
			for (let newApp of responseData.jobs) {
				// Ignore this app if we already have an object for it
				for (let app of this.appTracker.finishedSessions) {
					if (app.uuid == newApp.uuid) continue NEW_APPS;
				}
				for (let app of this.appTracker.finishedJobs) {
					if (app.uuid == newApp.uuid) continue NEW_APPS;
				}
				for (let app of this.appTracker.activeSessions) {
					if (app.uuid == newApp.uuid) continue NEW_APPS;
				}
				for (let app of this.appTracker.activeJobs) {
					if (app.uuid == newApp.uuid) continue NEW_APPS;
				}
				this.appTracker.addApp(App.reconstruct(newApp));
			}
		}
	}

	private setUserInformation(param: string, value: string) {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/set-user-information";
		const init = {
			method: 'POST',
			body: JSON.stringify({
				'param': param,
				'value': value,
			})
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
		});	
	}

	public changePassword(loginName: string, oldPassword: string, newPassword: string) {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/change-password";
		const init = {
			method: 'POST',
			body: JSON.stringify({
				'loginName': loginName,
				'oldPassword': oldPassword,
				'newPassword': newPassword,
			})
		};
		return ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
		});	
	}
}
