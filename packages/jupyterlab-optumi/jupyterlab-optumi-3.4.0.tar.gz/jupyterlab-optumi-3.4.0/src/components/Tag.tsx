/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { withStyles, LinearProgress, Chip } from '@material-ui/core';
import { Global } from '../Global';
import { StatusColor } from './StatusWrapper';

interface IProps {
    id?: string
    label: string
    color?: string
    showLoading?: boolean
    percentLoaded?: number
    icon? : JSX.Element;
    onMouseOver?: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void
    onMouseOut?: (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => void
}

interface IState {}

const progressBorderSize: number = 1

export class Tag extends React.Component<IProps, IState> {

    // Do some extra work to avoid creating new styles every time this component renders
    PreviousStyledChip: any = null;
    PreviousStyledLinearProgress: any = null;

    StyledChip: any;
    StyledLinearProgress: any;

    public constructor(props: IProps) {
        super(props);
        this.StyledChip = this.getStyledChip();
        this.StyledLinearProgress = this.getStyledLinearProgress();
    }

    private getStyledChip = () => {
        const newStyledChip = withStyles({
            root: {
                position: 'relative',
                bottom: '0px',
                margin: `${progressBorderSize}px`,
                height: '18px',
                width: ((Global.getStringWidth(this.props.label, '13px Roboto, Helvetica, Arial, sans-serif') + 14) + (this.props.icon ? 14 : 0)) + 'px',
                backgroundColor: 'var(--jp-layout-color2)',
            },
            label: {
                overflow: 'visible',
            }
        }) (Chip);
        this.PreviousStyledChip = JSON.stringify(newStyledChip) == JSON.stringify(this.PreviousStyledChip) ? this.PreviousStyledChip : newStyledChip;
        return this.PreviousStyledChip;
    }

    private getStyledLinearProgress = () => {
        const newStyledLinearProgress = withStyles({
            root: {
                position: 'absolute',
                bottom: '0px',
                width: (Global.getStringWidth(this.props.label, '13px Roboto, Helvetica, Arial, sans-serif') + 14 + (2 * progressBorderSize)) + 'px',
                height: `${18 + (2 * progressBorderSize)}px`,
                borderRadius: `${(18 + (2 * progressBorderSize)) / 2}px`,
            },
            barColorPrimary: {
                backgroundColor: this.props.color || '#10A0F9',
            },
            colorPrimary: {
                backgroundColor: StatusColor.DARK_GRAY,
            },
        }) (LinearProgress);
        this.PreviousStyledLinearProgress = JSON.stringify(newStyledLinearProgress) == JSON.stringify(this.PreviousStyledLinearProgress) ? this.PreviousStyledLinearProgress : newStyledLinearProgress;
        return this.PreviousStyledLinearProgress;
    }

    private handleMouseOver = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.onMouseOver) this.props.onMouseOver(event);
    }

    private handleMouseOut = (event: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
        if (this.props.onMouseOut) this.props.onMouseOut(event);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('TagRender (' + new Date().getSeconds() + ')');
        this.StyledChip = this.getStyledChip();
        this.StyledLinearProgress = this.getStyledLinearProgress();
        return (
            <>
                {this.props.label != "" && this.props.label != undefined &&
                    <div
                        style={{
                            position: 'relative',
                            margin: '3px',
                        }}
                        onMouseOver={this.handleMouseOver}
                        onMouseOut={this.handleMouseOut}
                    >
                        {this.props.showLoading && (
                            this.props.percentLoaded === undefined ? (
                                <this.StyledLinearProgress />
                            ) : (
                                <this.StyledLinearProgress variant='determinate' value={this.props.percentLoaded * 100} />
                            )
                        )}
                        <this.StyledChip
                            id={this.props.id}
                            size='small'
                            label={this.props.label}
                            icon={this.props.icon}
                            style={{border: !this.props.showLoading ? '1px solid ' + (this.props.color || StatusColor.DARK_GRAY) : ''}}
                        />
                    </div>
                }
            </>
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
