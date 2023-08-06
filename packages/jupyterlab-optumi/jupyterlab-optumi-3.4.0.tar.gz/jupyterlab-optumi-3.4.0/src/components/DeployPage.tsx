/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';

import { PreviewLaunchButton } from './deploy/PreviewLaunchButton';
import { NotebookPanel } from '@jupyterlab/notebook';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { OptumiMetadataTracker } from '../models/OptumiMetadataTracker';
import { IntentSlider } from '../core';
import { FilesPanel } from './deploy/FilesPanel';
import { ResourcesPanel } from './deploy/resources/ResourcesPanel';
import { LaunchMode } from './deploy/resources/LaunchMode';
import ExtraInfo from '../utils/ExtraInfo';

interface IProps {
	style?: CSSProperties
	openUserDialogTo?: (page: number) => Promise<void> // This is somewhat spaghetti code-y, maybe think about revising
}

interface IState {}

// Defaults for this component
const DefaultState: IState = {}

export class DeployPage extends React.Component<IProps, IState> {
	state = DefaultState;
	// We need to know if the component is mounted to change state
	_isMounted = false;

	private getValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
		return optumi.metadata.intent;
	}

	private async saveValue(intent: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
		optumi.metadata.intent = intent;
		tracker.setMetadata(optumi);
	}

	constructor(props: IProps) {
		super(props)
		if (Global.tracker.currentWidget != null) {
			Global.tracker.currentWidget.context.ready.then(() => {if (this._isMounted) this.forceUpdate()})
		}
	}

	// The contents of the component
	render() {
		if (Global.shouldLogOnRender) console.log('DeployPageRender (' + new Date().getSeconds() + ')');
		return (
			<div style={Object.assign({overflow: 'auto'}, this.props.style)}>
				{((Global.labShell.currentWidget instanceof NotebookPanel) && (Global.tracker.currentWidget != null) && (Global.tracker.currentWidget.context.isReady)) ? (
					<>
						<div style={{padding: '6px 20px'}}>
							<ExtraInfo reminder={Global.tracker.currentWidget.context.path}>
								<div style={{margin: '6px', opacity: 0.5, fontStyle: 'italic', overflow: 'hidden', textOverflow: 'ellipsis'}}>
									{'Notebook: ' + Global.tracker.currentWidget.context.path.split('/').pop()}
								</div>
							</ExtraInfo>
							<FilesPanel openUserDialogTo={this.props.openUserDialogTo} />
							<LaunchMode />
							<ResourcesPanel />
							<IntentSlider
								color={'#10A0F9'}
								getValue={this.getValue}
								saveValue={this.saveValue}
							/>
						</div>
						<PreviewLaunchButton style={{padding: '6px'}}/>
					</>
				) : (
					<div style={{ textAlign: 'center', padding: "16px" }}>
						Open a notebook to get started...
					</div>
				)}
			</div>
		);
	}

	handleLabShellChange = () => this.forceUpdate()
    handleTrackerChange = () => this.forceUpdate()
    handleMetadataChange = () => this.forceUpdate()
	handleUserChange = () => {
		this.forceUpdate()
	}

	// Will be called automatically when the component is mounted
	componentDidMount = () => {
		this._isMounted = true;
        Global.labShell.currentChanged.connect(this.handleLabShellChange);
		Global.tracker.currentChanged.connect(this.handleTrackerChange);
        Global.tracker.selectionChanged.connect(this.handleTrackerChange);
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
		Global.onUserChange.connect(this.handleUserChange)
		this.handleUserChange()
	}

	// Will be called automatically when the component is unmounted
	componentWillUnmount = () => {
		Global.labShell.currentChanged.disconnect(this.handleLabShellChange);
		Global.tracker.currentChanged.disconnect(this.handleTrackerChange);
        Global.tracker.selectionChanged.disconnect(this.handleTrackerChange);
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
		Global.onUserChange.disconnect(this.handleUserChange)
		this._isMounted = false;
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
