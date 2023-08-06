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

export class Budget extends React.Component<IProps, IState> {
    private _isMounted = false;
    private polling = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
            cost: Global.lastBudgetCost,
        }
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('BudgetRender (' + new Date().getSeconds() + ')');
        return (
            <div style={{display: 'flex', margin: '6px'}}>
                <div style={{flexGrow: 1, justifyContent: 'center', fontSize: '16px', lineHeight: '30px', fontWeight: 'bold'}}>
                    Monthly Budget
                </div>
                <div style={{flexGrow: 1, justifyContent: 'center', fontSize: '14px', lineHeight: '30px', textAlign: 'right'}}>
                    <div>
                        Left: ${(Global.user.userBudget - this.state.cost).toFixed(2)}
                    </div>
                    <div>
                        Used: ${this.state.cost.toFixed(2)}
                    </div>
                </div>
            </div>
        )
    }


    private async receiveUpdate() {
		const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/get-total-billing";
        const now = new Date();
        const thisMonth = new Date(now);
        thisMonth.setDate(1);
        thisMonth.setHours(0);
        thisMonth.setMinutes(0);
        thisMonth.setSeconds(0);
        thisMonth.setMilliseconds(0);
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				startTime: thisMonth.toISOString(),
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
				this.checkAndSetState({ cost: body.total });
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
        Global.lastBudgetCost = this.state.cost;
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