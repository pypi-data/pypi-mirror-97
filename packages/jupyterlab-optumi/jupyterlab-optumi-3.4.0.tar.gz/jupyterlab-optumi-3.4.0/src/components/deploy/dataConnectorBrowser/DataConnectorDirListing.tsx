/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import DataConnectorDirListingContent from './DataConnectorDirListingContent'
import { caretUpIcon, caretDownIcon } from '@jupyterlab/ui-components'
import { DataConnectorMetadata } from './DataConnectorBrowser'

interface IProps {
    dataConnectors: DataConnectorMetadata[]
    onOpen: (dataConnector: DataConnectorMetadata) => void
    getSelected?: (getSelected: () => DataConnectorMetadata[]) => void
    handleDelete?: (dataConnectorMetadata: DataConnectorMetadata) => void
}

interface IState {
    selected: 'name' | 'dataService'
    sorted: 'forward' | 'backward'
}

export default class DataConnectorDirListing extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props)
        this.state = {
            selected: 'name',
            sorted: 'forward',
        }
    }

    public render = (): JSX.Element => {
        const sort = (a: DataConnectorMetadata, b: DataConnectorMetadata) => {
            const sortDirection = (a: any, b: any): number => a.localeCompare(b) * (this.state.sorted === 'forward' ? 1 : -1);
            if (this.state.selected === 'name') {
                if (a.name === b.name) return a.dataService.localeCompare(b.dataService);
                return sortDirection(a.name, b.name)
            } else if (this.state.selected === 'dataService') {
                if (a.dataService === b.dataService) return a.name.localeCompare(b.name);
                return sortDirection(a.dataService, b.dataService)
            }
        }
        return (
            <div className='jp-DirListing jp-FileBrowser-listing' style={{overflow: 'hidden'}}>
                <div className='jp-DirListing-header'>
                    <div
                        className={'jp-DirListing-headerItem jp-id-data-service' + (this.state.selected === 'dataService' ? ' jp-mod-selected' : '')}
                        onClick={() => {
                            if (this.state.selected === 'dataService') {
                                this.setState({sorted: this.state.sorted === 'forward' ? 'backward' : 'forward'})
                            } else {
                                this.setState({selected: 'dataService', sorted: 'forward'})
                            }
                        }}
                        style={{flex: '0 0 210px', textAlign: 'left', padding: '4px 12px 2px 17px'}}
                    >
                        <span className='jp-DirListing-headerItemText'>
                            Data Service
                        </span>
                        {this.state.selected === 'dataService' && (
                            <span className='jp-DirListing-headerItemIcon' style={{float: 'right'}}>
                                {this.state.sorted === 'forward' ? (
                                    <caretUpIcon.react container={<></> as unknown as HTMLElement} />
                                ) : (
                                    <caretDownIcon.react container={<></> as unknown as HTMLElement} />
                                )}
                            </span>
                        )}
                    </div>
                    <div
                        className={'jp-DirListing-headerItem jp-id-name' + (this.state.selected === 'name' ? ' jp-mod-selected' : '')}
                        onClick={() => {
                            if (this.state.selected === 'name') {
                                this.setState({sorted: this.state.sorted === 'forward' ? 'backward' : 'forward'})
                            } else {
                                this.setState({selected: 'name', sorted: 'forward'})
                            }
                        }}
                        style={{padding: '4px 12px 2px 17px'}}
                    >
                        <span className='jp-DirListing-headerItemText'>
                            Name
                        </span>
                        {this.state.selected === 'name' && (
                            <span className='jp-DirListing-headerItemIcon' style={{float: 'right'}}>
                                {this.state.sorted === 'forward' ? (
                                    <caretUpIcon.react container={<></> as unknown as HTMLElement} />
                                ) : (
                                    <caretDownIcon.react container={<></> as unknown as HTMLElement} />
                                )}
                            </span>
                        )}
                    </div>
                </div>
                <div style={{marginBottom: '6px'}} />
                <DataConnectorDirListingContent
                    dataConnectors={this.props.dataConnectors}
                    handleDelete={this.props.handleDelete}
                    onOpen={this.props.onOpen}
                    sort={sort}
                    getSelected={this.props.getSelected}
                />
                <div style={{marginBottom: '6px'}} />
            </div>
        )
    }
}