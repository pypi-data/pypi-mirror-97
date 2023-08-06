/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { CSSProperties } from '@material-ui/core/styles/withStyles';

interface IProps {
    style?: CSSProperties
    title: string
    align?: 'left' | 'center' | 'right'
    grey?: boolean
}

interface IState {}

export class Header extends React.Component<IProps, IState> {
    public render = (): JSX.Element => {
        return (
            <div style={Object.assign({
                textAlign: this.props.align || 'left',
                fontSize: '16px',
                fontWeight: 'bold',
                lineHeight: '18px',
                margin: '6px'
            }, this.props.style)}>
                {this.props.title}
            </div>
        )
    }
}

export class SubHeader extends React.Component<IProps, IState> {
    public render = (): JSX.Element => {
        return (
            <div style={Object.assign({
                textAlign: this.props.align || 'left',
                fontSize: '14px',
                fontWeight: 'bold',
                lineHeight: '18px',
                margin: '6px',
                opacity: this.props.grey ? 0.5 : 1,
            }, this.props.style)}>
                {this.props.title}
            </div>
        )
    }
}

