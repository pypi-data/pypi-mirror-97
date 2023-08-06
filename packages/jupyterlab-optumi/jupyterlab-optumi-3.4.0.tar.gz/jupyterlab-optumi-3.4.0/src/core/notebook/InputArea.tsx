/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import Editor from './Editor'
import Markdown from './Markdown'

interface IProps {
    cell: any
    metadata: any
}

interface IState {}

export default class InputArea extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        return (
            <div className='p-Widget lm-Widget jp-Cell-inputWrapper'>
                <div className='p-Widget lm-Widget jp-InputArea jp-Cell-inputArea'>
                    <div className='p-Widget lm-Widget jp-InputPrompt jp-InputArea-prompt'>
                    {this.props.cell.cell_type === 'code' ? (
                        <>
                            {this.props.cell.execution_count !== undefined && `[${this.props.cell.execution_count === null ? ' ' : this.props.cell.execution_count}]:`}
                        </>
                    ) : this.props.cell.cell_type === 'markdown' ? (
                        <></>
                    ) : (
                        <></>
                    )}
                    </div>
                    {this.props.cell.cell_type === 'code' ? (
                        <Editor cell={this.props.cell} metadata={this.props.metadata} />
                    ) : this.props.cell.cell_type === 'markdown' ? (
                        <Markdown cell={this.props.cell} metadata={this.props.metadata} />
                    ) : (
                        <></>
                    )}
                </div>
            </div>
        )
    }
}