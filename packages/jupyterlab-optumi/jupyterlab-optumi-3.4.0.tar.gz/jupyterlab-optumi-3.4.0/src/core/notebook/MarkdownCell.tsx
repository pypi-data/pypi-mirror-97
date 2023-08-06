/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import InputArea from './InputArea'

interface IProps {
    cell: any
    metadata: any
}

interface IState {}

export default class MarkdownCell extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        return (
            <div className='p-Widget lm-Widget jp-Cell jp-MarkdownCell jp-Notebook-cell'>
                <InputArea cell={this.props.cell} metadata={this.props.metadata} />
            </div>
        )
    }
}