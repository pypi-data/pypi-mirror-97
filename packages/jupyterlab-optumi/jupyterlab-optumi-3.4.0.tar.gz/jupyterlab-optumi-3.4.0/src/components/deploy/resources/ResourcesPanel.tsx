/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../../Global';

import {
    Divider,
} from '@material-ui/core';

import { ResourceSelector } from './ResourceSelector';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';

import { GraphicsBasic } from './GraphicsBasic';
import { GraphicsRating } from './GraphicsRating';
import { GraphicsEquipment } from './GraphicsEquipment';
import { GraphicsComponent } from './GraphicsComponent';
import { ComputeBasic } from './ComputeBasic';
import { ComputeRating } from './ComputeRating';
import { ComputeComponent } from './ComputeComponent';
import { ComputeSimplified } from './ComputeSimplified';
import { MemoryBasic } from './MemoryBasic';
import { MemoryRating } from './MemoryRating';
import { MemoryComponent } from './MemoryComponent';
import { StorageBasic } from './StorageBasic';
import { StorageComponent } from './StorageComponent';
import { StorageRating } from './StorageRating';
import { StorageMetadata } from '../../../models/StorageMetadata';
import { Expertise } from '../../../models/OptumiMetadata';
import { ComputeMetadata } from '../../../models/ComputeMetadata';
import { GraphicsMetadata } from '../../../models/GraphicsMetadata';
import { MemoryMetadata } from '../../../models/MemoryMetadata';
import { Basic } from './Basic';

interface IProps {
    style?: React.CSSProperties,
}

interface IState {}

export class ResourcesPanel extends React.Component<IProps, IState> {

    private getGraphicsLevel(tracker: OptumiMetadataTracker): Expertise {
        const optumi = tracker.getMetadata();
        const graphics: GraphicsMetadata = optumi.metadata.graphics;
        return graphics.expertise;
    }

    private async saveGraphicsLevel(tracker: OptumiMetadataTracker, expertise: Expertise) {
        const optumi = tracker.getMetadata();
        const graphics: GraphicsMetadata = optumi.metadata.graphics;
        graphics.expertise = expertise;
        tracker.setMetadata(optumi);
    }

    private getComputeLevel(tracker: OptumiMetadataTracker): Expertise {
        const optumi = tracker.getMetadata();
        const compute: ComputeMetadata = optumi.metadata.compute;
        return compute.expertise;
    }

    private async saveComputeLevel(tracker: OptumiMetadataTracker, expertise: Expertise) {
        const optumi = tracker.getMetadata();
        const compute: ComputeMetadata = optumi.metadata.compute;
        compute.expertise = expertise;
        tracker.setMetadata(optumi);
    }

    private getMemoryLevel(tracker: OptumiMetadataTracker): Expertise {
        const optumi = tracker.getMetadata();
        const memory: MemoryMetadata = optumi.metadata.memory;
        return memory.expertise;
    }

    private async saveMemoryLevel(tracker: OptumiMetadataTracker, expertise: Expertise) {
        const optumi = tracker.getMetadata();
        const memory: MemoryMetadata = optumi.metadata.memory;
        memory.expertise = expertise;
        tracker.setMetadata(optumi);
    }

    private getStorageLevel(tracker: OptumiMetadataTracker): Expertise {
        const optumi = tracker.getMetadata();
        const storage: StorageMetadata = optumi.metadata.storage;
        return storage.expertise;
    }

    private async saveStorageLevel(tracker: OptumiMetadataTracker, expertise: Expertise) {
        const optumi = tracker.getMetadata();
        const storage: StorageMetadata = optumi.metadata.storage;
        storage.expertise = expertise;
        tracker.setMetadata(optumi);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ResourcesPanelRender (' + new Date().getSeconds() + ')');
        // For non-experimental users, we only need to look at one resource to decide what mode they are in
        // const basic: boolean = Global.metadata.getMetadata().metadata.graphics.expertise == Expertise.BASIC;
        return (
            <div style={this.props.style}>
                {Global.user.userExpertise >= 2 ? (
                    <>
                        <ResourceSelector title='GPU' getValue={this.getGraphicsLevel} saveValue={this.saveGraphicsLevel} childrenLabels={[Expertise.BASIC, Expertise.RATING, Expertise.EQUIPMENT, Expertise.COMPONENT]}>
                            <GraphicsBasic />
                            <GraphicsRating />
                            <GraphicsEquipment />
                            {Global.user.userExpertise >= 2 && <GraphicsComponent />}
                        </ResourceSelector>
                        <Divider variant='middle' />
                        <ResourceSelector title='CPU' getValue={this.getComputeLevel} saveValue={this.saveComputeLevel} childrenLabels={[Expertise.BASIC, Expertise.RATING, Expertise.SIMPLIFIED, Expertise.COMPONENT]}>
                            <ComputeBasic />
                            <ComputeRating />
                            {Global.user.userExpertise >= 2 && <ComputeSimplified />}
                            {Global.user.userExpertise >= 2 && <ComputeComponent />}
                        </ResourceSelector>
                        <Divider variant='middle' />
                        <ResourceSelector title='RAM' getValue={this.getMemoryLevel} saveValue={this.saveMemoryLevel} childrenLabels={[Expertise.BASIC, Expertise.RATING, Expertise.COMPONENT]}>
                            <MemoryBasic />
                            <MemoryRating />
                            {Global.user.userExpertise >= 2 && <MemoryComponent />}
                        </ResourceSelector>
                        <Divider variant='middle' />
                        <ResourceSelector title='DSK' getValue={this.getStorageLevel} saveValue={this.saveStorageLevel} childrenLabels={[Expertise.BASIC, Expertise.RATING, Expertise.COMPONENT]}>
                            <StorageBasic />
                            <StorageRating />
                            {Global.user.userExpertise >= 2 && <StorageComponent />}
                        </ResourceSelector>
                    </>
                ) : (
                    <>
                        <Basic />
                    </>
                )}
                
            </div>
        );
    }

    private handleMetadataChange = () => { this.forceUpdate() }

    // Will be called automatically when the component is mounted
	componentDidMount = () => {
        // This will cause the display to change when we change to a new notebook with a different level specified
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
