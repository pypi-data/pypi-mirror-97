/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Button, CircularProgress, Dialog, DialogContent, /*IconButton,*/ withStyles } from '@material-ui/core';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { ArrowBackIos } from '@material-ui/icons';
import * as React from 'react'
import { Global } from '../../Global';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import { ShadowedDivider, TextBox } from '../../core';

import { ServerConnection } from '@jupyterlab/services';
import { CreateDataConnector } from './CreateDataConnector';
import { DataService } from './dataConnectorBrowser/DataConnectorDirListingItemIcon';
import { DataConnectorUploadMetadata } from '../../models/DataConnectorUploadMetadata';
import { OptumiMetadataTracker } from '../../models/OptumiMetadataTracker';
import { UploadMetadata } from '../../models/UploadMetadata';
import { NotebookPanel } from '@jupyterlab/notebook';

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
    startIcon: {
        marginRight: '0px',
    },
    iconSizeMedium: {
        '& > *:first-child': {
            fontSize: '12px',
        },
    }
 })(Button);

interface IProps {
    // This close action will allow us to get a new set of connectors when a new one is created
    handleClose?: () => any
    style?: CSSProperties
}

interface IState {
    open: boolean
    name: string
    bucketName: string
    objectKey: string
    accessKeyID: string
    accessSecretKey: string
    waiting: boolean
    addSpinning: boolean
    createSpinning: boolean
    errorMessage: string
}

const LABEL_WIDTH = '136px'

