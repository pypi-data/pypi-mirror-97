/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import DirListingItem from './DirListingItem'
import { FileMetadata } from './FileBrowser'

interface IProps {
    files: FileMetadata[]
    onOpen: (file: FileMetadata) => void
    sort: (a: FileMetadata, b: FileMetadata) => number
    getSelected: (getSelected: () => FileMetadata[]) => void
}

interface IState {
    selected: FileMetadata[]
}

export default class DirListingContent extends React.Component<IProps, IState> {
    firstClicked: FileMetadata // Pressing enter operates on this file
    lastClicked: FileMetadata

    constructor(props: IProps) {
        super(props)
        this.props.getSelected(() => this.state.selected)
        this.state = {
            selected: []
        }
    }

    public render = (): JSX.Element => {
        const sortedFiles = this.props.files.sort(this.props.sort)
        return (
            <ul className='jp-DirListing-content' style={{overflowY: 'auto'}}>
                {sortedFiles.map(file => (
                    <DirListingItem
                        key={file.path + file.name}
                        file={file}
                        selected={this.state.selected.includes(file)}
                        onClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => {
                            if (this.firstClicked === undefined) {
                                if (event.shiftKey) {
                                    this.firstClicked = sortedFiles[0]
                                    this.lastClicked = sortedFiles[0]
                                } else {
                                    this.firstClicked = file
                                }
                            }
                            if (event.ctrlKey) {
                                const newSelected = this.state.selected
                                if (newSelected.includes(file)) {
                                    newSelected.splice(newSelected.indexOf(file), 1)
                                } else {
                                    newSelected.push(file)
                                }
                                this.setState({selected: newSelected})
                                this.lastClicked = file
                            } else if (event.shiftKey) {
                                const newSelected = this.state.selected
                                let index = sortedFiles.indexOf(file)
                                const lastClickedIndex = sortedFiles.indexOf(this.lastClicked)
                                const direction = index < lastClickedIndex ? 1 : -1
                                while (!newSelected.includes(sortedFiles[index]) && index !== lastClickedIndex) {
                                    newSelected.push(sortedFiles[index])
                                    index += direction
                                }
                                if (index === lastClickedIndex && !newSelected.includes(this.lastClicked)) newSelected.push(this.lastClicked);
                                this.setState({selected: newSelected})
                            } else {
                                this.setState({selected: [file]})
                                this.firstClicked = file
                                this.lastClicked = file
                            }
                        }}
                        onDoubleClick={(event: React.MouseEvent<HTMLLIElement, MouseEvent>) => {
                            if (!event.ctrlKey && !event.shiftKey) this.props.onOpen(file);
                        }}
                    />
                ))}
            </ul>
        )
    }
}