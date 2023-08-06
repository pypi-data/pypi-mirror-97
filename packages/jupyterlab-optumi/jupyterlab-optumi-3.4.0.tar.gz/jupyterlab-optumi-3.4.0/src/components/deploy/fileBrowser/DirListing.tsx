/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import DirListingContent from './DirListingContent'
import { FileMetadata } from './FileBrowser'
import { caretUpIcon, caretDownIcon } from '@jupyterlab/ui-components'

interface IProps {
    files: FileMetadata[]
    onOpen: (file: FileMetadata) => void
    getSelected: (getSelected: () => FileMetadata[]) => void
}

interface IState {
    selected: 'name' | 'modified'
    sorted: 'forward' | 'backward'
}

export default class DirListing extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props)
        this.state = {
            selected: 'name',
            sorted: 'forward',
        }
    }

    public render = (): JSX.Element => {
        const sort = (a: FileMetadata, b: FileMetadata) => {
            if (a.type !== b.type && (a.type === 'directory' || b.type === 'directory')) return a.type.localeCompare(b.type);
            const sortDirection = (a: any, b: any): number => a.localeCompare(b) * (this.state.sorted === 'forward' ? 1 : -1);

            if (this.state.selected === 'name') {
                return sortDirection(a.name, b.name)
            } else if (this.state.selected === 'modified') {
                return sortDirection(b.last_modified, a.last_modified)
            }
        }
        return (
            <div className='jp-DirListing jp-FileBrowser-listing' style={{overflow: 'hidden'}}>
                <div className='jp-DirListing-header'>
                    <div
                        className={'jp-DirListing-headerItem jp-id-name' + (this.state.selected === 'name' ? ' jp-mod-selected' : '')}
                        onClick={() => {
                            if (this.state.selected === 'name') {
                                this.setState({sorted: this.state.sorted === 'forward' ? 'backward' : 'forward'})
                            } else {
                                this.setState({selected: 'name', sorted: 'forward'})
                            }
                        }}
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
                    <div
                        className={'jp-DirListing-headerItem jp-id-modified' + (this.state.selected === 'modified' ? ' jp-mod-selected' : '')}
                        onClick={() => {
                            if (this.state.selected === 'modified') {
                                this.setState({sorted: this.state.sorted === 'forward' ? 'backward' : 'forward'})
                            } else {
                                this.setState({selected: 'modified', sorted: 'forward'})
                            }
                        }}
                        style={{flex: '0 0 150px'}}
                    >
                        <span className='jp-DirListing-headerItemText'>
                            Last Modified
                        </span>
                        {this.state.selected === 'modified' && (
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
                <DirListingContent
                    files={this.props.files}
                    onOpen={this.props.onOpen}
                    sort={sort}
                    getSelected={this.props.getSelected}
                />
            </div>
        )
    }
}