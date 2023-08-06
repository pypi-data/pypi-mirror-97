/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Divider } from '@material-ui/core';
import * as React from 'react';
import { Header, Label } from '../../core';
import { Global } from '../../Global';
import FormatUtils from '../../utils/FormatUtils';
import { Machine } from './Machine';

interface IProps {
    machine: Machine
}

interface IState {}

export class MachineCapability extends React.Component<IProps, IState> {
    _isMounted = false;

    constructor(props: IProps) {
        super(props);
        this.state = {};
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('MachineCapabilitiesRender (' + new Date().getSeconds() + ')');
        const machine = this.props.machine;
        return (
            <>
                {machine.graphicsNumCards > 0 && (
                    <>
                        <div style={{ margin: '6px' }}>
                            <Header title='GPU' align='left' />
                            {machine.graphicsCardType !== 'None' && <Label<string>
                                align='left'
                                getValue={() => machine.graphicsCardType}
                                label='Type'
                            />}
                            {machine.graphicsNumCards > 0 && <Label<number>
                                align='left'
                                getValue={() => machine.graphicsNumCards}
                                label='Count'
                            />}
                            {Global.user.userExpertise >= 2 && machine.graphicsCores > 0 && <Label<number>
                                align='left'
                                getValue={() => machine.graphicsCores}
                                label='Cores'
                            />}
                            {Global.user.userExpertise >= 2 && machine.graphicsScore > 0 && <Label<number>
                                align='left'
                                getValue={() => machine.graphicsScore}
                                label='Score'
                            />}
                            {Global.user.userExpertise >= 2 && machine.graphicsFrequency > 0 && <Label<number>
                                align='left'
                                getValue={() => machine.graphicsFrequency}
                                label='Frequency'
                                styledUnitValue={FormatUtils.styleFrequencyUnitValue()}
                            />}
                        </div>
                        <Divider variant='middle' />
                    </>
                )}
                {machine.computeCores > 0 && (
                    <>
                        <div style={{ margin: '6px' }}>
                            <Header title='CPU' align='left' />
                            {machine.computeCores > 0 && <Label<number>
                                align='left'
                                getValue={() => machine.computeCores}
                                label='Cores'
                            />}
                            {Global.user.userExpertise >= 2 && machine.computeScore > 0 && <Label<number>
                                align='left'
                                getValue={() => machine.computeScore}
                                label='Score'
                            />}
                            {Global.user.userExpertise >= 2 && machine.computeFrequency > 0 && <Label<number>
                                align='left'
                                getValue={() => machine.computeFrequency}
                                label='Frequency'
                                styledUnitValue={FormatUtils.styleFrequencyUnitValue()}
                            />}
                        </div>
                        <Divider variant='middle' />
                    </>
                )}
                {machine.memorySize > 0 && (
                    <>
                        <div style={{ margin: '6px' }}>
                            <Header title='RAM' align='left' />
                            {machine.memorySize > 0 && <Label<number>
                                align='left'
                                getValue={() => machine.memorySize}
                                label='Size'
                                styledUnitValue={FormatUtils.styleCapacityUnitValue()}
                            />}
                        </div>
                        <Divider variant='middle' />
                    </>
                )}
                {machine.storageSize > 0 && (
                    <>
                        <div style={{ margin: '6px' }}>
                            <Header title='DSK' align='left' />
                            {machine.storageSize > 0 && <Label<number>
                                align='left'
                                getValue={() => machine.storageSize}
                                label='Size'
                                styledUnitValue={FormatUtils.styleCapacityUnitValue()}
                            />}
                            {Global.user.userExpertise >= 2 && machine.storageIops > 0 && <Label<number>
                                align='left'
                                getValue={() => machine.storageIops}
                                label='IOPS'
                            />}
                            {Global.user.userExpertise >= 2 && machine.storageThroughput > 0 && <Label<number>
                                align='left'
                                getValue={() => machine.storageThroughput}
                                label='Throughput'
                                styledUnitValue={FormatUtils.styleThroughputUnitValue()}
                            />}
                        </div>
                        <Divider variant='middle' />
                    </>
                )}
            </>
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


    public componentDidMount = () => {
        this._isMounted = true
    }

	public componentWillUnmount = () => {
        this._isMounted = false
    }
}
