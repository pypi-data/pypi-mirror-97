/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Button, Dialog, IconButton, withStyles } from '@material-ui/core';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { Close } from '@material-ui/icons';
import * as React from 'react'
import { Global } from '../../Global';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import { ShadowedDivider } from '../../core';
import FileBrowser, { FileMetadata } from './fileBrowser/FileBrowser';

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

const StyledButton = withStyles({
   root: {
       height: '20px',
       padding: '0px',
       fontSize: '12px',
       lineHeight: '12px',
       minWidth: '0px',
       margin: '0px 6px 6px 6px',
       width: '100%',
   },
   label: {
       height: '20px',
   },
})(Button);

interface IProps {
    style?: CSSProperties
    onOpen?: () => void
    onClose?: () => void
    onFilesAdded: (paths: FileMetadata[]) => void
}

interface IState {
    open: boolean,
}

// TODO:Beck The popup needs to be abstracted out, there is too much going on to reproduce it in more than one file
export class AddFilesPopup extends React.Component<IProps, IState> {

    private getSelectedFiles: () => FileMetadata[] = () => []

    constructor(props: IProps) {
        super(props);
		this.state = {
            open: false,
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
    
    private handleAdd = () => {
        this.props.onFilesAdded(this.getSelectedFiles())
        // console.log(this.getSelectedFiles())
        this.handleClose()
    }

    private handleKeyDown = (event: KeyboardEvent) => {
        // The enter has to be a timeout because without it the file gets added but the popup doesn't close
        if (event.key === 'Enter') setTimeout(() => this.handleAdd(), 0);
        if (event.key === 'Escape') this.handleClose();
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('AddFilesPopupRender (' + new Date().getSeconds() + ')');
        return (
            <div style={Object.assign({display: 'inline-flex', width: '50%'}, this.props.style)} >
                <StyledButton
                    onClick={this.handleClickOpen}
                    variant='contained'
                    disableElevation
                    color='primary'
                >
                    + Upload
                </StyledButton>
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
                            minWidth: '225px',
                            fontSize: '16px',
                            fontWeight: 'bold',
                            paddingRight: '12px', // this is 6px counteracting the MuiDialogTitle padding and 6px aligning the padding to the right of the tabs
                        }}>
                            <div style={{margin: 'auto', paddingLeft: '12px'}}>
            					Select Files or Directories
                            </div>
                        </div>
                        <div style={{flexGrow: 1}} />
                        <div>
                            <Button
                                disableElevation
                                style={{ height: '36px', margin: '6px' }}
                                variant='contained'
                                color='primary'
                                onClick={this.handleAdd}
                            >
                                Add
                            </Button>
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
                            <Close
                                style={{
                                    width: '30px',
                                    height: '30px',
                                    padding: '3px',
                                }}
                            />
                        </IconButton>
					</MuiDialogTitle>
                    <ShadowedDivider />
                    <FileBrowser style={{maxHeight: 'calc(100% - 60px - 2px)'}} onAdd={this.handleAdd} getSelectedFiles={(getSelectedFiles: () => FileMetadata[]) => this.getSelectedFiles = getSelectedFiles} />
				</StyledDialog>
            </div>
        )
    }

    public componentDidMount = () => {
        document.addEventListener('keydown', this.handleKeyDown, false)
    }

    public componentWillUnmount = () => {
        document.removeEventListener('keydown', this.handleKeyDown, false)
    }
}
