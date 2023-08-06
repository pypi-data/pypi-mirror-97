/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../../Global';

import { Slider } from '../../../core';
import { GraphicsMetadata } from '../../../models/GraphicsMetadata';
import { User } from '../../../models/User';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import FormatUtils from '../../../utils/FormatUtils';

interface IProps {
    style?: React.CSSProperties,
}

interface IState {}

export class GraphicsComponent extends React.Component<IProps, IState> {
        
    private getCoresValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsMetadata = optumi.metadata.graphics;
        return graphics.cores[1];
    }

    private async saveCoresValue(cores: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsMetadata = optumi.metadata.graphics;
        graphics.cores = [-1, cores, -1];
        tracker.setMetadata(optumi);
    }

    private getScoreValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsMetadata = optumi.metadata.graphics;
        return graphics.score[1];
    }
    
    private async saveScoreValue(score: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsMetadata = optumi.metadata.graphics;
        graphics.score = [-1, score, -1];
        tracker.setMetadata(optumi);
    }

    private getFrequencyValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsMetadata = optumi.metadata.graphics;
        return graphics.frequency[1];
    }
    
    private async saveFrequencyValue(frequency: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsMetadata = optumi.metadata.graphics;
        graphics.frequency = [-1, frequency, -1];
        tracker.setMetadata(optumi);
    }

    private getMemoryValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsMetadata = optumi.metadata.graphics;
        return graphics.memory[1];
    }
    
    private async saveMemoryValue(memory: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsMetadata = optumi.metadata.graphics;
        graphics.memory = [-1, memory, -1];
        tracker.setMetadata(optumi);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('GraphicsComponentRender (' + new Date().getSeconds() + ')');
        var user: User = Global.user;
        return (
            <div style={this.props.style}>
                <Slider
                    getValue={this.getCoresValue}
                    saveValue={this.saveCoresValue}
                    minValue={-1}
                    maxValue={user.machines.absoluteGraphicsMaxCores}
                    label={'Cores'}
                    color={'#ffba7d'}
                    showUnit
                />
                <Slider
                    getValue={this.getScoreValue}
                    saveValue={this.saveScoreValue}
                    minValue={-1}
                    maxValue={user.machines.absoluteGraphicsMaxScore}
                    label={'Score'}
                    color={'#ffba7d'}
                    showUnit
                />
                <Slider
                    getValue={this.getFrequencyValue}
                    saveValue={this.saveFrequencyValue}
                    minValue={-1}
                    step={1000000}
                    maxValue={user.machines.absoluteGraphicsMaxFrequency}
                    label={'Frequency'}
                    color={'#ffba7d'}
                    showUnit
                    styledUnit={FormatUtils.styleFrequencyUnit()}
                    styledValue={FormatUtils.styleFrequencyValue()}
                    unstyledValue={FormatUtils.unstyleFrequencyValue()}
                />
                <Slider
                    getValue={this.getMemoryValue}
                    saveValue={this.saveMemoryValue}
                    minValue={-1}
                    step={1048576}
                    maxValue={user.machines.absoluteGraphicsMaxMemory}
                    label={'Memory'}
                    color={'#ffba7d'}
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
