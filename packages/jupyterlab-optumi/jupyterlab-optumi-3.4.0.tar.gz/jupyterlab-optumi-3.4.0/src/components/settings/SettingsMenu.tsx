/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import { ServerConnection } from '@jupyterlab/services';

import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { ChangePasswordPopup } from './ChangePasswordPopup';
import { CheckoutForm } from './CheckoutForm';
import { Header, Switch, TextBox, TextBoxDropdown } from '../../core';
import FormatUtils from '../../utils/FormatUtils';
import { Button, Divider } from '@material-ui/core';
import GetAppIcon from '@material-ui/icons/GetApp';
import DataConnectorBrowser, { DataConnectorMetadata } from '../deploy/dataConnectorBrowser/DataConnectorBrowser';
import { AmazonS3ConnectorPopup } from '../deploy/AmazonS3ConnectorPopup';
import { GoogleCloudStorageConnectorPopup } from '../deploy/GoogleCloudStorageConnectorPopup';
import { GoogleDriveConnectorPopup } from '../deploy/GoogleDriveConnectorPopup';
import { KaggleConnectorPopup } from '../deploy/KaggleConnectorPopup';
import { WasabiConnectorPopup } from '../deploy/WasabiConnectorPopup';

// Properties from parent
interface IProps {
	style?: CSSProperties
}

// Properties for this component
interface IState {}

const emUpSub = 'Upgrade subscription to unlock'

const LABEL_WIDTH = '68px'

interface IAccountGeneralSubMenuState {}

export class AccountGeneralSubMenu extends React.Component<IProps, IAccountGeneralSubMenuState> {

    constructor(props: IProps) {
        super(props);
        this.state = {}
    }

    private getPasswordValue(): string { return '******' }
    private savePasswordValue(password: string) {
        Global.user.changePassword("", "", password);
    }

    private getCompressFilesEnabledValue(): boolean { return Global.user.compressFilesEnabled }
    private saveCompressFilesEnabledValue(compressFilesEnabled: boolean) { Global.user.compressFilesEnabled = compressFilesEnabled }

