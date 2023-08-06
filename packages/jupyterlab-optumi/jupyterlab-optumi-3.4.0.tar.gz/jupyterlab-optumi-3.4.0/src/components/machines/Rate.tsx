/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import { ServerConnection } from '@jupyterlab/services';

interface IProps {
    style?: React.CSSProperties
}

interface IState {
    cost: number,
}

export class Rate extends React.Component<IProps, IState> {
    private _isMounted = false;
    private polling = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
            cost: Global.lastMachineRate,
        }
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('RateRender (' + new Date().getSeconds() + ')');

        return (
            <div style={{display: 'flex', margin: '6px'}}>
                <div style={{flexGrow: 1, justifyContent: 'center', fontSize: '16px', lineHeight: '30px', fontWeight: 'bold'}}>
                Rate
                </div>
                <div style={{flexGrow: 1, justifyContent: 'center', fontSize: '14px', lineHeight: '30px', textAlign: 'right'}}>
                    <div>
                        ${this.state.cost.toFixed(2)}/hr
                    </div>
                </div>
            </div>
        )
    }


    private async receiveUpdate() {
		const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/get-total-billing";
        const now = new Date();
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				startTime: now.toISOString(),
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
				this.checkAndSetState({ balance: body.balance, cost: body.total });
			}
		});
	}

    // Will be called automatically when the component is mounted
	componentDidMount = () => {
        this._isMounted = true;
        this.polling = true;
        this.receiveUpdate();
	}

	// Will be called automatically when the component is unmounted
	componentWillUnmount = () => {
        this._isMounted = false;
        Global.lastMachineRate = this.state.cost;
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