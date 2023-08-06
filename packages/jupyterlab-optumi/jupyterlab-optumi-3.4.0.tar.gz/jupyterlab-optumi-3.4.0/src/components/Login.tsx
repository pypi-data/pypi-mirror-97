///<reference path="../../node_modules/@types/node/index.d.ts"/>

/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';

import { User } from '../models/User';

import {
	Container,
	Button,
	TextField,
	Link,
	Typography,
	CircularProgress,
	withStyles,
	Dialog,
	DialogActions,
	DialogContent,
	DialogTitle,
 } from '@material-ui/core';

import { ServerConnection } from '@jupyterlab/services';
import { Header, ShadowedDivider } from '../core';

// Element to display the Copyright with optumi.com link
function Copyright() {
	return (
		<Typography style={{marginBottom: '10px'}} variant="body2" color="textSecondary" align="center">
			{'Copyright © '}
			<Link color="inherit" href="https://optumi.com/">
				Optumi Inc
			</Link>
		</Typography>
	);
}

const StyledDialog = withStyles({
    root: {
        margin: '12px',
        padding: '0px',
    },
    paper: {
        backgroundColor: 'var(--jp-layout-color1)',
    },
})(Dialog)

// Properties from parent
interface IProps {}

// Properties for this component
interface IState {
	domain: string;
	loginName: string;
	password: string;
	loginFailed: boolean;
	domainFailed: boolean;
	loginFailedMessage: string;
	waiting: boolean;
	spinning: boolean;
	packageString: string;
	downgrade: boolean;
}

// The login screen
export class Login extends React.Component<IProps, IState> {
	_isMounted = false;

	constructor(props: IProps) {
		super(props);
		this.state = {
			domain: Global.domain,
			loginName: "",
			password: "",
			loginFailed: false,
            domainFailed: false,
            loginFailedMessage: "",
			waiting: false,
			spinning: false,
			packageString: "",
			downgrade: false,
		}
	}

