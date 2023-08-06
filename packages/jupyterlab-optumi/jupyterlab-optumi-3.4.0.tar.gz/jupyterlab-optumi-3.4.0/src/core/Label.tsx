/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';
import { CSSProperties } from '@material-ui/core/styles/withStyles';

interface IProps<T> {
    style?: CSSProperties
    label: string
    labelWidth?: string
    getValue: () => T
    styledUnitValue?: (value: T) => string
    align?: 'left' | 'center' | 'right'
}

interface IState<T> {}

export class Label<T> extends React.Component<IProps<T>, IState<T>> {

    static defaultProps: Partial<IProps<any>> = {
        styledUnitValue: (value: any) => { return value.toString() },
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('LabelRender (' + new Date().getSeconds() + ')');
        return (
            <div
                style={Object.assign({display: 'inline-flex', width: '100%', padding: '3px 0px'}, this.props.style)}
            >
                <div style={{
                    minWidth: this.props.labelWidth || '68px',
                    maxWidth: this.props.labelWidth || '68px',
                    height: '24px',
                    margin: '0px 12px',
                    lineHeight: '24px',
                    textAlign: this.props.align || 'center',
                }}>
                    {this.props.label}
                </div>
                <div style={{
                    width: '100%',
                    height: '24px',
                    margin: '0px 6px',
                    lineHeight: '24px',
                }}>
                    <div style={{padding: '0px 6px', fontSize: '12px'}}>
                        {this.props.styledUnitValue(this.props.getValue())}
                    </div>
                </div>
            </div>
        )
    }

    public shouldComponentUpdate = (nextProps: IProps<any>, nextState: IState<any>): boolean => {
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