    public render = (): JSX.Element => {
        return (
            <>
                <div style={Object.assign({padding: '6px'}, this.props.style)}>
                    {/* <ResourceTextBox<string>
                        getValue={this.getNameValue}
                        label='Name'
                        editPressRequired
                    /> */}
                    <div style={{display: 'inline-flex', width: '100%'}}>
                        <TextBox<string>
                            style={{flexGrow: 1}}
                            getValue={this.getPasswordValue}
                            saveValue={this.savePasswordValue}
                            label='Password'
                            labelWidth={LABEL_WIDTH}
                        />
                        <ChangePasswordPopup style={{margin: '8px 0px', height: '20px', fontSize: '12px', lineHeight: '12px'}}/>
                    </div>
                    {/* <ExtraInfo
                        reminder={`Compress files before uploading`}
                    > */}
                    <Switch
                        getValue={this.getCompressFilesEnabledValue}
                        saveValue={this.saveCompressFilesEnabledValue}
                        label='Compress my files before uploading'
                        labelWidth={LABEL_WIDTH}
                    />
                    {/* </ExtraInfo> */}
                    {/* <ResourceSwitch
                        tooltip='Start uploading files&#10;before launching'
                        getValue={() => false}
                        saveValue={() => {}}
                        label='Preupload'
                    /> */}
                </div>
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
}

interface IAccountLimitsSubMenuState {
    holdoverFocused: boolean;
    budgetFocused: boolean;
    recsFocused: boolean;
}

export class AccountLimitsSubMenu extends React.Component<IProps, IAccountLimitsSubMenuState> {

    constructor(props: IProps) {
        super(props);
        this.state = {
            holdoverFocused: false,
            budgetFocused: false,
            recsFocused: false,
        }
    }
    private getUserBudgetValue(): number { return Global.user.userBudget }
    private saveUserBudgetValue(userBudget: number) { Global.user.userBudget = userBudget }

    private getUserRecommendationsValue(): number { return Global.user.userRecommendations }
    private saveUserRecommendationsValue(userRecommendations: number) { Global.user.userRecommendations = userRecommendations }

    private getMaxJobsValue(): number { return Global.user.maxJobs }
    private saveMaxJobsValue(value: number) { Global.user.maxJobs = value }

    private getMaxMachinesValue(): number { return Global.user.maxMachines }
    private saveMaxMachinesValue(value: number) { Global.user.maxMachines = value }

    private getUserHoldoverTimeValue(): number { return Global.user.userHoldoverTime }
    private saveUserHoldoverTimeValue(userHoldoverTime: number) { Global.user.userHoldoverTime = userHoldoverTime }

    public render = (): JSX.Element => {
        return (
            <>
                <div style={Object.assign({padding: '6px'}, this.props.style)}>
                    {Global.user.userExpertise > 0 ? (<TextBox<number>
                        getValue={this.getUserBudgetValue}
                        saveValue={this.saveUserBudgetValue}
                        styledUnitValue={(value: number) => '$' + value.toFixed(2)}
                        unstyleUnitValue={(value: string) => { return value.replace('$', '').replace('.', '').replace(/\d/g, '').length > 0 ? Number.NaN : Number.parseFloat(value.replace('$', '')) }}
                        label='Budget'
                        labelWidth={LABEL_WIDTH}
                        onFocus={() => this.setState({budgetFocused: true})}
                        onBlur={() => this.setState({budgetFocused: false})}
                        helperText={this.state.budgetFocused ? `Must be between $1 and $${Global.user.maxBudget}` : 'Max monthly spend'}
                        minValue={1}
                        maxValue={Global.user.maxBudget}
                        // disabledMessage={Global.user.userExpertise < 2 ? emUpSub : ''}
                    />) : (<></>)}
                    <TextBox<number>
                        getValue={this.getUserRecommendationsValue}
                        saveValue={this.saveUserRecommendationsValue}
                        label='Alternatives'
                        labelWidth={LABEL_WIDTH}
                        onFocus={() => this.setState({recsFocused: true})}
                        onBlur={() => this.setState({recsFocused: false})}
                        helperText={this.state.recsFocused ? `Must be between 1 and ${Global.user.maxRecommendations}` : 'Number of machines considered'}
                        minValue={1}
                        maxValue={Global.user.maxRecommendations}
                        disabledMessage={Global.user.userExpertise < 2 ? emUpSub : ''}
                    />
                    <TextBox<number>
                        getValue={this.getMaxJobsValue}
                        saveValue={this.saveMaxJobsValue}
                        unstyleUnitValue={(value: string) => { return value.replace(/\d/g, '').length > 0 ? Number.NaN : Number.parseFloat(value) }}
                        label='Jobs'
                        labelWidth={LABEL_WIDTH}
                        helperText={'Max number of concurrent jobs'}
                        disabledMessage={emUpSub}
                    />
                    <TextBox<number>
                        getValue={this.getMaxMachinesValue}
                        saveValue={this.saveMaxMachinesValue}
                        unstyleUnitValue={(value: string) => { return value.replace(/\d/g, '').length > 0 ? Number.NaN : Number.parseFloat(value) }}
                        label='Machines'
                        labelWidth={LABEL_WIDTH}
                        helperText='Max number of concurrent machines'
                        disabledMessage={emUpSub}
                    />
                    <TextBoxDropdown
                        getValue={this.getUserHoldoverTimeValue}
                        saveValue={this.saveUserHoldoverTimeValue}
                        unitValues={[
                            {unit: 'seconds', value: 1},
                            {unit: 'minutes', value: 60},
                            {unit: 'hours', value: 3600},
                        ]}
                        label='Holdover'
                        labelWidth={LABEL_WIDTH}
                        onFocus={() => this.setState({holdoverFocused: true})}
                        onBlur={() => this.setState({holdoverFocused: false})}
                        helperText={this.state.holdoverFocused ? `Must be between 0 seconds and ${Global.user.maxHoldoverTime / 3600} hours` : 'Time before releasing idle machines'}
                        minValue={0}
                        maxValue={Global.user.maxHoldoverTime}
                    />
                </div>
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
}

interface IAccountPaymentSubMenuState {
    balance: number;
    billing: any[];
}

export class AccountPaymentSubMenu extends React.Component<IProps, IAccountPaymentSubMenuState> {
    private _isMounted = false;
    private polling = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
            balance: 0,
            billing: [],
        }
    }

    private getDuration = (record: any): string => {
        var endTime = new Date(record.endTime as string);
        var startTime = new Date(record.startTime as string);
        var diff = endTime.getTime() - startTime.getTime();
        const stillRunning = diff < 0;
        if (stillRunning) {
            diff = new Date().getTime() - startTime.getTime();
        }
        var time = FormatUtils.msToTime(diff).split(':');
        var formatted;
        if (time.length == 3) {
            formatted = time[0] + 'h ' + time[1] + 'm ' + time[2] + 's';
        } else {
            formatted = time[0] + 'm ' + time[1] + 's';
        }
        return stillRunning ? formatted + ' (still running)' : formatted;
    }

    private getCost = (record: any): string => {
        var endTime = new Date(record.endTime as string);
        var startTime = new Date(record.startTime as string);
        var diff = endTime.getTime() - startTime.getTime();
        const stillRunning = diff < 0;
        if (stillRunning) {
            diff = new Date().getTime() - startTime.getTime();
        }
        var formatted = '$' + ((diff / 3600000) * record.machine.rate).toFixed(2);
        return stillRunning ? formatted + ' (still running)' : formatted;
    }

    public render = (): JSX.Element => {
        return (
            <>
                <div style={Object.assign({padding: '6px'}, this.props.style)}>
                    <div style={{display: 'inline-flex', width: '100%', padding: '3px 0px'}}>
                        <div 
                            style={{
                            lineHeight: '24px',
                            margin: '0px 12px',
                            flexGrow: 1,
                        }}
                        >
                            {'Remaining balance:'}
                        </div>
                        <div style={{padding: '0px 6px 0px 6px'}}>
                            {'$' + (-this.state.balance).toFixed(2)}
                        </div>
                    </div>
                    <CheckoutForm />
                    <div style={{padding: '6px', width: '100%'}}>
                        <Button
                            variant="outlined"
                            color="primary"
                            startIcon={<GetAppIcon />}
                            style={{width: '100%'}}
                            onClick={() => this.getDetailedBilling(true)}
                        >
                            Billing records
                        </Button>
                    </div>
                </div>
            </>
        )
    }

    private async receiveUpdate() {
		const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/get-total-billing";
        const now = new Date();
        const epoch = new Date(0);
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				startTime: epoch.toISOString(),
				endTime: now.toISOString(),
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			if (this.polling) {
				// If we are polling, send a new request in 2 seconds
				setTimeout(() => this.receiveUpdate(), 2000);
			}
			Global.handleResponse(response);
			return response.json();
		}).then((body: any) => {
			if (body) {
                this.checkAndSetState({ balance: body.balance });
			}
        });
    }
    
