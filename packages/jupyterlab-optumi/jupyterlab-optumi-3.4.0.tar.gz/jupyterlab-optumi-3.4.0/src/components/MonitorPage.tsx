/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';

import { App } from '../models/App';

import {
	Divider,
} from '@material-ui/core';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { Header, SubHeader } from '../core';

interface IProps {
	style?: CSSProperties
}

interface IState {}

// Defaults for this component
const DefaultState: IState = {}

export class MonitorPage extends React.Component<IProps, IState> {
	state = DefaultState;

	private generateActive = (apps: App[]) => {
		var sorted: App[] = apps.sort((n1,n2) => {
			if (n1.timestamp > n2.timestamp) {
				return -1;
			}
			if (n1.timestamp < n2.timestamp) {
				return 1;
			}
			return 0;
		});
		return sorted.map(value => (
				<div key={value.uuid} style={{padding: '6px 0px 6px 6px'}}>
					{value.getComponent()}
				</div>
			)
		);
	}

	private generateFinished = (apps: App[]) => {
		var sorted: App[] = apps.sort((n1,n2) => {
			if (n1.getEndTime() > n2.getEndTime()) {
				return -1;
			}
			if (n1.getEndTime() < n2.getEndTime()) {
				return 1;
			}
			return 0;
		});
		return sorted.map(value => (
				<div key={value.uuid} style={{padding: '6px 0px 6px 6px'}}>
					{value.getComponent()}
				</div>
			)
		);
	}

	// The contents of the component
	render() {
		if (Global.shouldLogOnRender) console.log('MonitorPageRender (' + new Date().getSeconds() + ')');
		const appTracker = Global.user.appTracker;
		return (
			<div style={Object.assign({overflowY: 'auto'}, this.props.style)}>
				<div style={{padding: '6px'}}>
					<Header title="Active" />
					{appTracker.activeSessions.length != 0 ? (
						<>
							<SubHeader title="Sessions" />
							{this.generateActive(appTracker.activeSessions)}
						</>
					) : (
						<div style={{display: 'inline-flex', width: '100%'}}>
							<SubHeader title="Sessions" grey />
							<div style={{ 
									margin: '6px 0px',
									fontSize: '14px',
									lineHeight: '18px',
									opacity: 0.5
								}}>
								(none)
							</div>
						</div>
					)}
					{appTracker.activeJobs.length != 0 ? (
						<>
							<SubHeader title="Jobs" grey />
							{this.generateActive(appTracker.activeJobs)}
						</>
					) : (
						<div style={{display: 'inline-flex', width: '100%'}}>
							<SubHeader title="Jobs" grey />
							<div style={{ 
								margin: '6px 0px',
								fontSize: '14px',
								lineHeight: '18px',
								opacity: 0.5
							}}>
								(none)
							</div>
						</div>
					)}
				</div>
				{(appTracker.finishedSessions.length != 0 || appTracker.finishedJobs.length == 0) && <Divider variant='middle' />}
				<div style={{padding: '6px'}}>
					<Header title="Finished" />
					{appTracker.finishedSessions.length != 0 ? (
						<>
							<SubHeader title="Sessions" grey />
							{this.generateFinished(appTracker.finishedSessions)}
						</>
					) : (
						<div style={{display: 'inline-flex', width: '100%'}}>
							<SubHeader title="Sessions" grey />
							<div style={{ 
								margin: '6px 0px',
								fontSize: '14px',
								lineHeight: '18px',
								opacity: 0.5
							}}>
								(none)
							</div>
						</div>
					)}
					{appTracker.finishedJobs.length != 0 ? (
						<>
							<SubHeader title="Jobs" grey />
							{this.generateFinished(appTracker.finishedJobs)}
						</>
					) : (
						<div style={{display: 'inline-flex', width: '100%'}}>
							<SubHeader title="Jobs" grey />
							<div style={{ 
								margin: '6px 0px',
								fontSize: '14px',
								lineHeight: '18px',
								opacity: 0.5
							}}>
								(none)
							</div>
						</div>
					)}
				</div>
			</div>
		);
	}

	private handleAppChange = () => { this.forceUpdate() }

	// Will be called automatically when the component is mounted
	componentDidMount = () => {
		Global.user.appTracker.appsChanged.connect(this.handleAppChange);
	}

	// Will be called automatically when the component is unmounted
	componentWillUnmount = () => {
		Global.user.appTracker.appsChanged.disconnect(this.handleAppChange);
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
