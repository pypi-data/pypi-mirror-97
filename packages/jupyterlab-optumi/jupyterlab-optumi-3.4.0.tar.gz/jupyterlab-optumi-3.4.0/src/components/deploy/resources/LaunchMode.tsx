/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { SubHeader } from '../../../core';
import { Global } from '../../../Global';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import ExtraInfo from '../../../utils/ExtraInfo';

import { OutlinedResourceRadio } from '../OutlinedResourceRadio';

interface IProps {
    style?: React.CSSProperties,
}

interface IState {}

export class LaunchMode extends React.Component<IProps, IState> {

    private getValue(): string {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        return optumi.metadata.interactive ? "Session" : "Job";
	}

	private saveValue(value: string) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        optumi.metadata.interactive = value == "Session" ? true : false;
        tracker.setMetadata(optumi);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ComputeBasicRender (' + new Date().getSeconds() + ')');
        const value = this.getValue();
        return (
            <>
                <SubHeader title='Launch Mode'/>
                <div
                    style={{
                        alignItems: 'center',
                        display: 'inline-flex',
                        width: '100%',
                    }}
                >
                    <ExtraInfo reminder='Run an interactive session'>
                        <OutlinedResourceRadio beta label={'Session'} hexColor={'#afaab0'} selected={value == "Session"} handleClick={() => this.saveValue("Session")}/>
                    </ExtraInfo>
                    <ExtraInfo reminder='Run a batch job'>
                        <OutlinedResourceRadio label={"Job"} hexColor={'#afaab0'} selected={value == "Job"} handleClick={() => this.saveValue("Job")}/>
                    </ExtraInfo>
                </div>
            </>
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