    private getDetailedBilling = (save: boolean) => {
        const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/get-detailed-billing";
        const now = new Date();
        const epoch = new Date(0);
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				startTime: epoch.toISOString(),
				endTime: now.toISOString(),
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
			if (body) {
                this.checkAndSetState({ billing: body.records });
                if (save) {
                    const data: string[][] = [];
                    var sorted: any[] = body.records.sort((n1: any, n2: any) => {
                        if (n1.startTime > n2.startTime) {
                            return -1;
                        }
                        if (n1.startTime < n2.startTime) {
                            return 1;
                        }
                        return 0;
                    });
                    for (let record of sorted) {
                        const machine = record.machine;
                        data.push(
                            [
                                new Date(record.startTime).toLocaleString().replace(/,/g, ''),
                                new Date(0).toISOString() == new Date(record.endTime).toISOString() ? 'Still running' : new Date(record.endTime).toLocaleString().replace(/,/g, ''),
                                this.getDuration(record),
                                '$' + machine.rate.toFixed(2),
                                this.getCost(record),
                                machine.graphicsNumCards > 0 ? (machine.graphicsNumCards + 'x' + machine.graphicsCardType) : 'No GPU',
                                machine.computeCores + ' cores',
                                FormatUtils.styleCapacityUnitValue()(machine.memorySize),
                                FormatUtils.styleCapacityUnitValue()(machine.storageSize)
                            ]
                        );
                    }

                    const headers = [
                        ["Start Time", "End Time", "Duration", "Rate ($/hr)", "Cost", "GPU", "CPU", "RAM", "Disk"]
                    ];
                                        
                    const csvContent = "data:text/csv;charset=utf-8," 
                        + headers.map(e => e.join(",")).join("\n") + '\n'
                        + data.map(e => e.join(",")).join("\n") + '\n';

                    var encodedUri = encodeURI(csvContent);
                    var link = document.createElement("a");
                    link.setAttribute("href", encodedUri);
                    link.setAttribute("download", "billing_records.csv");
                    document.body.appendChild(link); // Required for FF
                    link.click();
                }
			}
        });
    }

    // Will be called automatically when the component is mounted
	componentDidMount = () => {
        this._isMounted = true;
        this.getDetailedBilling(false);
        this.polling = true;
        this.receiveUpdate();
	}

	// Will be called automatically when the component is unmounted
	componentWillUnmount = () => {
        this._isMounted = false;
        this.polling = false;
    }
    
    private checkAndSetState = (map: any) => {
		if (this._isMounted) {
			this.setState(map);
		}
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
}

