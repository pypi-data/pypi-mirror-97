/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import {
	Tabs,
	Tab,
} from '@material-ui/core';

import { CSSProperties } from '@material-ui/core/styles/withStyles';
import withStyles from '@material-ui/core/styles/withStyles';

const StyledTab = withStyles({
    root: {
      minHeight: "24px",
      padding: "6px"
    }
  })(Tab);

export enum Page {
	RESOURCES = 0,
	FILES = 1,
}

interface IProps {
	style?: CSSProperties
}

// Properties for this component
interface IState {
    page: Page;
}

export class RequirementsBar extends React.Component<IProps, IState> {
	_isMounted = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
            page: Global.user.deploySubMenu || Page.RESOURCES,
        }
    }

	private handleTabChange = (event: React.ChangeEvent<{}>, newValue: Page) => {
        this.checkAndSetState({ page: newValue });
        Global.user.deploySubMenu = newValue;
	}

	render() {
		if (Global.shouldLogOnRender) console.log('RequirementsBarRender (' + new Date().getSeconds() + ')');
		return (
			<div style={{width: '100%', textAlign: 'center'}}>
				<Tabs 
                    value={this.state.page}
                    onChange={this.handleTabChange}
                    variant="fullWidth"
                    indicatorColor="primary"
                    textColor="primary"
                    style={{padding: "0px 6px 0px 6px", minHeight: "24px"}}
                >
					<StyledTab
                        label="RESOURCES"
                        style={{minWidth: "100px"}}
					/>
					<StyledTab
                        label="FILES"
                        style={{minWidth: "100px"}}
					/>
				</Tabs>
			</div>
		);
	}

	private handleCardChange = () => this.forceUpdate()

	// Will be called automatically when the component is mounted
	componentDidMount = () => {
		this._isMounted = true;
		Global.user.deploySubMenuChanged.connect(this.handleCardChange);
	}

	// Will be called automatically when the component is unmounted
	componentWillUnmount = () => {
		Global.user.deploySubMenuChanged.disconnect(this.handleCardChange);
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
