/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Switch } from '../../../core';
import { Global } from '../../../Global';
import { MemoryMetadata } from '../../../models/MemoryMetadata';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';

interface IProps {
    style?: React.CSSProperties,
}

interface IState {}

export class MemoryBasic extends React.Component<IProps, IState> {
    
    private getValue(): boolean {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
		const memory: MemoryMetadata = optumi.metadata.memory;
		return memory.required;
	}

	private async saveValue(checked: boolean) {
        const tracker: OptumiMetadataTracker = Global.metadata;
		const optumi = tracker.getMetadata();
        const memory: MemoryMetadata = optumi.metadata.memory;
        memory.required = checked;
        tracker.setMetadata(optumi);
	}

    handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const checked = event.target.checked;
        this.saveValue(checked);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('MemoryBasicRender (' + new Date().getSeconds() + ')');
        return (
            <div style={this.props.style}>
                <Switch
                    label='Required'
                    flip
                    getValue={this.getValue}
                    saveValue={this.saveValue}
                />
            </div>
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