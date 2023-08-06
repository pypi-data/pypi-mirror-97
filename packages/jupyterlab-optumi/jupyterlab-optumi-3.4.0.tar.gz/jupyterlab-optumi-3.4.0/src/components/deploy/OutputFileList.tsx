/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import { App } from '../../models/App';
import { OutputFileEntry } from './OutputFileEntry';

import {
	List,
} from '@material-ui/core';
import { getStyledSwitch } from '../../core/Switch';
import ExtraInfo from '../../utils/ExtraInfo';

interface IProps {
	app: App;
}

// Properties for this component
interface IState {
	overwrite: boolean
}

const StyledSwitch = getStyledSwitch();

export class OutputFileList extends React.Component<IProps, IState> {
	_isMounted = false;

	constructor(props: IProps) {
		super(props);
		this.state = {
			overwrite: false
		};
	}

	private getFiles() {
		var files: any[] = [];
		for (let module of this.props.app.modules) {
            if (module.files) {
                for (let file of module.files) {
                    files.push({
                        "file": file.path,
						"lastModified": file.lastModified,
						"size": file.size,
                        "moduleUUID": module.uuid,
                    });
                }
            }
		} 
		if (!this.props.app.running.started) {
			return (
				<div>
					Files will appear here when the job starts.
				</div>
			)
		} else {
			var sorted: any[] = files.sort((n1,n2) => {
				if (n1.file > n2.file) {
					return 1;
				}
				if (n1.file < n2.file) {
					return -1;
				}
				return 0;
			});
			return (
				<div>
                    <div style={{display: 'inline-flex', alignItems: 'center'}}>
                        <div style={{paddingLeft: '16px', paddingRight: '16px'}}>
                            <ExtraInfo reminder='Overwrite existing files with downloaded files, or rename the downloaded files'>
								<StyledSwitch
									color='primary'
									inputProps={{style: {height: '24px'}}}
									checked={this.state.overwrite}
									onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
										this.checkAndSetState({overwrite: event.currentTarget.checked})
									}}
								/>
							</ExtraInfo>
                       </div>
                        Overwrite existing files
                    </div>
                    <List>
						{sorted.map((value: any) => 
							React.cloneElement((
								<OutputFileEntry
                                    name={value.file}
									lastModified={value.lastModified}
									size={value.size}
                                    files={[value.file]}
									workloadUUID={this.props.app.uuid}
									moduleUUID={value.moduleUUID}
                                    disabled={false}
                                    overwrite={this.state.overwrite}
								/>
							), { key: value.file })
						)}
                        {this.props.app.interactive && <OutputFileEntry
                            name={'Download stdout as file'}
							lastModified=""
							size={0}
                            files={[this.props.app.name.replace('.ipynb', '.stdout')]}
                            workloadUUID={this.props.app.uuid}
                            moduleUUID={this.props.app.modules[0].uuid}
                            disabled={false}
							overwrite={this.state.overwrite}
							
                        />}
                        {this.props.app.interactive && <OutputFileEntry
                            name={'Download stderr as file'}
							lastModified=""
							size={0}
                            files={[this.props.app.name.replace('.ipynb', '.stderr')]}
                            workloadUUID={this.props.app.uuid}
                            moduleUUID={this.props.app.modules[0].uuid}
                            disabled={false}
                            overwrite={this.state.overwrite}
                        />}
						<OutputFileEntry
							name={'Download all files'}
							size={sorted.length == 0 ? 0 : sorted.reduce((a, b) => { return { size: a.size + b.size } }, {size: 0}).size}
							lastModified=""
							files={sorted.map((value: any) => value.file).concat(this.props.app.interactive ? [this.props.app.name.replace('.ipynb', '.stderr'), this.props.app.name.replace('.ipynb', '.stdout')] : [])}
							workloadUUID={this.props.app.uuid}
							moduleUUID={this.props.app.modules[0].uuid}
							disabled={!this.props.app.interactive && sorted.length == 0}
							overwrite={this.state.overwrite}
						/>
					</List>
				</div>
			)
		}
	}

	render() {
		if (Global.shouldLogOnRender) console.log('OutputFileListRender (' + new Date().getSeconds() + ')');
		return (
			<div style={{padding: '12px', width: "100%"}}>
				{this.getFiles()}
			</div>
		);
	}

	// Will be called automatically when the component is mounted
	componentDidMount = () => {
		this._isMounted = true;
	}

	// Will be called automatically when the component is unmounted
	componentWillUnmount = () => {
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
