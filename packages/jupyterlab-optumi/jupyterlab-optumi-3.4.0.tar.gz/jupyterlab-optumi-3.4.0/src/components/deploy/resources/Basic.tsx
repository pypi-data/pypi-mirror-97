/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { SubHeader } from '../../../core';
import { Global } from '../../../Global';
import { Expertise } from '../../../models/OptumiMetadata';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import ExtraInfo from '../../../utils/ExtraInfo';

import { OutlinedResourceRadio } from '../OutlinedResourceRadio';

interface IProps {
    style?: React.CSSProperties,
}

interface IState {}

export class Basic extends React.Component<IProps, IState> {

    private getValue(): string {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
		if (optumi.metadata.graphics.required == true) return "GPU";
        if (optumi.metadata.compute.required == true) return "CPU";
        if (optumi.metadata.memory.required == true) return "RAM";
        if (optumi.metadata.storage.required == true) return "DSK";
        return "CPU";
	}

	private saveValue(value: string) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        optumi.metadata.graphics.required = value == "GPU" ? true : false;
        optumi.metadata.compute.required = value == "CPU" ? true : false;
        optumi.metadata.memory.required = value == "RAM" ? true : false;
        optumi.metadata.storage.required = value == "DSK" ? true : false;
        tracker.setMetadata(optumi);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('BasicRender (' + new Date().getSeconds() + ')');
        const value = this.getValue();
        return (
            <>
                <SubHeader title='Resource Emphasis'/>
                <div
                    style={{
                        alignItems: 'center',
                    }}
                >
                    <ExtraInfo reminder='Optimize for GPU'>
                        <OutlinedResourceRadio label={"GPU"} hexColor={'#ffba7d'} selected={value == "GPU"} handleClick={() => this.saveValue("GPU")}/>
                    </ExtraInfo>
                    <ExtraInfo reminder='Optimize for CPU'>
                        <OutlinedResourceRadio label={"CPU"} hexColor={'#f48f8d'} selected={value == "CPU"} handleClick={() => this.saveValue("CPU")}/>
                    </ExtraInfo>
                    <ExtraInfo reminder='Optimize for RAM'>
                        <OutlinedResourceRadio label={"RAM"} hexColor={'#afaab0'} selected={value == "RAM"} handleClick={() => this.saveValue("RAM")}/>
                    </ExtraInfo>
                </div>
            </>
        )
    }

    private handleMetadataChange = () => { this.forceUpdate() }

    // Will be called automatically when the component is mounted
	componentDidMount = () => {
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);

        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        // Ser all resource levels to basic
        optumi.metadata.graphics.expertise = Expertise.BASIC;
        optumi.metadata.compute.expertise = Expertise.BASIC;
        optumi.metadata.memory.expertise = Expertise.BASIC;
        optumi.metadata.storage.expertise = Expertise.BASIC;
        // Make sure only one required flag is set to true
        if (optumi.metadata.graphics.required) {
            optumi.metadata.compute.required = false;
            optumi.metadata.memory.required = false;
            optumi.metadata.storage.required = false
        } else if (optumi.metadata.compute.required) {
            optumi.metadata.graphics.required = false;
            optumi.metadata.memory.required = false;
            optumi.metadata.storage.required = false
        } else if (optumi.metadata.memory.required) {
            optumi.metadata.graphics.required = false;
            optumi.metadata.compute.required = false;
            optumi.metadata.storage.required = false
        } else {    // By default we will set compute to required
            optumi.metadata.graphics.required = false;
            optumi.metadata.compute.required = true;
            optumi.metadata.memory.required = false;
            optumi.metadata.storage.required = false
        }
        tracker.setMetadata(optumi);
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
