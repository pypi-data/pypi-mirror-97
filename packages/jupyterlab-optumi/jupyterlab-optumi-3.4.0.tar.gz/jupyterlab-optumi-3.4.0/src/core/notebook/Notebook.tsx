/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { Global } from '../../Global'
import CodeCell from './CodeCell'
import MarkdownCell from './MarkdownCell'

interface IProps {
    notebook: {cells: any[], metadata: any}
}

interface IState {}

export default class Notebook extends React.Component<IProps, IState> {
    private oldOpen: (event: MouseEvent) => boolean

    public render = (): JSX.Element => {
        const notebook = this.props.notebook
        let i = 0;
        return (
            <div className='p-Widget lm-Widget jp-Notebook jp-NotebookPanel-notebook jp-mod-scrollPastEnd jp-mod-commandMode'>
                {notebook.cells.map(cell => 
                    cell.cell_type === 'code' ? (
                        <CodeCell key={i++} cell={cell} metadata={notebook.metadata} />
                    ) : cell.cell_type === 'markdown' ? (
                        <MarkdownCell key={i++} cell={cell} metadata={notebook.metadata} />
                    ) : (
                        <></>
                    )
                )}
            </div>
        )
    }

    public componentDidMount = () => {
        // Override the JupyterLab context menu open (disable it)
        this.oldOpen = Global.lab.contextMenu.open;
        Global.lab.contextMenu.open = () => false;
    }

    // Add context menu items back
    public componentWillUnmount = () => {
        // Restore the old JupyterLab context menu open
        Global.lab.contextMenu.open = this.oldOpen;
    }
}
