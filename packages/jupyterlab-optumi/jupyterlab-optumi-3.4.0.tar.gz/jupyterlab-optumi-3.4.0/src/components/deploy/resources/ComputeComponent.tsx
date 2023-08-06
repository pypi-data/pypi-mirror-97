/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../../Global';

import { ComputeMetadata } from '../../../models/ComputeMetadata';
import { User } from '../../../models/User';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import { Slider } from '../../../core';
import FormatUtils from '../../../utils/FormatUtils';

interface IProps {
    style?: React.CSSProperties,
}

interface IState {}

export class ComputeComponent extends React.Component<IProps, IState> {

    private getCoresValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
		const compute: ComputeMetadata = optumi.metadata.compute;
		return compute.cores[1];
	}

	private async saveCoresValue(cores: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
		const compute: ComputeMetadata = optumi.metadata.compute;
        compute.cores = [-1, cores, -1];
		tracker.setMetadata(optumi);
    }
    
    private getScoreValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
		const compute: ComputeMetadata = optumi.metadata.compute;
		return compute.score[1];
	}

	private async saveScoreValue(score: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
		const compute: ComputeMetadata = optumi.metadata.compute;
        compute.score = [-1, score, -1];
		tracker.setMetadata(optumi);
	}

    private getFrequencyValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
		const compute: ComputeMetadata = optumi.metadata.compute;
		return compute.frequency[1];
	}

	private async saveFrequencyValue(frequency: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
		const compute: ComputeMetadata = optumi.metadata.compute;
        compute.frequency = [-1, frequency, -1];
		tracker.setMetadata(optumi);
	}

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComputeComponentRender (' + new Date().getSeconds() + ')');
        var user: User = Global.user;
        return (
            <div style={this.props.style}>
                <Slider
                    getValue={this.getCoresValue}
                    saveValue={this.saveCoresValue}
                    minValue={-1}
                    maxValue={user.machines.absoluteComputeMaxCores}
                    label={'Cores'}
                    color={'#f48f8d'}
                    showUnit
                />
                <Slider
                    getValue={this.getScoreValue}
                    saveValue={this.saveScoreValue}
                    minValue={-1}
                    maxValue={user.machines.absoluteComputeMaxScore}
                    label={'Score'}
                    color={'#f48f8d'}
                    showUnit
                />
                <Slider
                    getValue={this.getFrequencyValue}
                    saveValue={this.saveFrequencyValue}
                    minValue={-1}
                    step={1000000}
                    maxValue={user.machines.absoluteComputeMaxFrequency}
                    label={'Frequency'}
                    color={'#f48f8d'}
                    showUnit
                    styledUnit={FormatUtils.styleFrequencyUnit()}
                    styledValue={FormatUtils.styleFrequencyValue()}
                    unstyledValue={FormatUtils.unstyleFrequencyValue()}
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