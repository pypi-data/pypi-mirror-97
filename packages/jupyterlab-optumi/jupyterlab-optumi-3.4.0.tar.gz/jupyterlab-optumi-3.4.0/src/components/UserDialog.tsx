/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Button, Dialog, DialogContent, IconButton, Tab, Tabs, withStyles } from '@material-ui/core';
import * as React from 'react';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import CloseIcon from '@material-ui/icons/Close';
import { Global } from '../Global';
import { ServerConnection } from '@jupyterlab/services';
import { AccountConnectorsSubMenu, AccountGeneralSubMenu, AccountLimitsSubMenu, AccountPaymentSubMenu } from './settings/SettingsMenu';
import { ShadowedDivider } from '../core';
import { User } from '../models/User';
import WarningPopup from '../core/WarningPopup';
import { App } from '../models/App';

const StyledDialog = withStyles({
    paper: {
        width: 'calc(min(80%, 600px + 150px + 2px))',
        // width: '100%',
        height: '80%',
        overflowY: 'visible',
        backgroundColor: 'var(--jp-layout-color1)',
        maxWidth: 'inherit',
    },
})(Dialog);

export const enum Page {
    GENERAL = 0,
    LIMITS = 1,
    PAYMENT = 2,
    CONNECTORS = 3,
}

interface IProps {
    style?: CSSProperties
    onOpen?: () => void
	onClose?: () => void
    getOpenTo?: (openTo: (page: Page) => Promise<void>) => void // This is somewhat spaghetti code-y, maybe think about revising
}

interface IState {
    open: boolean,
    selectedPanel: number,
    showLogoutWithSessionPopup: boolean,
}

