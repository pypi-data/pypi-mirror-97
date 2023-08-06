/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import { Machine, NoMachine } from '../../models/machine/Machine';
import { App } from '../../models/App';

// Properties from parent
interface IProps {
	style?: React.CSSProperties
}

// Properties for this component
interface IState {
	machine: Machine[]
}

// Defaults for this component
const DefaultState: IState = {
	machine: [new NoMachine()]
}

var retrievingPreview: boolean = false;
var updatePreviewAgain: boolean = false;

export class PreviewLaunchButton extends React.Component<IProps, IState> {
	state = DefaultState;
	// We need to know if the component is mounted to change state
	_isMounted = false;
	polling = false;

	private poll = () => {
		// We will poll for a new preview every 10 seconds
		if (this.polling) setTimeout(() => this.poll(), 10000);
		this.handlePreviewClick(false);
	}

	// To understand whats going on, look at the commented out functions below
	private handlePreviewClick = (printRecommendations: boolean, bypassLimiter?: boolean) => {
		const current = Global.tracker.currentWidget;
		if (current != null) {
			// await current.context.ready;
			// current.context.save();
            // Make sure the notebook has the correct metadata.
			if (bypassLimiter || !retrievingPreview) {
				retrievingPreview = true;
				const app = new App(current.context.path, current.model.toJSON());
				app.previewNotebook(printRecommendations).then((machines: Machine[]) => {
					this.checkAndSetState({
						machine: machines,
					});
					if (updatePreviewAgain) {
						updatePreviewAgain = false;
						this.handlePreviewClick(false, true);
					} else {
						retrievingPreview = false;
					}
				}, () => {
					retrievingPreview = false;
				});
			} else {
				updatePreviewAgain = true;
			}
		}
	}

	// This is the logic of the function above incase we want to understand what it is doing easier
	// This function uses two flags, one flag keeps track of when we are actively getting an update, and one keeps track if we need to get another at the end.
	// We do this to not lose any requests that would be dropped between when we last started an update and the last request to update
	// private newHandlePreviewClick = (printRecommendations: boolean, bypassLimiter?: boolean) => {
	// 	if (bypassLimiter || !retrievingPreview) {
	// 		retrievingPreview = true;
	//		try {
	// 			// do the update
	//			...
	//			// after the update completed
	// 			if (updatePreviewAgain) {
	// 				updatePreviewAgain = false;
	// 				this.newHandlePreviewClick(false, true);
	// 			} else {
	// 				retrievingPreview = false;
	// 			}
	//		} catch (exception) {
	//			retrievingPreview = false;
	//		}
	// 	} else {
	// 		updatePreviewAgain = true;
	// 	}
	// }

	// This is the old handle code that was combined with the function above for the current handlePreviewClick
	// private oldHandlePreviewClick = (printRecommendations: boolean) => {
	// 	const current = Global.tracker.currentWidget;
	// 	if (current != null) {
	// 		const app = new App(current.context.path, current.model.toJSON(), "");
	// 		app.previewNotebook(printRecommendations).then((machine: Machine) => {
	// 			this.checkAndSetState({
	// 				machine: machine,
	// 			});
	// 		});
	// 	}
	// }

	public render(): JSX.Element {
        if (Global.shouldLogOnRender) console.log('PreviewLaunchButtonRender (' + new Date().getSeconds() + ')');
        var order = 1;
		return (
			<div style={Object.assign({width: '100%'}, this.props.style)}>
				{React.cloneElement(this.state.machine[0].getRecommendedComponent(order++), { onClick: () => this.handlePreviewClick(true, true) })}
                {Global.user.userExpertise < 2 ? (<></>) : (this.state.machine.splice(1).map(x => (<div style={{marginTop: '12px'}}>{x.getRecommendedComponent(order++)}</div>)))}
			</div>
		);
	}

	private handleMetadataChange = () => this.handlePreviewClick(false)

	// Will be called automatically when the component is mounted
	public componentDidMount = () => {
		this._isMounted = true;
		this.polling = true;
		this.poll();
		Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
		this.handlePreviewClick(false);
	}

	// Will be called automatically when the component is unmounted
	public componentWillUnmount = () => {
		Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
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
