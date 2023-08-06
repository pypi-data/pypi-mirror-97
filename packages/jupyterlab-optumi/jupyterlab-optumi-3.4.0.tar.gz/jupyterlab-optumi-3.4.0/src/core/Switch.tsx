/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';
import { withStyles, Switch as OtherSwitch } from '@material-ui/core';
import ExtraInfo from '../utils/ExtraInfo';

interface IProps {
    style?: React.CSSProperties
    tooltip?: string
    getValue: () => boolean
    saveValue: (value: boolean) => void
    label: string
    labelWidth?: string
    flip?: boolean
    ref?: any
    onMouseOver?: (...args: any[]) => any
    onMouseOut?: (...args: any[]) => any
}

interface IState {
    value: boolean,
}

export const getStyledSwitch = () => {
    return withStyles({
        root: {
            width: '42px',
            height: '24px',
            padding: '0px',
        },
        thumb: {
            width: '20px',
            height: '20px',
            padding: '0px',
            margin: '2px',
        },
        switchBase: {
            padding: '0px',
        },
        track: {
            height: '12px',
            width: '34px',
            borderRadius: '6px',
            padding: '0px',
            margin: '6px',
        },
    }) (OtherSwitch);
}

export class Switch extends React.Component<IProps, IState> {

    StyledSwitch: any;

    public constructor(props: IProps) {
        super (props);
        this.StyledSwitch = getStyledSwitch();
        this.state = { value: this.props.getValue() }
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('SwitchRender (' + new Date().getSeconds() + ')');
        return (
            <div
                style={Object.assign({
                    display: 'inline-flex',
                    width: '100%',
                    padding: '6px 0px',
                    direction: this.props.flip ? 'rtl' : 'ltr'
                }, this.props.style)}
                ref={this.props.ref}
                onMouseOver={this.props.onMouseOver}
                onMouseOut={this.props.onMouseOut}
            >
                <ExtraInfo reminder={this.props.tooltip || ''}>
                    <div 
                        style={{
                        minWidth: this.props.labelWidth || '68px',
                        lineHeight: '24px',
                        textAlign: 'center',
                        margin: '0px 12px',
                    }}>
                        <this.StyledSwitch
                            color='primary'
                            inputProps={{style: {height: '24px'}}}
                            checked={this.state.value}
                            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                                this.setState({value: event.currentTarget.checked})
                                this.props.saveValue(event.currentTarget.checked)
                            }}
                        />
                    </div>
                </ExtraInfo>
                <div style={{width: '100%', textAlign: this.props.flip ? 'right' : 'left', margin: 'auto 6px'}}>
                    {this.props.label}                    
                </div>
            </div>
        )
    }

    private handleMetadataChange = () => { this.setState({value: this.props.getValue()}) }
    private handleThemeChange = () => {
        this.StyledSwitch = getStyledSwitch()
        this.forceUpdate();
    }

    // Will be called automatically when the component is mounted
	componentDidMount = () => {
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
        Global.themeManager.themeChanged.connect(this.handleThemeChange);
	}

	// Will be called automatically when the component is unmounted
	componentWillUnmount = () => {
        Global.themeManager.themeChanged.disconnect(this.handleThemeChange);
        Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
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
