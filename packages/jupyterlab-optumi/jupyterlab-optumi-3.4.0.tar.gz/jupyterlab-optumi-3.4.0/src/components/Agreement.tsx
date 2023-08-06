/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Button, Checkbox, Divider } from '@material-ui/core';
import * as React from 'react'
import { Global } from '../Global';
import { ServerConnection } from '@jupyterlab/services';

interface IProps {
    callback: () => void;
}

interface IState {
    agreed: boolean,
}

export class Agreement extends React.Component<IProps, IState> {
    _isMounted = false

    constructor(props: IProps) {
        super(props)
        this.state = {
            agreed: false,
        }
    }

    // Log out of the REST interface (Copied from SettingsPage aside from setState call)
	private logout = () => {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/logout";
		const init = {
			method: 'GET',
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
            Global.user = null;
            this.checkAndSetState({open: false})
		});
	}

    private acceptAgreement = () => {
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/sign-agreement";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				timeOfSigning: new Date().toISOString(),
			}),
		};
		return ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.text();
		}).then((body: string) => {
            Global.user.unsignedAgreement = false;
            this.props.callback();
		});
    }

    public render = (): JSX.Element => {
        return (
            <>
                <div className='jp-optumi-logo'/>
                <div style={{
                    display: 'flex',
                    flexFlow: 'column',
                    overflow: 'hidden',
                    height: '100%',
                }}>
                    <div
                        style={{
                            padding: '0px',
                            flexGrow: 1,
                            // overflowY: 'auto',
                            overflowY: 'hidden',
                            whiteSpace: 'pre-wrap',
                            backgroundColor: 'white'
                        }}
                    >
                        <embed  src={Global.agreementURL} height='100%' width='100%' />
                    </div>
                    <Divider variant='middle' />
                    <div style={{padding: '6px', display: 'flex', justifyContent: 'center'}}>
                        <Checkbox
                            checked={this.state.agreed}
                            color='primary'
                            onClick={() => this.checkAndSetState({ agreed: !this.state.agreed})}
                            style={{
                                padding: '6px',
                                margin: '0px',
                                flexGrow: 1,
                            }}
                        />
                        <div 
                            style={{
                                padding: '6px',
                                margin: '0px',
                                flexGrow: 1,
                                fontWeight: 'bold'
                            }}
                        >
                            I have read and I agree to the Optumi Terms and Conditions of Service
                        </div>
                    </div>
                    <div style={{padding: '6px', display: 'flex', justifyContent: 'center'}}>
                        <Button
                            onClick={this.logout}
                            style={{
                                padding: '9px',
                                fontWeight: 'bold',
                                fontSize: '14px',
                                lineHeight: '14px',
                                margin: '0px',
                                flexGrow: 1,
                            }}
                        >
                            Logout
                        </Button>
                        <Button
                            onClick={this.acceptAgreement}
                            color='primary'
                            variant='contained'
                            disabled={!this.state.agreed}
                            style={{
                                padding: '9px',
                                fontWeight: 'bold',
                                fontSize: '14px',
                                lineHeight: '14px',
                                margin: '0px',
                                flexGrow: 1,
                            }}
                        >
                            I accept
                        </Button>
                    </div>
                </div>
            </>
        )
    }

    private checkAndSetState = (map: any) => {
        if (this._isMounted) {
            this.setState(map)
        }
    }

    public componentDidMount = () => {
        this._isMounted = true
    }

    public componentWillUnmount = () => {
        this._isMounted = false
    }
}
