/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../../Global';

import {
    IconButton
} from '@material-ui/core';

import ChevronLeft from '@material-ui/icons/ChevronLeft';
import ChevronRight from '@material-ui/icons/ChevronRight';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';
import { Expertise } from '../../../models/OptumiMetadata';

interface IProps {
    getValue: (tracker: OptumiMetadataTracker) => Expertise
    saveValue: (tracker: OptumiMetadataTracker, value: Expertise) => void
    style?: React.CSSProperties
    title: string,
    children: JSX.Element[] | JSX.Element,
    childrenLabels: Expertise[]
}

interface IState {
    currentLevel: number
}

export class ResourceSelector extends React.Component<IProps, IState> {
    _isMounted = false;

    public constructor(props: IProps) {
        super (props);
        this.state = {
            currentLevel: this.props.childrenLabels.indexOf(this.props.getValue(Global.metadata)),
        };
    }

    // This had to be written because ResourcePanel complained that a single element
    // was not an array, so we had to accept both and handle internally
    private getChildren = (): JSX.Element[] => {
        var children: JSX.Element[] | JSX.Element = this.props.children;
        if (children instanceof Array) {
			// The filter below allows us to remove levels conditionally (if they aren't added they evaluate as false)
            return children.filter(child => React.isValidElement(child));
        } else {
            var singleton: JSX.Element[] = [];
            singleton.push(children);
            return singleton;
        }
    }

    private decreaseExpertise = (): void => {
        const newLevel = this.state.currentLevel - 1;
        if (this.state.currentLevel > 0) {
            this.checkAndSetState({ currentLevel: newLevel });
        }
        this.props.saveValue(Global.metadata, this.props.childrenLabels[newLevel] as Expertise);
    }

    private increaseExpertise = (): void => {
        const newLevel = this.state.currentLevel + 1;
        if (this.state.currentLevel < this.getChildren().length - 1) {
            this.checkAndSetState({ currentLevel: newLevel})
        }
        this.props.saveValue(Global.metadata, this.props.childrenLabels[newLevel]);
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ResourceSelectorRender (' + new Date().getSeconds() + ')');
        this.props.children;
        // The padding is not in the div because the padding affects the ability to click the chevrons
        // The position and left/right on the icons is so all chevrons are aligned vertically no matter the size of the text
        // The title is in an inline-block div because we want the chevrons around the title and they use position: absolute
        // The lineHeight in the title centers the text vertically (24px comes from the chevron height from the inspector)
        return (
            <div style={this.props.style}>
                <div style={{textAlign: 'center', margin: '6px'}}>
                    <div style={{position: 'relative', textAlign: 'center'}}>
                        <IconButton
                            disabled={this.state.currentLevel <= 0 ? true : false}
                            color='primary'
                            onClick={() => this.decreaseExpertise()}
                            style={{position: 'absolute', left: '25%', padding: '3px'}}
                        >
                            <ChevronLeft />
                        </IconButton>
                        <div style={{display: 'inline-block', fontSize: '16px', fontWeight: 'bold', lineHeight: '18px', margin: '6px'}}>
                            {this.props.title}
                        </div>
                        <IconButton
                            disabled={this.state.currentLevel >= this.getChildren().length - 1 ? true : false}
                            color='primary'
                            onClick={() => this.increaseExpertise()}
                            style={{position: 'absolute', right: '25%', padding: '3px'}}
                        >
                            <ChevronRight />
                        </IconButton>
                    </div>
                    {this.getChildren()[this.state.currentLevel]}
                </div>
            </div>
        );
    }

    private handleMetadataChange = () => {
        this.checkAndSetState({ currentLevel: this.props.childrenLabels.indexOf(this.props.getValue(Global.metadata)) });
    }

    // Will be called automatically when the component is mounted
	componentDidMount = () => {
		this._isMounted = true;
		Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
	}

	// Will be called automatically when the component is unmounted
	componentWillUnmount = () => {
		Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
		this._isMounted = false;
	}

	private checkAndSetState = (map: any) => {
		if (this._isMounted) {
			this.setState(map);
		}
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
