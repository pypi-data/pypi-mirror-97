/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';

import { DeployPage } from './DeployPage';
import { MonitorPage } from './MonitorPage';

import {
	Tabs,
	Tab,
	Badge,
	SvgIcon,
} from '@material-ui/core';

import { MachinesPage } from './MachinesPage';
import { ShadowedDivider } from '../core';

import { withSnackbar, WithSnackbarProps } from 'notistack';
import { Snackbar } from '../models/Snackbar';
import { UserDialog } from './UserDialog';

// Properties from parent
interface IProps extends WithSnackbarProps {}

enum Page {
	Deploy = 0,
	Monitor = 1,
	Machines = 2,
}

// Properties for this component
interface IState {
	page: Page;
	deployDisabled: boolean;
}

class Pilot extends React.Component<IProps, IState> {
	_isMounted = false;
	openUserDialogTo: (page: number) => Promise<void> = () => new Promise<void>(resolve => resolve()) // This is somewhat spaghetti code-y, maybe think about revising

	constructor(props: IProps) {
		super(props);
		this.state = {
			page: Global.user.lastPage,
			deployDisabled: false,
		}
	}

	private handleTabChange = (event: React.ChangeEvent<{}>, newValue: Page) => {
		this.checkAndSetState({ page: newValue });
		Global.user.lastPage = newValue;
	}

