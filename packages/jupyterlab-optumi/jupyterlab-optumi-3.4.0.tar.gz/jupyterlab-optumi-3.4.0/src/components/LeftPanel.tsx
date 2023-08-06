/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';

import { User } from '../models/User';
import { Login } from './Login';
import { Pilot } from './Pilot';

import { ServerConnection } from '@jupyterlab/services';
import { IThemeManager } from '@jupyterlab/apputils';

import CssBaseline from '@material-ui/core/CssBaseline';
import {
	ThemeProvider,
	createMuiTheme,
	Theme,
    withStyles,
    StyledComponentProps, 
} from '@material-ui/core/styles';
import { Agreement } from './Agreement';
import { SnackbarProvider } from 'notistack';
import { providerOptions } from '../models/Snackbar';
import { Box } from '@material-ui/core';

const GlobalThemeDiv = withStyles({
	'@global': {
		':root': {
			'--ot-font-family': 'var(--jp-ui-font-family)',
			'--ot-padding': '12px',
			'--ot-padding-half': '6px',
			'--ot-margin': '12px',
			'--ot-margin-half': '6px',
			'--ot-backgroundColor': 'var(--jp-layout-color1)',
			'--ot-backgroundColor-emphasized': 'var(--jp-layout-color2)',
        },
		'button:focus': {
			outline: 'none !important',
		},
		'code': {
			color: 'var(--jp-ui-font-color0) !important',
		},
	}
})(Box)

// Properties from parent
interface IProps extends StyledComponentProps {}

// Properties for this component
interface IState {
	loggedIn: boolean
}

class OptumiLeftPanel extends React.Component<IProps, IState> {    
    // We need to know if the component is mounted to change state
	_isMounted = false;
    private domRoot: HTMLElement;

    constructor(props: IProps) {
        super(props);
        this.state = {
            loggedIn: false
        }
        this.domRoot = document.getElementById("main");
    }

	// The contents of the component
	render() {
        if (Global.shouldLogOnRender) console.log('LeftPanelRender (' + new Date().getSeconds() + ')');
		return (
			<GlobalThemeDiv component='div' style={{
				height: '100%',
				display: 'flex',
				flexFlow: 'column',
				overflow: 'hidden',
				color: 'var(--jp-ui-font-color1)',
				backgroundColor: 'var(--jp-layout-color1)',
				fontSize: 'var(--jp-ui-font-size1)',
				fontFamily: 'var(--jp-ui-font-family)'
			}}>
				<CssBaseline />
				<ThemeProvider theme={this.theme}>
                    <SnackbarProvider 
                    maxSnack={3} 
                    domRoot={this.domRoot} 
                    classes={{
                        variantSuccess: this.props.classes.success,
                        variantError: this.props.classes.error,
                        variantWarning: this.props.classes.warning,
                        variantInfo: this.props.classes.info,
                    }}
                >
                    {this.state.loggedIn && Global.version ? 
                        (Global.user.unsignedAgreement ? (
                            <Agreement callback={() => this.forceUpdate()}/>
                        ) : (
                            <Pilot />
                        )
                    ) : (
                        <Login />
                    )}
                    </SnackbarProvider>
				</ThemeProvider>
			</GlobalThemeDiv>
		);
	}

	private getTheme = () => {
		var themeManager: IThemeManager = Global.themeManager;
		return createMuiTheme({
			props: {
				MuiOutlinedInput: { inputProps: { spellCheck: 'false' }}
			},
			overrides: {
				MuiButton: { root: { textTransform: 'none', fontWeight: 'bold' }},
				MuiDialog: { paperWidthSm: { maxWidth: '650px' } }
			},
			palette: {
				type: themeManager.theme == null || themeManager.isLight(themeManager.theme) ? 'light' : 'dark',
				primary: {
					// light: will be calculated from palette.primary.main,
					main: '#10A0F9',
					// dark: will be calculated from palette.primary.main,
					// contrastText: will be calculated to contrast with palette.primary.main
				},
				secondary: {
					// light: will be calculated from palette.secondary.main,
					main: '#afaab0',
					// dark: will be calculated from palette.secondary.main,
					// contrastText: will be calculated to contrast with palette.secondary.main
				},
				error: {
					// light: will be calculated from palette.error.main,
					main: '#f48f8d',
					// dark: will be calculated from palette.error.main,
				 	// contrastText: will be calculated to contrast with palette.error.main
				 },
				 // warning: {

				 // },
				 // info: {

				 // },
				 success: {
					 // light: will be calculated from palette.error.main,
					 main: '#68da7c',
					 // dark: will be calculated from palette.error.main,
					 // contrastText: will be calculated to contrast with palette.error.main
				 },
				 // Used by `getContrastText()` to maximize the contrast between
				 // the background and the text.
				 contrastThreshold: 2.2,
				 // Used by the functions below to shift a color's luminance by approximately
				 // two indexes within its tonal palette.
				 // E.g., shift from Red 500 to Red 300 or Red 700.
				 tonalOffset: 0.2,
		 	},
		});
	}
	theme: Theme = this.getTheme();

	private handleVersionSet = () => this.forceUpdate()
	private handleUserChange = () => this.setState({loggedIn: Global.user != null})
	private handleNullUserChange = () => this.setState({loggedIn: false})

	//TODO:JJ should this be async?
	private handleThemeChange = async () => {
		this.theme = this.getTheme();
		this.forceUpdate();
	}

	// Will be called automatically when the component is mounted
	componentDidMount = () => {
		this._isMounted = true;
		Global.onVersionSet.connect(this.handleVersionSet);
		Global.onNullUser.connect(this.handleNullUserChange);
		Global.onUserChange.connect(this.handleUserChange);
        Global.themeManager.themeChanged.connect(this.handleThemeChange);
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/login";
		const init = {
			method: 'GET',
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			if (response.status !== 200 && response.status !== 201) {
				// We still want to get the domain
				response.json().then((body: any) => { Global.domain = body.domain });
				throw new ServerConnection.ResponseError(response);
			}
			return response.json();
		}).then((body: any) => {
			Global.domain = body.domain;
			if (body.loginFailed || body.domainFailed) {
				// No login
			} else {
				var user = User.handleLogin(body);
				Global.user = user;
			}
		});
	}

	// Will be called automatically when the component is unmounted
	componentWillUnmount = () => {
		Global.onVersionSet.disconnect(this.handleVersionSet);
		Global.onNullUser.disconnect(this.handleNullUserChange);
		Global.onUserChange.disconnect(this.handleUserChange);
		Global.themeManager.themeChanged.disconnect(this.handleThemeChange);
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

const StyledOptumiLeftPanel = withStyles(providerOptions)(OptumiLeftPanel);
export { StyledOptumiLeftPanel as OptumiLeftPanel };