	private handleDomainChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        if (new RegExp('^[A-Za-z0-9.:]*$').test(value)) {
            this.checkAndSetState({domain: value, loginFailed: false, domainFailed: false});
        }
	}

	private handleLoginNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		this.checkAndSetState({loginName: e.target.value, loginFailed: false, domainFailed: false});
	}

	private handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		this.checkAndSetState({password: e.target.value, loginFailed: false, domainFailed: false});
	}

	private handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
		if (e.key === 'Enter') {
			this.login();
		}
	}

	// The contents of the component
	render() {
		if (Global.shouldLogOnRender) console.log('LoginRender (' + new Date().getSeconds() + ')');
		return (
            <>
                <div className='jp-optumi-logo'/>
                <Container style={{textAlign: 'center'}} maxWidth="xs">
                    <Typography component="h1" variant="h5">
                        Sign in
                    </Typography>
                    <form>
                        <TextField
                            fullWidth
                            required
                            style={{marginTop: "16px", marginBottom: "8px"}}
                            label="Domain"
                            variant="outlined"
                            value={this.state.domain}
                            onChange = {this.handleDomainChange}
                            onKeyDown = { this.handleKeyDown }
                            error={ this.state.domainFailed }
                            helperText={ this.state.domainFailed? "Unable to contact " + this.state.domain : ""}
                        />
                        <TextField
                            id='username'
                            name='username'
                            fullWidth
                            required
                            style={{marginTop: "16px", marginBottom: "8px"}}
                            label="Username"
                            variant="outlined"
                            value={this.state.loginName}
                            onChange = {this.handleLoginNameChange}
                            onKeyDown = { this.handleKeyDown }
                            error={ this.state.loginFailed }
                            autoComplete='username'
                        />
                        <TextField
                            id='password'
                            name='password'
                            fullWidth
                            required
                            style={{marginTop: "16px", marginBottom: "8px"}}
                            type="password"
                            label="Password"
                            variant="outlined"
                            value={this.state.password}
                            onChange = {this.handlePasswordChange}
                            onKeyDown = { this.handleKeyDown }
                            error={ this.state.loginFailed }
                            helperText={ this.state.loginFailed ? this.state.loginFailedMessage : "" }
                            autoComplete='current-password'
                        />
                        <Button
                            fullWidth
                            style={{marginTop: "16px", marginBottom: "8px"}}
                            variant="contained"
                            color="primary"
                            disabled={this.state.waiting}
                            onClick={ () => this.login() }
                        >
                            {this.state.waiting && this.state.spinning ? <CircularProgress size='1.75em'/> : 'Sign in'}
                        </Button>
                    </form>
                    <div style={{marginTop: "30px"}} />
                    <Copyright />
                    {/* <div dangerouslySetInnerHTML={{__html: this.fbWidget.node.innerHTML}} /> */}
                </Container>
			<StyledDialog
                disableBackdropClick
                disableEscapeKeyDown
                open={this.state.packageString != ""}
            >
				<DialogTitle
					disableTypography
					style={{
						backgroundColor: 'var(--jp-layout-color2)',
						height: '48px',
						padding: '6px 30px',
					}}
				>
					<Header
						title={this.state.downgrade ? "Switch to compatible JupyterLab extension" : "Upgrade JupyterLab extension"}
						style={{lineHeight: '24px'}}
					/>
				</DialogTitle>
                <ShadowedDivider />
                <div style={{padding: '18px'}}>
					<DialogContent style={{padding: '6px 18px', lineHeight: '24px'}}>
						<div>
							{this.state.downgrade ? 
								"Sorry, we've noticed an incompatibility between this JupyterLab extension version and our backend. To switch to a compatible JupyterLab extension run the command"
							:
								"We've made enhancements on the backend that require a new JupyterLab extension version. To upgrade your JupyterLab extension run the command"
							}
						</div>
						<textarea
							id="optumi-upgrade-string"
							style={{
								fontFamily: 'var(--jp-code-font-family)',
								width: '100%',
								lineHeight: '18px',
								marginTop: '6px',
							}}
							rows={1}
							readOnly
						>
							{'pip install ' + this.state.packageString}
						</textarea>
						<div>
							{'and restart JupyterLab.'}
						</div>
					</DialogContent>
                    <DialogActions style={{padding: '12px 6px 6px 6px'}}>
						<Button
							variant='contained'
							onClick={() => {
								var copyTextarea: HTMLTextAreaElement = document.getElementById('optumi-upgrade-string') as HTMLTextAreaElement;
								copyTextarea.focus();
								copyTextarea.select();

								try {
									document.execCommand('copy');
								} catch (err) {
									console.log(err);
								}
							}}
							color={'primary'}
						>
							Copy command
						</Button>
						<Button
							variant='contained'
							onClick={() => {
								this.checkAndSetState({loginFailed: false, domainFailed: false, packageString: "", downgrade: false, loginFailedMessage: ""});
							}}
							color={'secondary'}
						>
							Close
						</Button>
                    </DialogActions>
                </div>
           </StyledDialog>
            </>
		);
	}

	// Try to log into the REST interface and update state according to response
	private async login() {
		this.checkAndSetState({ waiting: true, spinning: false });
		setTimeout(() => this.checkAndSetState({ spinning: true }), 1000);
		Global.domain = this.state.domain;
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/login";
		const init = {
			method: 'POST',
			body: JSON.stringify({
				'domain': this.state.domain,
				'loginName': this.state.loginName,
				'password': this.state.password,
			})
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			this.checkAndSetState({ waiting: false })
			if (response.status !== 200 && response.status !== 201) {
                this.checkAndSetState({ loginFailed: false, domainFailed: true });
				throw new ServerConnection.ResponseError(response);
			}
			return response.json();
		}, () => this.checkAndSetState({ waiting: false })).then((body: any) => {
			if (body.loginFailed || body.domainFailed) {
				if (body.message == 'Version exchange failed') {
					var rawVersion = body.loginFailedMessage;
					var split = rawVersion.split('-')[0].split('.');
					const downgrade = Global.version.split('.')[1] > split[1];
					var packageString = '"jupyterlab-optumi>=' + split[0] + '.' + split[1] + '.0,' + '<' + split[0] + '.' + (+split[1] + 1) + '.0"'
					this.checkAndSetState({ loginFailed: body.loginFailed || false, domainFailed: body.domainFailed || false, packageString: packageString, downgrade: downgrade});
				} else {
					this.checkAndSetState({ loginFailed: body.loginFailed || false, domainFailed: body.domainFailed || false, loginFailedMessage: body.loginFailedMessage || ""});
				}
			} else {
				var user = User.handleLogin(body);
				Global.user = user;
				this.checkAndSetState({ loginFailed: false, domainFailed: false });
			}
		});
	}

	private checkAndSetState = (map: any) => {
		if (this._isMounted) {
			this.setState(map);
		}
	}

	handleGlobalDomainChange = () => this.checkAndSetState({ domain: Global.domain });

	// Will be called automatically when the component is mounted
	componentDidMount = () => {
		this._isMounted = true;
		Global.onDomainChange.connect(this.handleGlobalDomainChange);
	}

	// Will be called automatically when the component is unmounted
	componentWillUnmount = () => {
		Global.onDomainChange.disconnect(this.handleGlobalDomainChange);
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
