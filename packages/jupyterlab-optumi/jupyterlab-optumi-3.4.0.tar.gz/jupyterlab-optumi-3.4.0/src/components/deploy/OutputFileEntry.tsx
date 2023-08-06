/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import { ServerConnection } from '@jupyterlab/services';

import {
	ListItem,
	IconButton,
	CircularProgress,
} from '@material-ui/core';

import GetAppIcon from '@material-ui/icons/GetApp';
import DoneIcon from '@material-ui/icons/Done';

// Properties from parent
interface IProps {
	workloadUUID: string;
    moduleUUID: string;
    name: string;
	lastModified: string;
	size: number;
	files: string[];
    disabled: boolean;
    overwrite: boolean;
}

// Properties for this component
interface IState {
	loaded: number;
    total: number;
    downloading: boolean;
	downloaded: boolean;
}

export class OutputFileEntry extends React.Component<IProps, IState> {
	// We need to know if the component is mounted to change state
	_isMounted = false;
	
	constructor(props: IProps) {
		super(props);
		this.state = {
			loaded: 0,
            total: 0,
            downloading: false,
			downloaded: false,
		};
	}

	private getDownloadProgress(name: string) {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/get-file-download-progress";
		const init: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				// The key we use to watch download progress
                name: name,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			if (response.status == 204) {
				setTimeout(() => this.getDownloadProgress(name), 500);
				return;
			}
			return response.json();
		}).then((body: any) => {
			if (body) {
				this.checkAndSetState({ loaded: body.read, total: body.total });
				if (!(body.read != 0 && body.read == body.total)) {
					setTimeout(() => this.getDownloadProgress(name), 500);
				}
			}
		}, (error: ServerConnection.ResponseError) => {
			setTimeout(() => this.getDownloadProgress(name), 500);
		});
	}

	public async saveOutputFile(name: string, files: string[]) {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "optumi/save-notebook-output-file";
		const init = {
			method: 'POST',
			body: JSON.stringify({
				workloadUUID: this.props.workloadUUID,
				moduleUUID: this.props.moduleUUID,
				name: name,
                files: files,
                overwrite: this.props.overwrite,
			}),
		};
		ServerConnection.makeRequest(
			url,
			init, 
			settings
		).then((response: Response) => {
			Global.handleResponse(response);
			return response.text();
		}).then((body: string) => {
			this.checkAndSetState({ downloaded: true, downloading: false })
			setTimeout(() => this.checkAndSetState({ downloaded: false }), 5000);
		});
		this.getDownloadProgress(name);
	}

	private formatSize = (value: number) => {
		if (value < Math.pow(1024, 1)) {
            return value.toFixed() + ' B';
        } else if (value < Math.pow(1024, 2)) {
            return (value / Math.pow(1024, 1)).toFixed(1) + ' KiB';
        } else if (value < Math.pow(1024, 3)) {
            return (value / Math.pow(1024, 2)).toFixed(1) + ' MiB';
        } else if (value < Math.pow(1024, 4)) {
            return (value / Math.pow(1024, 3)).toFixed(1) + ' GiB';
        } else if (value < Math.pow(1024, 5)) {
            return (value / Math.pow(1024, 4)).toFixed(1) + ' TiB';
        } else {
            return (value / Math.pow(1024, 5)).toFixed(1) + ' PiB';
        }
	}

	private formatExtraInfo = () => {
		var lastModified = this.props.lastModified == "" ? "" : new Date(this.props.lastModified).toLocaleTimeString();
		var size = this.props.size == 0 ? "" : this.formatSize(this.props.size);
		if (lastModified == "" && size == "") return "";
		if (lastModified == "") return " (" + size + ")";
		if (size == "") return " (" + lastModified + ")";
		return " (" + size + ", " + lastModified + ")";
	}

	// The contents of the component
	render() {
		if (Global.shouldLogOnRender) console.log('OutputFileEntryRender (' + new Date().getSeconds() + ')');
		return (
            <ListItem style={{paddingTop: "2px", paddingBottom: "2px"}}>
				{ this.state.downloaded ? (
					<IconButton
						edge="end"
						disabled
					>
						<DoneIcon />
					</IconButton>
				) : (
					<div>
						{!this.state.downloading ? (
							<IconButton
								edge="end"
								disabled={this.props.disabled}
								onClick={ () => {
										this.saveOutputFile(this.props.name, this.props.files);
										this.checkAndSetState({ downloading: true });
									}
								}
							>
								<GetAppIcon />
							</IconButton>
						) : (
							<div style={{position: 'relative', height: '48px', width: '48px'}}>
								<CircularProgress />
                                <span style={{position: 'absolute', top: '12.5px', left: '9px', fontSize: '0.75rem'}}>
									{this.state.loaded != this.state.total ? ((this.state.loaded/this.state.total) * 100).toFixed(0) + "%" : ''}
								</span>
							</div>
						)}
					</div>
				)}
                <div
					style={{
						overflow: 'auto',
						marginLeft: !this.state.downloading ? '24px' : '12px',
						marginTop: '4px',
						marginBottom: '4px',
						opacity: this.props.disabled ? '0.5' : '1',
					}}>
					{ this.props.name + this.formatExtraInfo() }
				</div>
                    
            </ListItem>
		);
	}

	private update() {
		if (this._isMounted) {
			this.forceUpdate();
		}
	}

	// Will be called automatically when the component is mounted
	componentDidMount = () => {
		this._isMounted = true;
		this.update();
	}

	// Will be called automatically when the component is unmounted
	componentWillUnmount = () => {
		this._isMounted = false;
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
