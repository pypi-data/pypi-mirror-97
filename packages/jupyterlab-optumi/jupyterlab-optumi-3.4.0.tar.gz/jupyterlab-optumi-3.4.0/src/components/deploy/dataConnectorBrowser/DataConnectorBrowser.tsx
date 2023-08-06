/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { ServerConnection } from '@jupyterlab/services';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { Global } from '../../../Global';
import { FileMetadata } from '../fileBrowser/FileBrowser';
import DataConnectorDirListing from './DataConnectorDirListing'
import { DataService } from './DataConnectorDirListingItemIcon';

export interface DataConnectorMetadata extends FileMetadata {
    dataService: DataService,
}

interface IProps {
    style?: CSSProperties
    getSelected?: (getSelected: () => DataConnectorMetadata[]) => void
    onAdd?: () => void
    handleDelete?: (dataConnectorMetadata: DataConnectorMetadata) => void
}

interface IState {
    dataConnectors: DataConnectorMetadata[],
}

export default class DataConnectorBrowser extends React.Component<IProps, IState> {
    private _isMounted = false
    private oldOpen: (event: MouseEvent) => boolean

    private getSelected = (): DataConnectorMetadata[] => {
        return this.getSelected();
    }

    constructor(props: IProps) {
        super(props)
        if (this.props.getSelected) {
            this.props.getSelected(this.getSelected);
        }
        this.state = {
            dataConnectors: Global.lastDataConnectors,
        }
    }

    public request = async () => {
        const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + 'optumi/get-data-connectors'
		return ServerConnection.makeRequest(url, {}, settings).then(response => {
			if (response.status !== 200) throw new ServerConnection.ResponseError(response);
			return response.json()
		})
    }

    private handleOpen = (file: FileMetadata) => {
        if (this.props.onAdd) this.props.onAdd();
    }

    public render = (): JSX.Element => {
        return (
            <div className='jp-FileBrowser' style={this.props.style}>
                <DataConnectorDirListing
                    dataConnectors={this.state.dataConnectors}
                    onOpen={this.handleOpen}
                    getSelected={this.props.getSelected && (getSelected => this.getSelected = getSelected)}
                    handleDelete={this.props.handleDelete}
                />
            </div>
        )
    }

    componentDidMount = () => {
        this._isMounted = true
        this.request().then(json => {
            if (this._isMounted) this.setState({dataConnectors: json.connectors});
            Global.lastDataConnectors = json.connectors;
        })
        // Override the JupyterLab context menu open (disable it)
        this.oldOpen = Global.lab.contextMenu.open
        Global.lab.contextMenu.open = () => false
    }

    // Add context menu items back
    componentWillUnmount = () => {
        // Restore the old JupyterLab context menu open
        Global.lab.contextMenu.open = this.oldOpen
        this._isMounted = false
    }
}
