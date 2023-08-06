/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import ReactMarkdown from 'react-markdown'
import gfm from 'remark-gfm';

interface IProps {
    cell: any
    metadata: any
}

interface IState {}

export default class Markdown extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        return (
            <div className='jp-RenderedMarkdown jp-MarkdownOutput jp-RenderedHTMLCommon'>
                <ReactMarkdown plugins={[gfm]} allowDangerousHtml >
                    {this.props.cell.source}
                </ReactMarkdown>
            </div>
        )
    }
}
