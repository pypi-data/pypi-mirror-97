/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Button, Dialog, DialogContent, IconButton, InputAdornment, Tab, Tabs, TextField, withStyles } from '@material-ui/core';
import * as React from 'react';
import { Global } from '../../Global';
import PopupIcon from '@material-ui/icons/MoreVert';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import CloseIcon from '@material-ui/icons/Close';
import { App } from '../../models/App';
import { ScrollableDiv } from './ScrollableDiv';
import { OutputFileList } from '../deploy/OutputFileList';
import CodeIcon from '@material-ui/icons/Code';
import { Status } from '../../models/Module';
import { MachineCapability } from '../../models/machine/MachineCapabilities';
import { ShadowedDivider } from '../../core';

import OpenInNewIcon from '@material-ui/icons/OpenInNew';
import Notebook from '../../core/notebook/Notebook';
import FileServerUtils from '../../utils/FileServerUtils';

const StyledDialog = withStyles({
    paper: {
        width: '80%',
        height: '80%',
        overflowY: 'visible',
        backgroundColor: 'var(--jp-layout-color1)',
        maxWidth: 'inherit',
    },
})(Dialog);

const enum Page {
    SUMMARY = 0,
    NOTEBOOK = 1,
    FILES = 2,
    MACHINE = 3,
    TERMINAL = 4,
}

interface IProps {
    style?: CSSProperties
    app: App
    onOpen?: () => void
	onClose?: () => void
    onMouseOver?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
    onMouseOut?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
}

interface IState {
    open: boolean,
	selectedPanel: number,
	inputLine: string
}

