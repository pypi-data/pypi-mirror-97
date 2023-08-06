/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import Ansi from 'ansi-to-react'
import * as React from 'react'
import Linkify from 'react-linkify'

interface IProps {
    cell: any
    metadata: any
}

interface IState {}

export default class OutputArea extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        let i = 0
        return (
            <div className='p-Widget lm-Widget jp-Cell-outputWrapper'>
                <div className='p-Widget lm-Widget jp-OutputArea jp-Cell-outputArea'>
                    <div className='p-Widget lm-Widget jp-OutputArea-child'>
                        <div className='p-Widget lm-Widget jp-OutputPrompt jp-OutputArea-prompt' />
                        {/* This extra div stops the out/err groups rendering as columns */}
                        <div style={{display: 'block', width: '100%'}}>
                            {this.props.cell.outputs.map((output: any) => (
                                <div key={i++} data-mime-type={output.name === 'stderr' || output.output_type === 'error' ? 'application/vnd.jupyter.stderr' : 'application/vnd.jupyter.stdout'} className='p-Widget lm-Widget jp-RenderedText jp-OutputArea-output'>
                                    {output.output_type === 'stream' ? (
                                        <Linkify componentDecorator={(decoratedHref: string, decoratedText: string, key: number) => {
                                            return (
                                                <a key={key} href={decoratedHref} rel={`noopener`} target={`_blank`}>
                                                    {decoratedText}
                                                </a>
                                            )
                                        }}>
                                            <pre>
                                                {/*This will remove any backspace characters still here*/}
                                                {output.text.map((x: string) => x.replace(/\x08/g, ''))}
                                            </pre>
                                        </Linkify>
                                    ) : output.output_type === 'error' ? (
                                        output.traceback.map((line: string) => (
                                            <pre key={line}>
                                                <Ansi>
                                                    {line}
                                                </Ansi>
                                            </pre>
                                        ))
                                    ) : output.output_type === 'display_data' ? (
                                        <></>
                                    ) : (
                                        <></>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}