	// The contents of the component
	render() {
		if (Global.shouldLogOnRender) console.log('PilotRender (' + new Date().getSeconds() + ')');
		return (
			<>
				<div style={{paddingBottom: "5px", textAlign: 'center', verticalAlign: 'middle'}}>
                    <div style={{display: 'inline-flex', width: '100%'}}>
						<a href='https://www.optumi.com' target='_blank'>
							<div className='jp-optumi-logo' />
						</a>
						<UserDialog style={{margin: 'auto 6px auto auto'}} getOpenTo={(openTo: (page: number) => Promise<void>) => {this.openUserDialogTo = openTo; this.forceUpdate()}} />
					</div>
					<Tabs
						value={this.state.page}
						onChange={this.handleTabChange}
						variant="fullWidth"
						indicatorColor="primary"
						textColor="primary"
						style={{margin: '0px 6px'}}
					>
						<Tab
							icon={
								<SvgIcon viewBox="0, 0, 400,446" style={{width: '28px', height: '28px'}}>
									<path d="M348.000 58.232 C 324.618 61.984,306.000 66.674,306.000 68.813 C 306.000 71.851,369.545 135.122,371.067 133.599 C 372.905 131.761,382.000 74.336,382.000 64.567 L 382.000 56.000 370.500 56.234 C 364.175 56.362,354.050 57.262,348.000 58.232 M261.029 86.235 C 214.374 111.539,184.827 137.455,151.438 182.354 C 131.859 208.683,134.247 207.280,105.973 209.077 C 77.646 210.877,78.107 210.586,46.111 246.944 C 14.709 282.628,13.657 285.006,24.595 295.608 C 33.914 304.640,38.535 303.841,62.774 289.000 C 74.453 281.850,85.356 276.000,87.004 276.000 C 90.397 276.000,91.021 279.133,88.000 281.000 C 80.966 285.347,86.211 293.260,115.524 322.525 C 145.290 352.241,154.153 357.842,159.000 350.000 C 161.093 346.613,163.948 347.791,162.638 351.500 C 161.957 353.425,155.685 364.580,148.700 376.288 C 133.629 401.551,133.207 405.011,144.006 414.767 C 155.049 424.744,153.659 425.401,190.701 392.696 C 227.821 359.922,227.156 360.976,229.004 332.000 C 230.748 304.673,229.916 306.203,252.454 288.864 C 308.578 245.687,341.585 206.858,361.005 161.165 C 368.325 143.941,367.373 141.488,347.134 125.396 C 330.680 112.314,319.724 100.874,305.577 82.000 C 295.803 68.959,292.260 69.296,261.029 86.235 M281.518 145.989 C 295.397 154.451,299.651 169.944,291.460 182.204 C 279.075 200.744,254.612 198.973,245.060 178.845 C 234.650 156.906,260.788 133.350,281.518 145.989 M65.116 318.984 C 41.834 327.278,33.655 343.820,22.828 404.507 C 19.046 425.702,19.740 429.180,26.337 422.099 C 32.573 415.406,48.022 408.969,72.496 402.867 C 109.336 393.683,120.097 382.787,119.904 354.869 L 119.808 341.000 116.404 347.823 C 111.679 357.294,105.398 361.342,88.000 366.125 C 79.750 368.394,70.975 371.564,68.500 373.171 C 63.012 376.734,63.005 376.424,68.070 354.701 C 73.737 330.396,81.234 320.000,93.094 320.000 C 94.692 320.000,96.000 319.100,96.000 318.000 C 96.000 315.041,74.239 315.734,65.116 318.984 " />
								</SvgIcon>
							} /*label="DEPLOY"*/ style={{minWidth: "72px"}} />
						<Tab 
							icon={
								<Badge
									badgeContent={Global.user.appTracker.getDisplayNum()}
									color={"primary"}>
										<SvgIcon viewBox="0, 0, 400,400" style={{width: '28px', height: '28px'}}>
											<path d="M184.000 75.671 C 157.886 84.352,136.646 102.091,124.338 125.500 L 117.765 138.000 105.383 138.035 C 90.924 138.075,71.538 141.909,56.000 147.801 C -14.626 174.580,-18.484 281.128,49.988 313.831 L 65.000 321.000 203.705 321.553 L 342.409 322.106 353.376 317.085 C 385.732 302.272,399.199 277.664,397.610 236.256 C 396.006 194.437,366.443 166.000,324.574 166.000 C 319.271 166.000,315.638 165.024,315.269 163.500 C 304.910 120.762,285.610 93.164,256.447 79.388 C 239.169 71.226,202.961 69.368,184.000 75.671 M244.970 147.777 C 301.927 179.760,259.786 271.237,199.913 245.586 L 192.826 242.549 169.913 267.273 C 142.622 296.721,133.842 300.366,127.894 284.720 C 125.394 278.145,125.295 278.289,151.476 250.369 L 173.952 226.400 169.629 216.700 C 148.789 169.946,200.388 122.743,244.970 147.777 M206.094 158.498 C 190.267 163.800,177.795 184.895,181.098 200.776 C 190.562 246.287,256.850 241.187,256.856 194.948 C 256.859 168.669,231.052 150.138,206.094 158.498 " />
										</SvgIcon>
								</Badge>
							} /*label="MONITOR"*/ style={{minWidth: "72px"}} />
						<Tab 
							icon={
								<SvgIcon viewBox="0, 0, 400,200" style={{width: '28px', height: '28px'}}>
									<path d="M0.000 40.000 L 0.000 80.000 200.000 80.000 L 400.000 80.000 400.000 40.000 L 400.000 0.000 200.000 0.000 L 0.000 0.000 0.000 40.000 M80.000 40.000 L 80.000 60.000 60.000 60.000 L 40.000 60.000 40.000 40.000 L 40.000 20.000 60.000 20.000 L 80.000 20.000 80.000 40.000 M0.000 160.000 L 0.000 200.000 200.000 200.000 L 400.000 200.000 400.000 160.000 L 400.000 120.000 200.000 120.000 L 0.000 120.000 0.000 160.000 M80.000 160.000 L 80.000 180.000 60.000 180.000 L 40.000 180.000 40.000 160.000 L 40.000 140.000 60.000 140.000 L 80.000 140.000 80.000 160.000 " />
								</SvgIcon>
							} /*label="MACHINES"*/ style={{minWidth: "72px"}} />
					</Tabs>
				</div>
				<ShadowedDivider />
				{this.state.page == Page.Deploy ? (
					<DeployPage style={{flexGrow: 1}} openUserDialogTo={this.openUserDialogTo} />
				) : this.state.page == Page.Monitor ? (
					<MonitorPage style={{flexGrow: 1}} />
				) : this.state.page == Page.Machines ? (
					<MachinesPage style={{flexGrow: 1}} />
				) : (
					<></>
				)}
			</>
		);
	}

    private handleSnackbarChange = (sender: Global, snackbar: Snackbar) => this.props.enqueueSnackbar(snackbar.message, snackbar.options)
    private handleAppsChange = () => this.forceUpdate()
	private handleJobLaunched = () => this.checkAndSetState({ page: Page.Monitor })

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
		this._isMounted = true;
        Global.user.appTracker.appsChanged.connect(this.handleAppsChange);
		Global.snackbarChange.connect(this.handleSnackbarChange);
		Global.jobLaunched.connect(this.handleJobLaunched);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
        Global.user.appTracker.appsChanged.disconnect(this.handleAppsChange);
		Global.snackbarChange.disconnect(this.handleSnackbarChange);
		Global.jobLaunched.disconnect(this.handleJobLaunched);
		this._isMounted = false;
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


const SnackbarPilot = withSnackbar(Pilot);
export { SnackbarPilot as Pilot }
