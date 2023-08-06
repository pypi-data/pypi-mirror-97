/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';
import { CSSProperties } from '@material-ui/core/styles/withStyles';
import { Paper } from '@material-ui/core';

interface IProps {
    style?: CSSProperties
    children: JSX.Element
    leftButton?: JSX.Element
    rightButton?: JSX.Element
    tags: JSX.Element[]
    specialTag?: JSX.Element[]
    onMouseOver?: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void
    onMouseOut?: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void
}

interface IState {}

export class InfoSkirt extends React.Component<IProps, IState> {

    private handleMouseOver = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.onMouseOver) this.props.onMouseOver(event);
    }

    private handleMouseOut = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.onMouseOut) this.props.onMouseOut(event);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('StatusRender (' + new Date().getSeconds() + ')');

        return (
            <Paper
                elevation={1}
                style={Object.assign({
                    width: '100%',
                    padding: '3px',
                    backgroundColor: 'var(--jp-layout-color2)',
                    borderRadius: '3px',
                }, this.props.style)}
                onMouseOver={this.handleMouseOver}
                onMouseOut={this.handleMouseOut}
            >
                <div style={{
                    display: 'inline-flex',
                    width: '100%',
                }}>
                    <div style={{
                        width: '100%',
                        margin: '3px 0px 3px 3px',
                        overflow: 'hidden',
                    }}>
                        {this.props.children}
                    </div>
                    <div style={{
                        display: 'inline-flex',
                        minWidth: '82px',
                        margin: '3px 3px 3px 0px',
                    }}>
                        <div style={{margin: 'auto 0 auto auto'}}>
                            {this.props.leftButton}
                        </div>
                        <div style={{margin: 'auto auto auto 0'}}>
                            {this.props.rightButton}
                        </div>
                    </div>
                </div>
                <div style={{
                    display: 'inline-flex',
                    flexWrap: 'wrap',
                    width: '100%',
                }}>
                    <div style={{
                        display: 'inline-flex',
                        flexGrow: 1,
                    }}>
                        {this.props.tags.length == 0 ? (
                            <div style={{
                                minWidth: '74px',
                                height: '20px',
                            }}/>
                        ) : (
                            this.props.tags
                        )}
                    </div>
                    <div style={{
                        minWidth: '74px',
                        justifyContent: 'right',
                    }}>
                        {this.props.specialTag}
                    </div>
                </div>
            </Paper>
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