// TODO:Beck The popup needs to be abstracted out, there is too much going on to reproduce it in more than one file
export class UserDialog extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props);
		this.state = {
            open: false,
            selectedPanel: Page.GENERAL,
            showLogoutWithSessionPopup: false,
		};
    }

    private resolveOpenToPromise: undefined | ((value: void | PromiseLike<void>) => void) = undefined
    public openTo = (page: Page) => {
        this.setState({open: true, selectedPanel: page})
        return new Promise<void>(resolve => {
            this.resolveOpenToPromise = resolve
        })
    }
    
    private handleClickOpen = () => {
        if (this.props.onOpen) this.props.onOpen()
		this.setState({ open: true, selectedPanel: Page.GENERAL });
	}

	private handleClose = () => {
        this.setState({ open: false });
        if (this.props.onClose) this.props.onClose();
        if (this.resolveOpenToPromise) {
			this.resolveOpenToPromise()
			this.resolveOpenToPromise = undefined
		}
	}

    private handleStopClicked = (app: App) => {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/stop-notebook";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				uuid: app.uuid,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init,
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
		});
	}

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('UsersDialogRender (' + new Date().getSeconds() + ')');
        var defaultProfilePicture: string = Global.user.name.replace(/(?<=\B)\w+/g, '').replace(/[ ]/g, '').toUpperCase()
        return (
            <div style={Object.assign({}, this.props.style)} >
                <IconButton
                    onClick={this.handleClickOpen}
                    style={{
                        display: 'inline-block',
                        width: '36px',
                        height: '36px',
                        padding: '3px',
                    }}
                >
                    <div style={{
                        width: '24px',
                        height: '24px',
                        // margin: '6px auto',
                        borderRadius: '12px',
                        backgroundColor: '#10A0F9',
                        color: 'white',
                        fontSize: '18px',
                        fontWeight: 'bold',
                        lineHeight: '24px',
                        textAlign: 'center'
                    }}>
                        {defaultProfilePicture[defaultProfilePicture.length-1]}
                    </div>
                </IconButton>
                <StyledDialog
					open={this.state.open}
					onClose={this.handleClose}
                    scroll='paper'
				>
					<MuiDialogTitle
					    disableTypography
                        style={{
                            display: 'inline-flex',
                            backgroundColor: 'var(--jp-layout-color2)',
                            height: '60px',
                            padding: '6px',
                            borderRadius: '4px',
                        }}
                    >
                        <div style={{
                            display: 'inline-flex',
                            minWidth: '150px',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            paddingRight: '12px', // this is 6px counteracting the MuiDialogTitle padding and 6px aligning the padding to the right of the tabs
                        }}>
                            <div style={{margin: 'auto', paddingLeft: '12px'}}>
            					Settings
                            </div>
                        </div>
                        <div style={{flexGrow: 1}} />
                        <div>
                            <WarningPopup
                                open={this.state.showLogoutWithSessionPopup}
                                headerText="Are you sure?"
                                bodyText={`You have a session that is currently active. If you log out, your session will be closed.`}
                                cancel={{
                                    text: `Cancel`,
                                    onCancel: (prevent: boolean) => {
                                        this.setState({ showLogoutWithSessionPopup: false })
                                    },
                                }}
                                continue={{
                                    text: `Close it`,
                                    onContinue: (prevent: boolean) => {
                                        this.setState({ showLogoutWithSessionPopup: false })
                                        for (let app of Global.user.appTracker.activeSessions) {
                                            this.handleStopClicked(app);
                                        }
                                        this.logout()
                                    },
                                    color: `error`,
                                }}
                            />
                            <Button
                                disableElevation
                                style={{ height: '36px', margin: '6px' }}
                                variant="contained"
                                color="secondary"
                                onClick={() => {
                                    const user: User = Global.user;
                                    if (user.appTracker.activeSessions.length != 0) {
                                        this.setState({ showLogoutWithSessionPopup: true });
                                    } else {
                                        this.logout()
                                    }
                                }}
                            >
                                Logout
                            </Button>
                        </div>
                        <IconButton
                            onClick={this.handleClose}
                            style={{
                                margin: '6px',
                                display: 'inline-block',
                                width: '36px',
                                height: '36px',
                                padding: '3px',
                            }}
                        >
                            <CloseIcon
                                style={{
                                    width: '30px',
                                    height: '30px',
                                    padding: '3px',
                                }}
                            />
                        </IconButton>
					</MuiDialogTitle>
                    <ShadowedDivider />
                    <div style={{display: 'flex', height: 'calc(100% - 60px - 2px'}}>
                        <div style={{width: '150px'}}>
                            <DialogContent style={{padding: '0px'}}>
                                <div style={{padding: '6px'}}>
                                    <Tabs
                                        value={this.state.selectedPanel}
                                        onChange={(event, newValue) => this.setState({selectedPanel: newValue})}
                                        orientation='vertical'
                                        variant='fullWidth'
                                        indicatorColor='primary'
                                        textColor='primary'
                                        style={{minHeight: '24px'}}
                                    >
                                        <Tab
                                            label='GENERAL'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.GENERAL}
                                        />
                                        <Tab
                                            label='LIMITS'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.LIMITS}
                                        />
                                        <Tab
                                            label='CONNECTORS'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.CONNECTORS}
                                        />
                                        <Tab
                                            label='PAYMENTS'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.PAYMENT}
                                        />
                                    </Tabs>
                                </div>
                            </DialogContent>
                        </div>
                        <ShadowedDivider orientation='vertical' />
                        <div style={{display: 'flex', flexFlow: 'column', overflow: 'hidden', width: 'calc(100% - 150px)', height: '100%'}}>
                            <DialogContent style={{
                                flexGrow: 1, 
                                overflowY: 'auto',
                                width: '100%',
                                height: '100%',
                                padding: '0px',
                                marginBottom: '0px', // This is because MuiDialogContentText-root is erroneously setting the bottom to 12
                                // lineHeight: 'var(--jp-code-line-height)',
                                fontSize: 'var(--jp-ui-font-size1)',
                                fontFamily: 'var(--jp-ui-font-family)',
                            }}>
                                <div style={{display: 'flex', flexFlow: 'column', overflow: 'hidden'}}>
                                    {this.state.selectedPanel == Page.GENERAL ? (
                                        <>
                                            <div style={{display: 'flex', padding: '6px 6px 0px 6px', maxWidth: '450px'}}>
                                                <div style={{width: '68px', margin: '0px 6px'}}>
                                                    <div style={{
                                                        width: '48px',
                                                        height: '48px',
                                                        margin: '6px auto',
                                                        borderRadius: '24px',
                                                        backgroundColor: '#10A0F9',
                                                        color: 'white',
                                                        fontSize: (28 - defaultProfilePicture.length * 4) + 'px',
                                                        fontWeight: 'bold',
                                                        lineHeight: '48px',
                                                        textAlign: 'center'
                                                    }}>
                                                        {defaultProfilePicture}
                                                    </div>
                                                </div>
                                                <div style={{display: 'table', height: '48px', margin: '6px'}}>
                                                    <div style={{display: 'table-cell', verticalAlign: 'middle'}}>
                                                        <span style={{fontSize: '16px', lineHeight: '1', fontWeight: 'normal'}}>
                                                            {Global.user.name}
                                                        </span>
                                                        <br />
                                                    </div>
                                                </div>
                                            </div>
                                            <AccountGeneralSubMenu style={{flexGrow: 1, overflowY: 'auto', maxWidth: '450px'}} />
                                        </>
                                    ) : this.state.selectedPanel == Page.LIMITS ? (
                                        <AccountLimitsSubMenu style={{flexGrow: 1, overflowY: 'auto', maxWidth: '450px'}} />
                                    ) : this.state.selectedPanel == Page.PAYMENT ? (
                                        <AccountPaymentSubMenu style={{flexGrow: 1, overflowY: 'auto', maxWidth: '450px'}} />
                                    ) : this.state.selectedPanel == Page.CONNECTORS && (
                                        <AccountConnectorsSubMenu style={{flexGrow: 1, overflowY: 'auto'}} />
                                    )}
                                </div>
                            </DialogContent>
                        </div>
                    </div>
                    <div style={{display: 'inline-flex'}}>
                        
                    </div>
				</StyledDialog>
            </div>
        )
    }

    // Log out of the REST interface
	private logout() {
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
		});		
	}

    public componentDidMount = () => {
        if (this.props.getOpenTo) this.props.getOpenTo(this.openTo);
    }

    public componentWillUnmount = () => {
        if (this.props.getOpenTo) this.props.getOpenTo(() => new Promise<void>(() => {}));
    }
}
