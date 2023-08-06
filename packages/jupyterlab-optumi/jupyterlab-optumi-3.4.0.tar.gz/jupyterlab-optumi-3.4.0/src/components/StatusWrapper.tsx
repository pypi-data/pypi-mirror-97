/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';
import { Paper } from '@material-ui/core';

interface IProps {
    style?: React.CSSProperties
    children?: JSX.Element | JSX.Element[]
    statusColor: StatusColor | string
}

interface IState {}

export enum StatusColor {
    RED = '#f48f8d',
    ORANGE = '#ffab61',
    YELLOW = '#fff21c',
    GREEN = '#68da7c',
    BLUE = '#10A0F9',
    LIGHT_BLUE = '#c3d7ff',
    PURPLE = '#934692',
    DARK_GRAY = '#89858b',
    LIGHT_GRAY = '#e7e5e7'
}

export class StatusWrapper extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('StatusRender (' + new Date().getSeconds() + ')');

        return (
            <div style={this.props.style}>
                <Paper elevation={0} style={{marginLeft: '-6px', background: this.props.statusColor}}>
                    <div style={{marginLeft: '6px', padding: '2px'}}>
                        {this.props.children}
                    </div>
                </Paper>
            </div>
        );
    }

    public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
        try {
            if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
            if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
            if (Global.shouldLogOnRender) console.log('SuppressedRender')
            return false;
        } catch (error) {
            return true;
        }
    }
}
