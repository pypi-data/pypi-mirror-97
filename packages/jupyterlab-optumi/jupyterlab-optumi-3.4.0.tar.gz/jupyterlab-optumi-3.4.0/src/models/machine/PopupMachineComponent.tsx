/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Dialog, DialogContent, IconButton, Tab, Tabs, withStyles } from '@material-ui/core';
import * as React from 'react';
import { Global } from '../../Global';
import { Machine, NoMachine } from './Machine';
import PopupIcon from '@material-ui/icons/MoreVert';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { ShadowedDivider } from '../../core';
import CloseIcon from '@material-ui/icons/Close';
import { MachineCapability } from './MachineCapabilities';
import FormatUtils from '../../utils/FormatUtils';

const StyledDialog = withStyles({
    paper: {
        width: 'calc(min(80%, 600px + 150px + 2px))',
        height: '80%',
        overflowY: 'visible',
        backgroundColor: 'var(--jp-layout-color1)',
        maxWidth: 'inherit',
    },
})(Dialog);

const enum Page {
    CAPABILITY = 0,
    STATUS = 1,
    COST = 2,
}

interface IProps {
    style?: CSSProperties
    machine: Machine
    onOpen?: () => void
	onClose?: () => void
    onMouseOver?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
    onMouseOut?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
}

interface IState {
    open: boolean,
    selectedPanel: number
}

// TODO:Beck The popup needs to be abstracted out, there is too much going on to reproduce it in more than one file
export class PopupMachineComponent extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props);
		this.state = {
            open: false,
            selectedPanel: Page.CAPABILITY,
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

    private handleMouseOver = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        if (this.props.onMouseOver) this.props.onMouseOver(event);
    }

    private handleMouseOut = (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        if (this.props.onMouseOut) this.props.onMouseOut(event);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('PopupMachineRender (' + new Date().getSeconds() + ')');
        const machine = this.props.machine
        return (
            <>
                <IconButton
                    disabled={machine instanceof NoMachine}
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
                            <div style={{margin: 'auto'}}>
            					Machine
                            </div>
                        </div>
                        <div style={{
							width: '100%',
							display: 'inline-flex',
                            fontSize: '16px',
                            fontWeight: 'bold',
							padding: '10px',
						}}>
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
                                            label='CAPABILITY'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                        />
                                        <Tab
                                            label='STATUS'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                        />
                                        <Tab
                                            label='COST'
                                            style={{
                                                padding: '0px',
                                                minWidth: 'auto',
                                                minHeight: '36px',
                                            }}
                                        />
                                    </Tabs>
                                </div>
                            </DialogContent>
                        </div>
                        <ShadowedDivider orientation='vertical' />
                        <div style={{display: 'flex', flexFlow: 'column', overflow: 'hidden', width: 'calc(100% - 150px)', height: '100%'}}>
                            <DialogContent style={{ padding: '0px', flexGrow: 1, overflowY: 'auto' }}>
                                {this.state.selectedPanel == Page.CAPABILITY ? (
                                    <MachineCapability machine={machine}/>
                                ) : this.state.selectedPanel == Page.STATUS ? (
                                    <div style={{ margin: '6px' }}>
                                        {Machine.getStateMessage(this.props.machine.state) == '' ? 'Machine currently has no status' : 'Machine is currently ' + Machine.getStateMessage(this.props.machine.state).toLowerCase()}
                                    </div>
                                ) : this.state.selectedPanel == Page.COST && (
                                    <div style={{ margin: '6px' }}>
                                        Machine costs {FormatUtils.styleRateUnitValue()(machine.rate) + (machine.promo ? ' (promotional price)' : '')}
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