/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { DataConnectorMetadata } from './DataConnectorBrowser'
import DataConnectorDirListingItem from './DataConnectorDirListingItem'
import { DataService } from './DataConnectorDirListingItemIcon'

interface IProps {
    dataConnectors: DataConnectorMetadata[]
    onOpen: (dataConnector: DataConnectorMetadata) => void
    sort: (a: DataConnectorMetadata, b: DataConnectorMetadata) => number
    getSelected?: (getSelected: () => DataConnectorMetadata[]) => void
    handleDelete?: (dataConnectorMetadata: DataConnectorMetadata) => void
}

interface IState {
    selected: DataConnectorMetadata[]
}

export default class DataConnectorDirListingContent extends React.Component<IProps, IState> {
    firstClicked: DataConnectorMetadata // Pressing enter operates on this file
    lastClicked: DataConnectorMetadata

    constructor(props: IProps) {
        super(props)
        if (this.props.getSelected) this.props.getSelected(() => this.state.selected);
        this.state = {
            selected: []
        }
    }

    public render = (): JSX.Element => {
        const sortedDataConnectors = this.props.dataConnectors.sort(this.props.sort)
        return (
            <ul className='jp-DirListing-content' style={{overflowY: 'auto'}}>
                {sortedDataConnectors.length == 0 ? (
                    <>
                        <DataConnectorDirListingItem
                            key={'empty'}
                            dataConnectorMetadata={{
                                name: '--',
                                dataService: DataService.EMPTY,
                            } as DataConnectorMetadata}
                            selected={false}
                            onClick={() => false}
                            onDoubleClick={() => false}
                        />
                    </>
                ) : (
                    <>
                        {sortedDataConnectors.map(dataConnector => (
                            <DataConnectorDirListingItem
                                key={dataConnector.path + dataConnector.name}
                                dataConnectorMetadata={dataConnector}
                                selected={this.state.selected.includes(dataConnector)}
                                handleButtonClick={this.props.handleDelete}
                                buttonText='Delete'
                                buttonColor='#f48f8d'
                                onClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => {
                                    if (this.props.getSelected === undefined) return; // If someone doesn't want what is selected, don't select.
                                    if (this.firstClicked === undefined) {
                                        if (event.shiftKey) {
                                            this.firstClicked = sortedDataConnectors[0]
                                            this.lastClicked = sortedDataConnectors[0]
                                        } else {
                                            this.firstClicked = dataConnector
                                        }
                                    }
                                    if (event.ctrlKey) {
                                        const newSelected = this.state.selected
                                        if (newSelected.includes(dataConnector)) {
                                            newSelected.splice(newSelected.indexOf(dataConnector), 1)
                                        } else {
                                            newSelected.push(dataConnector)
                                        }
                                        this.setState({selected: newSelected})
                                        this.lastClicked = dataConnector
                                    } else if (event.shiftKey) {
                                        const newSelected = this.state.selected
                                        let index = sortedDataConnectors.indexOf(dataConnector)
                                        const lastClickedIndex = sortedDataConnectors.indexOf(this.lastClicked)
                                        const direction = index < lastClickedIndex ? 1 : -1
                                        while (!newSelected.includes(sortedDataConnectors[index]) && index !== lastClickedIndex) {
                                            newSelected.push(sortedDataConnectors[index])
                                            index += direction
                                        }
                                        if (index === lastClickedIndex && !newSelected.includes(this.lastClicked)) newSelected.push(this.lastClicked);
                                        this.setState({selected: newSelected})
                                    } else {
                                        this.setState({selected: [dataConnector]})
                                        this.firstClicked = dataConnector
                                        this.lastClicked = dataConnector
                                    }
                                }}
                                onDoubleClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => {
                                    if (!event.ctrlKey && !event.shiftKey) this.props.onOpen(dataConnector);
                                }}
                            />
                        ))}
                    </>
                )}
            </ul>
        )
    }
}