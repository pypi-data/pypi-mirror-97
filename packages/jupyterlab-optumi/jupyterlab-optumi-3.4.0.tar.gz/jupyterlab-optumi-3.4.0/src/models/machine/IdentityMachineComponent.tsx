/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { darken, Slider, withStyles } from '@material-ui/core';
import * as React from 'react';
import { Global } from '../../Global';
import ExtraInfo from '../../utils/ExtraInfo';
import FormatUtils from '../../utils/FormatUtils';
import { Machine, NoMachine } from './Machine';

const GraphicsBar = withStyles(forBar('Graphics')) (Slider);
const ComputeBar = withStyles(forBar('Compute')) (Slider);
const MemoryBar = withStyles(forBar('Memory')) (Slider);
const DiskBar = withStyles(forBar('Disk')) (Slider);

function forBar(type: string): any {
    var color: string, trackRadius: string
    if (type == 'Graphics') {
        color = '#ffba7d';
        trackRadius = '4px 4px 4px 0px';
    } else if (type == 'Compute') {
        color = '#f48f8d';
        trackRadius = '0px 4px 4px 0px';
    } else if (type == 'Memory') {
        color = '#afaab0';
        trackRadius = '0px 4px 4px 0px';
    } else if (type == 'Disk') {
        color = '#68da7c';
        trackRadius = '0px 4px 4px 4px';
    }
    return {
        root: {
            marginRight: '5px',
            height: type == 'Disk' ? '14px' : '13px',
            width: '100%',
            padding: '0px',
            lineHeight: 1,
            fontSize: '14px',
        },
        thumb: { // hidden
            height: '14px',
            top: '6px',
            backgroundColor: 'transparent',
            padding: '0px',
            '&:focus, &:hover, &:active': {
                boxShadow: 'none',
            },
            '&::after': {
                left: -6,
                top: -6,
                right: -6,
                bottom: -6,
            },
        },
        track: { // left side
            height: '14px',
            color: color,
            boxSizing: 'border-box',
            border: "1px solid " + darken(color, 0.25),
            borderRadius: trackRadius,
        },
        rail: { // right side
            display: 'none',
        },
    };
}

interface IProps {
    machine: Machine
}

interface IState {}

export class IdentityMachineComponent extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('IdentityMachineComponentRender (' + new Date().getSeconds() + ')');
        const machine = this.props.machine
        const title = machine instanceof NoMachine ? 'No matching machines' : '';
        return (
            <ExtraInfo reminder={title}>
                <div style={{width: '100%', lineHeight: '9px'}}>
                    <div style={{width: '100%', display: 'inline-flex'}}>
                        <GraphicsBar
                            value={machine.graphicsRating}
                            max={1}
                            step={0.01}
                            disabled
                        />
                        <div style={{minWidth: '55px', textAlign: 'right', margin: '2px'}}>
                            {(machine.graphicsNumCards > 0 ? (machine.graphicsNumCards + ' ' + machine.graphicsCardType) : 'No GPU')}
                        </div>
                    </div>
                    <div style={{width: '100%', display: 'inline-flex'}}>
                        <ComputeBar
                            value={machine.computeRating}
                            max={1}
                            step={0.01}
                            disabled
                        />
                        <div style={{minWidth: '55px', textAlign: 'right', margin: '2px'}}>
                            {machine.computeCores} cores
                        </div>
                    </div>
                    <div style={{width: '100%', display: 'inline-flex'}}>                
                        <MemoryBar
                            value={machine.memoryRating}
                            max={1}
                            step={0.01}
                            disabled
                        />
                        <div style={{minWidth: '55px', textAlign: 'right', margin: '2px'}}>
                            {FormatUtils.styleCapacityUnitValue()(machine.memorySize)}
                        </div>
                    </div>
                    <div style={{width: '100%', display: 'inline-flex'}}>                
                        <DiskBar
                            value={machine.storageRating}
                            max={1}
                            step={0.01}
                            disabled
                        />
                        <div style={{minWidth: '55px', textAlign: 'right', margin: '2px'}}>
                            {machine.storageSize != 0 ? FormatUtils.styleCapacityUnitValue()(machine.storageSize) : 'No disk'}
                        </div>
                    </div>
                </div>
            </ExtraInfo>
        )
    }
}