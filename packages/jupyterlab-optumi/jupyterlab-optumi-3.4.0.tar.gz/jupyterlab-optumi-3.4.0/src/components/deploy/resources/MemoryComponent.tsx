/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../../Global';

import { Slider } from '../../../core';
import { MemoryMetadata } from '../../../models/MemoryMetadata';
import { User } from '../../../models/User';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import FormatUtils from '../../../utils/FormatUtils';

interface IProps {
    style?: React.CSSProperties,
}

interface IState {}

export class MemoryComponent extends React.Component<IProps, IState> {
    
    private getSizeValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const memory: MemoryMetadata = optumi.metadata.memory;
        return memory.size[1];
    }
    
    private async saveSizeValue(size: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const memory: MemoryMetadata = optumi.metadata.memory;
        memory.size = [-1, size, -1];
        tracker.setMetadata(optumi);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('MemoryComponentRender (' + new Date().getSeconds() + ')');
        var user: User = Global.user;
        return (
            <div style={this.props.style}>
                <Slider
                    getValue={this.getSizeValue}
                    saveValue={this.saveSizeValue}
                    minValue={-1}
                    step={1048576}
                    maxValue={user.machines.absoluteMemoryMaxSize}
                    label={'Size'}
                    color={'#89858b'}
                    showUnit
                    styledUnit={FormatUtils.styleCapacityUnit()}
                    styledValue={FormatUtils.styleCapacityValue()}
                    unstyledValue={FormatUtils.unstyleCapacityValue()}
                />
            </div>
        )
    }

    private handleMetadataChange = () => { this.forceUpdate() }

    // Will be called automatically when the component is mounted
	componentDidMount = () => {
		Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
	}

	// Will be called automatically when the component is unmounted
	componentWillUnmount = () => {
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