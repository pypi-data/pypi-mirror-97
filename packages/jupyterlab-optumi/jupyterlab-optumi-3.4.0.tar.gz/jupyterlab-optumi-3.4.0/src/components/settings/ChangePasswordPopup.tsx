/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import {
	Dialog,
	DialogContent,
    Button,
    IconButton,
    Divider,
    DialogActions
} from '@material-ui/core';
import CloseIcon from '@material-ui/icons/Close';
import MuiDialogTitle from '@material-ui/core/DialogTitle';

import { withStyles } from '@material-ui/core/styles';
import { TextBox, ShadowedDivider } from '../../core';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import ExtraInfo from '../../utils/ExtraInfo';

const StyledDialog = withStyles({
    paper: {
        width: '300px',
        backgroundColor: 'var(--jp-layout-color1)',
        // minHeight: ((300 * 9 / 16) + 60) + 'px',
    },
})(Dialog);

interface IProps {
    style?: CSSProperties
    onOpen?: () => {}
	onClose?: () => {}
}

// Properties for this component
interface IState {
    open: boolean,
    loginName: string,
    oldPassword: string,
    newPassword: string,
    errorMessage: string,
}

export class ChangePasswordPopup extends React.Component<IProps, IState> {

	constructor(props: IProps) {
        super(props);
		this.state = {
            open: false,
            loginName: '',
            oldPassword: '',
            newPassword: '',
            errorMessage: '',
		};
	}

	private handleClickOpen = () => {
        if (this.props.onOpen !== undefined) this.props.onOpen()
		this.setState({ open: true });
	}

	private handleClose = () => {
        this.setState({ open: false, loginName: '', oldPassword: '', newPassword: '', errorMessage: '' });
        if (this.props.onClose !== undefined) this.props.onClose()
    }
    
    private changePassword = () => {
        if (this.state.newPassword.length < 8) {
            this.setState({errorMessage: 'Password bust be at least 8 characters'});
        } else {
            Global.user.changePassword(this.state.loginName, this.state.oldPassword, this.state.newPassword).then(() => {
                this.handleClose()
            }, (reason: any) => {
                this.setState({errorMessage:
`Failed to change password...
Try checking your username/password`});
            })
        } 
    }

	render() {
		if (Global.shouldLogOnRender) console.log('ChangePasswordPopupRender (' + new Date().getSeconds() + ')');
		return (
            <>
				<Button
                    onClick={this.handleClickOpen}
                    style={Object.assign({
                        minWidth: '0px',
                    }, this.props.style)}
                    variant="contained"
                    color="secondary"
                    disableElevation 
                >
                    Edit
                </Button>
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
                            padding: '6px'
                        }}
                    >
                        <div style={{
                            display: 'inline-flex',
                            width: '100%',
                            padding: '6px',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            lineHeight: '24px',
                            margin: '6px',
                        }}>
    						Change Password
                        </div>
                        <IconButton
                            onClick={this.handleClose}
                            style={{
                                display: 'inline-block',
                                width: '36px',
                                height: '36px',
                                padding: '3px',
                                margin: '6px',
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
					<DialogContent style={{padding: '0px'}}>
                        <div style={{padding: '6px'}}>
                            <TextBox<string>
                                label='Username'
                                getValue={() => ''}
                                saveValue={(loginName: string) => {
                                    this.setState({loginName: loginName, errorMessage: ''})
                                }}
                                placeholder='Username'
                            />
                            <TextBox<string>
                                label='Old'
                                getValue={() => ''}
                                saveValue={(oldPassword: string) => {
                                    this.setState({oldPassword: oldPassword, errorMessage: ''})
                                }}
                                placeholder='Old Password'
                                password
                            />
                            <TextBox<string>
                                label='New'
                                getValue={() => ''}
                                saveValue={(newPassword: string) => {
                                    this.setState({newPassword: newPassword, errorMessage: ''})
                                }}
                                placeholder='New Password'
                                password
                            />
                            {this.state.errorMessage != '' && (
                                <div style={{
                                    color: '#f48f8d',
                                    margin: '0px 12px',
                                }}>
                                    {this.state.errorMessage}
                                </div>
                            )}
                        </div>
					</DialogContent>
                    <Divider variant='middle' />
                    <DialogActions style={{padding: '6px'}}>
                        {/* <Button
                            onClick={this.handleClose}
                            style={{
                                padding: '6px',
                                fontWeight: 'bold',
                                fontSize: '14px',
                                lineHeight: '14px',
                                margin: '0px'
                            }}
                        >
                            Cancel
                        </Button> */}
                        <ExtraInfo reminder={this.state.errorMessage}>
                            <Button
                                onClick={this.changePassword}
                                color='primary'
                                style={{
                                    padding: '6px',
                                    fontWeight: 'bold',
                                    fontSize: '14px',
                                    lineHeight: '14px',
                                    margin: '0px',
                                    color: this.state.errorMessage ? '#f48f8d' : '',
                                }}
                            >
                                Confirm
                            </Button>
                        </ExtraInfo>
                    </DialogActions>
				</StyledDialog>
            </>
		);
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
