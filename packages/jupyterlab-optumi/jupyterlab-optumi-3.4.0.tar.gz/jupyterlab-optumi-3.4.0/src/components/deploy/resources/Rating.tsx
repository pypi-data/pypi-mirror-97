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
import { ComputeRating } from './ComputeRating';
import { GraphicsRating } from './GraphicsRating';
import { MemoryRating } from './MemoryRating';
import { StorageRating } from './StorageRating';

interface IProps {
    style?: React.CSSProperties,
}

interface IState {}

export class Rating extends React.Component<IProps, IState> {
    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('RatingRender (' + new Date().getSeconds() + ')');
        return (
            <>
                <SubHeader title='Ability'/>
                <GraphicsRating />
                <ComputeRating />
                <MemoryRating />
                <StorageRating />
            </>
        )
    }

    // Will be called automatically when the component is mounted
    componentDidMount = () => {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        // Ser all resource levels to basic
        optumi.metadata.graphics.expertise = Expertise.RATING;
        optumi.metadata.compute.expertise = Expertise.RATING;
        optumi.metadata.memory.expertise = Expertise.RATING;
        optumi.metadata.storage.expertise = Expertise.RATING;
        tracker.setMetadata(optumi);
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