interface IAccountConnectorsSubMenuState {
    dataConnectors: DataConnectorMetadata[],
    browserKey: number,
}

export class AccountConnectorsSubMenu extends React.Component<IProps, IAccountConnectorsSubMenuState> {
    private _isMounted = false

    constructor(props: IProps) {
        super(props);
        this.state = {
            dataConnectors: [],
            browserKey: 0,
        }
    }

    // Use a key to force the data connector browser to refresh
    private forceNewBrowser = () => {
        this.setState({ browserKey: this.state.browserKey + 1 })
    }

    public request = async () => {
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + 'optumi/get-data-connectors'
		return ServerConnection.makeRequest(url, {}, settings).then(response => {
			if (response.status !== 200) throw new ServerConnection.ResponseError(response);
			return response.json()
		})
    }

    public render = (): JSX.Element => {
        return (
            <>
                <div style={Object.assign({}, this.props.style)}>
                    <div style={{display: 'inline-flex', margin: '6px'}}>
                        <Header title='Existing Connectors' style={{ lineHeight: '24px', margin: '6px 6px 6px 11px' }} />
                    </div>
                    <Divider />
                    <DataConnectorBrowser
                        key={this.state.browserKey}
                        style={{
                            maxHeight: 'calc(100% - 60px - 2px)',
                        }}
                        handleDelete={(dataConnectorMetadata: DataConnectorMetadata) => {
                            const settings = ServerConnection.makeSettings();
                            const url = settings.baseUrl + "optumi/remove-data-connector";
                            const init: RequestInit = {
                                method: 'POST',
                                body: JSON.stringify({
                                    name: dataConnectorMetadata.name,
                                }),
                            };
                            ServerConnection.makeRequest(
                                url,
                                init, 
                                settings
                            ).then((response: Response) => {
                                Global.handleResponse(response);
                            }).then(() => {
                                var newDataConnectors = this.state.dataConnectors
                                newDataConnectors = newDataConnectors.filter(dataConnector => dataConnector.name !== dataConnectorMetadata.name)
                                this.setState({dataConnectors: newDataConnectors})
                                this.forceNewBrowser()
                            });                            
                        }}
                    />
                    <Divider style={{marginTop: '33px'}}/>
                    <div style={{display: 'inline-flex', margin: '6px'}}>
                        <Header title='New Connectors' style={{ lineHeight: '24px', margin: '6px 6px 6px 11px'  }} />
                    </div>
                    <Divider />
                    <div style={{marginBottom: '6px'}} />
                    <AmazonS3ConnectorPopup handleClose={this.forceNewBrowser} />
                    <GoogleCloudStorageConnectorPopup handleClose={this.forceNewBrowser} />
                    <GoogleDriveConnectorPopup handleClose={this.forceNewBrowser} />
                    <KaggleConnectorPopup handleClose={this.forceNewBrowser} />
                    <WasabiConnectorPopup handleClose={this.forceNewBrowser} />
                </div>
            </>
        )
    }

    public componentDidMount = () => {
        this._isMounted = true
        this.request().then(json => {
            if (this._isMounted) this.setState({dataConnectors: json.connectors});
        })
    }

    public componentWillUnmount = () => {
        this._isMounted = false
    }

    public shouldComponentUpdate = (nextProps: IProps, nextState: IAccountConnectorsSubMenuState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender')
            return false;
        } catch (error) {
            return true;
        }
    }
}

export class TeamSubMenu extends React.Component<IProps, IState> {
    public render = (): JSX.Element => {
        return (
            <Header title='Members' />
        )
    }
}