// TODO:Beck The popup needs to be abstracted out, there is too much going on to reproduce it in more than one file
export class DetailsDialog extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props);
		this.state = {
            open: false,
			selectedPanel: Page.SUMMARY,
			inputLine: ''
		};
    }
    
    private handleClickOpen = () => {
        if (this.props.onOpen) this.props.onOpen()
		this.setState({ open: true });
	}

	private handleClose = () => {
        this.setState({ open: false });
        if (this.props.onClose) this.props.onClose()
	}
	
	private handleInputLineChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({ inputLine: event.target.value });
    }

    private handleKeyDown = (event: React.KeyboardEvent) => {
        if (event.key == 'Enter') {
            this.setState({ inputLine: ''}), 
            this.props.app.modules[0].pushModuleInput(this.state.inputLine);
        }
    }
    
    private handleMouseOver = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        if (this.props.onMouseOver) this.props.onMouseOver(event);
    }

    private handleMouseOut = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        if (this.props.onMouseOut) this.props.onMouseOut(event);
    }

    private openSession = () => {
        window.open('http://localhost:' + this.props.app.sessionPort + '?token=' + this.props.app.sessionToken, '_blank');
    }

    private openAsNewNotebook = () => {
        // ex. "1-21-2021@1:46:48PM"
        const formattedTime = new Date().toLocaleString().replace(/\//g, '-').replace(/,/g, '').replace(/ /, '@').replace(/ /, '');
        const path = this.props.app.name.replace('.ipynb', '-' + formattedTime + '.ipynb');
        var notebook: any = this.props.app.notebook;
        // Remove the 'installing requirements' cell
        notebook['cells'].shift();
        FileServerUtils.saveNotebook(path, notebook).then((success: boolean) => { Global.docManager.open(path) });
        // Close the dialog
        this.setState({ open: false });
    }

    public render = (): JSX.Element => {
        var i = 0;
        if (Global.shouldLogOnRender) console.log('DetailsDialogRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <IconButton
                    onClick={this.handleClickOpen}
                    style={{
                        display: 'inline-block',
                        width: '36px',
                        height: '36px',
                        padding: '3px',
                    }}
                    onMouseOver={this.handleMouseOver}
                    onMouseOut={this.handleMouseOut}
                >
                    <PopupIcon
                        style={{
                            width: '30px',
                            height: '30px',
                            padding: '3px',
                        }}
                    />
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
            					{this.props.app.interactive ? "Session" : "Job"}
                            </div>
                        </div>
						<div style={{width: '100%', display: 'inline-flex', overflowX: 'hidden', fontSize: '16px', paddingLeft: '8px'}}>
	                        <div style={{flexGrow: 1, margin: 'auto 0px'}}>
                                {this.props.app.name}
                            </div>
                            {this.props.app.interactive && (
                                <Button
                                    style={{margin: '6px'}}
                                    disableElevation
                                    variant='contained'
                                    color='primary'
                                    onClick={this.openSession}
                                    disabled={this.props.app.getAppStatus() == Status.Completed || !(this.props.app.modules.length > 0 && this.props.app.modules[0].sessionReady)}
                                    endIcon={<OpenInNewIcon />}
                                >
                                    Open session
                                </Button>
                            )}
                            {!this.props.app.interactive && (
                                <Button
                                    style={{margin: '6px'}}
                                    disableElevation
                                    variant='contained'
                                    color='primary'
                                    onClick={this.openAsNewNotebook}
                                    disabled={this.props.app.getAppStatus() != Status.Completed}
                                    endIcon={<OpenInNewIcon />}
                                >
                                    Open as a new notebook
                                </Button>
                            )}
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
                                            label='SUMMARY'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.SUMMARY}
                                        />
                                        {!this.props.app.interactive && <Tab
                                            label='NOTEBOOK'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.NOTEBOOK}
                                        />}
                                        <Tab
                                            label='FILES'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.FILES}
                                        />
                                        <Tab
                                            label='MACHINE'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.MACHINE}
                                        />
                                        {this.props.app.modules.length > 0 && this.props.app.interactive && <Tab
                                            label='TERMINAL'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                            value={Page.TERMINAL}
                                        />}
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
                                // fontSize: 'var(--jp-code-font-size)',
                                // fontFamily: 'var(--jp-code-font-family)',
                            }}>
                                {this.state.selectedPanel == Page.SUMMARY ? (
                                    <div style={{padding: '12px'}}>
                                        {this.props.app.interactive ? 'Session' : 'Job'} launched at {this.props.app.timestamp.toLocaleTimeString('en-US', { 
                                            hour: 'numeric', minute: 'numeric',
                                        })} on {this.props.app.timestamp.toLocaleDateString('en-US', { 
                                            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' 
                                        })}
                                        <br/>
                                        {this.props.app.getTimeElapsed() ? (
                                            <>
                                                Duration: {this.props.app.getTimeElapsed()}<br/>
                                            </>
                                        ) : (
                                            <></>
                                        )}
                                        {this.props.app.getCost() ? (
                                            <>
                                                Estimated cost: {this.props.app.getCost()}<br/>
                                            </>
                                        ) : (
                                            <></>
                                        )}
                                        <br/>
                                        {/* The must have unique key error apparently applies to fragments as well, despite not being able to hold keys */}
                                        {this.props.app.initializing.messages.map((value: string) => (<span key={value + i++}>{value}<br /></span>))}
                                        {this.props.app.uploading.messages.map((value: string) => (<span key={value + i++}>{value}<br /></span>))}
                                        {this.props.app.requisitioning.messages.map((value: string) => (<span key={value + i++}>{value}<br /></span>))}
                                        {this.props.app.running.messages.map((value: string) => (<span key={value + i++}>{value}<br /></span>))}
                                    </div>
                                ) : this.state.selectedPanel == Page.NOTEBOOK ? (
                                    <div style={{overflow: 'hidden', width: '100%', height: '100%'}}>
                                        <div style={{width: '100%', height: 'calc(100% - 68px)', overflow: 'auto'}}>
                                            <Notebook notebook={this.props.app.notebook} />
                                        </div>
                                        <div style={{padding: '6px', width: '100%'}}>
                                                <TextField
                                                    variant='outlined' 
                                                    disabled={this.props.app.modules.length > 0 && this.props.app.modules[0].modStatus == Status.Completed}
                                                    value={this.state.inputLine} 
                                                    onChange={this.handleInputLineChange} 
                                                    onKeyDown={this.handleKeyDown}
                                                    style={{height: '56px', width: '100%'}}
                                                    InputProps={{startAdornment: 
                                                        (<InputAdornment position="start">
                                                            <CodeIcon />
                                                        </InputAdornment>)
                                                    }}
                                                />
                                            </div>
                                    </div>
                                ) : this.state.selectedPanel == Page.FILES ? (
                                    <div>
                                        {this.props.app.interactive && this.props.app.getAppStatus() != Status.Completed ? (
                                            <div style={{padding: '12px'}}>
                                                Files will appear here after your session has completed. Until then, you can upload/download files directly from the session tab.
                                            </div>
                                        ) : (
                                            <OutputFileList app={this.props.app} />
                                        )}
                                    </div>
                                ) : this.state.selectedPanel == Page.MACHINE ? (
                                   
                                    <div>
                                         {this.props.app.machine ? (
									        <MachineCapability machine={this.props.app.machine} />
                                        ) : (
                                            <div style={{padding: '12px'}}>
                                                Machine information will appear when the {this.props.app.interactive ? ' session ' : ' job '} starts.
                                            </div>
                                        )}
                                    </div>
                                    
								) : this.state.selectedPanel == Page.TERMINAL && (
                                    <div style={{overflow: 'hidden', width: '100%', height: '100%'}}>
                                        <ScrollableDiv
                                            key='output'
                                            source={Object.assign([], this.props.app.modules[0].output)}
                                            autoScroll={true}
                                        />
                                    </div>
								)}
                            </DialogContent>
                        </div>
                    </div>
				</StyledDialog>
            </>
        )
    }
}
