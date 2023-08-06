/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';
import withStyles, { CSSProperties } from '@material-ui/core/styles/withStyles';
import { Button } from '@material-ui/core';

import RadioButtonUncheckedIcon from '@material-ui/icons/RadioButtonUnchecked';
import CheckCircleIcon from '@material-ui/icons/CheckCircle';

interface IProps {
    style?: CSSProperties
    label: string
    selected: boolean
    hexColor: string
    beta?: boolean
    handleClick: () => string | void
    onMouseOver?: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void
    onMouseOut?: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void
}

interface IState {}

export class OutlinedResourceRadio extends React.Component<IProps, IState> {
    textField: React.RefObject<HTMLInputElement>

    StyledButton: any

    constructor(props: IProps) {
        super(props);
        this.StyledButton = this.getStyledButton(this.props.hexColor);
    }

    private handleMouseOver = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.onMouseOver) this.props.onMouseOver(event);
    }

    private handleMouseOut = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.onMouseOut) this.props.onMouseOut(event);
    }

    private getStyledButton = (color: string) => {
        return withStyles({
            root: {
                textAlign: 'center',
                fontWeight: 'normal',
                display: 'inline-flex',
                padding: '6px',
                height: '34px',
                border: '2px solid ' + color + '80',
                borderRadius: '6px',
                margin: '0px 6px 6px 6px',
                width: 'calc(100% - 12px)',
                transition: 'background-color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms',
                overflow: 'hidden',
                position: 'relative',
                '&:hover': {
                    border: '2px solid ' + color + '80',
                    backgroundColor: color + '40'
                },
            },
        }) (Button)
    }
    
    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ResourceTextBoxRender (' + new Date().getSeconds() + ')');
        return (
            <this.StyledButton
                style={Object.assign({
                    border: this.props.selected ? '2px solid ' + this.props.hexColor : '',
                    backgroundColor: this.props.selected ? this.props.hexColor + '40' : '',
                }, this.props.style)}
                onClick={() => this.props.handleClick()}
                onMouseOver={this.handleMouseOver}
                onMouseOut={this.handleMouseOut}
            >
                <span style={{
                    flexGrow: 1,
                    lineHeight: '14px',
                    margin: 'auto auto auto 6px',
                    textAlign: 'center',
                    whiteSpace: 'pre-wrap',
                }}>
                    {(this.props.beta ? ' ' : '' /* This extra space is explicitly for 'Session' launch mode so we dont forget to remove the space when we remove the beta label */) + this.props.label}
                </span>
                {this.props.selected ? (
                    <CheckCircleIcon
                        fontSize='small'
                        style={{
                            fill: this.props.hexColor,
                            margin: 'auto',
                        }}
                    />
                ) : (
                    <RadioButtonUncheckedIcon
                        fontSize='small'
                        style={{
                            fill: this.props.hexColor + '80',
                            margin: 'auto',
                        }}
                    />
                )}
                {this.props.beta && (
                    <div style={{
                        position: 'absolute',
                        left: '-22px',
                        top: '3px',
                        transform: 'rotate(-45deg)',
                        background: this.props.selected ? this.props.hexColor : this.props.hexColor + '80',
                        color: '#ffffff',
                        fontSize: '9px',
                        lineHeight: '14px',
                        fontWeight: 'bold',
                        padding: '0px 20px',
                    }}>
                        BETA
                    </div>
                )}
            </this.StyledButton>
        )
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