export class AmazonS3ConnectorPopup extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props);
		this.state = {
            open: false,
            name: '',
            bucketName: '',
            objectKey: '',
            accessKeyID: '',
            accessSecretKey: '',
            waiting: false,
            addSpinning: false,
            createSpinning: false,
            errorMessage: '',
		};
    }
    
    private handleClickOpen = () => {
		this.setState({ open: true });
	}

	private handleClose = () => {
        if (!this.state.waiting) {
            if (this.props.handleClose) this.props.handleClose();
            this.setState({
                open: false,
                name: '',
                bucketName: '',
                objectKey: '',
                accessKeyID: '',
                accessSecretKey: '',
                waiting: false,
                addSpinning: false,
                createSpinning: false,
                errorMessage: '',
            });
        }
    }

    private nameHasError = (name: string): boolean => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const upload: UploadMetadata = optumi.metadata.upload;
        const dataConnectors = upload.dataConnectors;
        for (var i = 0; i < dataConnectors.length; i++) {
            if (dataConnectors[i].name === name) return true;
        }
        return false;
    }

    private handleCreate = (add?: boolean) => {
        this.setState({ waiting: true, addSpinning: false, createSpinning: false })
        if (add) {
            setTimeout(() => this.setState({ addSpinning: true }), 1000)
        } else {
            setTimeout(() => this.setState({ createSpinning: true }), 1000)
        }
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/add-data-connector";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
                // TODO:JJ Change this once we support multiple data connector types
                dataService: DataService.AMAZON_S3,
                name: this.state.name,
                info: JSON.stringify({
                    bucketName: this.state.bucketName,
                    objectKey: this.state.objectKey,
                    accessKeyID: this.state.accessKeyID,
                    accessSecretKey: this.state.accessSecretKey,
                }),
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
		}).then(() => {
            this.setState({ waiting: false, addSpinning: false, createSpinning: false})
            if (add && !this.nameHasError(this.state.name)) {
                const tracker = Global.metadata
                const optumi = tracker.getMetadata()
                var dataConnectors = optumi.metadata.upload.dataConnectors
                dataConnectors.push(new DataConnectorUploadMetadata({
                    name: this.state.name,
                    dataService: DataService.AMAZON_S3,
                }))
                tracker.setMetadata(optumi)
            }
            // Success
            this.handleClose()
		}, (error: ServerConnection.ResponseError) => {
            error.response.text().then((text: string) => {
                // Show what went wrong
                this.setState({ waiting: false, addSpinning: false, createSpinning: false, errorMessage: text });
            });
        });
    }

    private handleKeyDown = (event: KeyboardEvent) => {
        if (!this.state.open) return;
        if (event.key === 'Enter') this.handleCreate();
        if (event.key === 'Escape') this.handleClose();
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('AmazonS3ConnectorPopupRender (' + new Date().getSeconds() + ')');
        return (
            <div style={Object.assign({}, this.props.style)} >
                <CreateDataConnector
                    iconClass='jp-s3-logo'
                    dataService={DataService.AMAZON_S3}
                    description='Access an S3 bucket'
                    handleClick={this.handleClickOpen}
                />
                <StyledDialog
                    disableBackdropClick
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
                            flexGrow: 1,
                            marginLeft: '-6px', // this is to counteract the padding in CreateDataConnector so we can reuse it without messing with it
                        }}>
                            <CreateDataConnector
                                iconClass='jp-s3-logo'
                                dataService={DataService.AMAZON_S3}
                                style={{zoom: 1.4}}
                            />
                        </div>
                        <div>
                            <StyledButton
                                disableElevation
                                style={{ margin: '6px', height: '36px' }}
                                variant='outlined'
                                onClick={this.handleClose}
                                disabled={this.state.waiting}
                                startIcon={<ArrowBackIos />}
                            >
                                Back
                            </StyledButton>
                        </div>
                        <div>
                            <Button
                                disableElevation
                                style={{ margin: '6px', height: '36px' }}
                                variant='contained'
                                color='primary'
                                onClick={() => this.handleCreate(false)}
                                disabled={this.state.waiting}
                            >
                                {this.state.waiting && this.state.createSpinning ? <CircularProgress size='1.75em'/> : 'Create'}
                            </Button>
                            <Button
                                disableElevation
                                style={{ margin: '6px', height: '36px' }}
                                variant='contained'
                                color='primary'
                                onClick={() => this.handleCreate(true)}
                                disabled={(!(Global.labShell.currentWidget instanceof NotebookPanel) && Global.tracker.currentWidget != null) || this.state.waiting}
                            >
                                {this.state.waiting && this.state.addSpinning ? <CircularProgress size='1.75em'/> : 'Create and add to notebook'}
                            </Button>
                        </div>
					</MuiDialogTitle>
                    <ShadowedDivider />
                    <DialogContent style={{padding: '0px'}}>
                        <div style={{padding: '12px'}}>
                            <div style={{margin: '12px 18px 18px 18px'}}>
                                Connect to an Amazon S3 bucket or object.
                            </div>
                            <TextBox<string>
                                getValue={() => this.state.name}
                                saveValue={(value: string) => this.setState({ name: value })}
                                label='Connector Name'
                                helperText="The unique identifier for this connector."
                                labelWidth={LABEL_WIDTH}
                                disabled={this.state.waiting}
                                required
                            />
                            <TextBox<string>
                                getValue={() => '~/s3/'}
                                saveValue={(value: string) => void 0}
                                label='Download Path'
                                helperText="We will create a directory with this name and place your files in it."
                                labelWidth={LABEL_WIDTH}
                                disabled
                                required
                            />
                            <TextBox<string>
                                getValue={() => this.state.bucketName}
                                saveValue={(value: string) => this.setState({ bucketName: value })}
                                label='Bucket Name'
                                helperText='The Bucket Name as specified in S3 documentation.'
                                labelWidth={LABEL_WIDTH}
                                disabled={this.state.waiting}
                                required
                            />
                            <TextBox<string>
                                getValue={() => this.state.objectKey}
                                saveValue={(value: string) => this.setState({ objectKey: value })}
                                label='Object Key'
                                helperText='If you leave this blank, we will transfer the entire bucket.'
                                labelWidth={LABEL_WIDTH}
                                disabled={this.state.waiting}
                            />
                            <TextBox<string>
                                getValue={() => this.state.accessKeyID}
                                saveValue={(value: string) => this.setState({ accessKeyID: value })}
                                label='Access Key ID'
                                helperText='The Access Key ID as specified in S3 documentation.'
                                labelWidth={LABEL_WIDTH}
                                disabled={this.state.waiting}
                                required
                            />
                            <TextBox<string>
                                getValue={() => this.state.accessSecretKey}
                                saveValue={(value: string) => this.setState({ accessSecretKey: value })}
                                label='Access Secret Key'
                                helperText='The Access Secret Key as specified in S3 documentation.'
                                labelWidth={LABEL_WIDTH}
                                disabled={this.state.waiting}
                                required
                            />
                            {this.state.errorMessage && (
                                <div style={{
                                    color: '#f48f8d',
                                    margin: '12px',
                                    wordBreak: 'break-all',
                                    fontSize: '12px',
                                }}>
                                    {this.state.errorMessage}
                                </div>
                            )}
                        </div>
					</DialogContent>
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
