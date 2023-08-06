/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Button, CircularProgress, SvgIcon } from '@material-ui/core';
import * as React from 'react';
import { InfoSkirt } from '../../components/InfoSkirt';
import { Tag } from '../../components/Tag';
import WarningPopup from '../../core/WarningPopup';
import { Global } from '../../Global';
import ExtraInfo from '../../utils/ExtraInfo';
import FormatUtils from '../../utils/FormatUtils';
import { App } from '../App';
import { OptumiMetadata } from '../OptumiMetadata';
import { User } from '../User';
import { Machine, NoMachine } from './Machine';

interface IProps {
    order: number;
    machine: Machine
}

interface IState {
    showNoRequirementsPopup: boolean;
    showNoFileUploadsPopup: boolean;
    showStartSessionPopup: boolean;
    waiting: boolean;
    spinning: boolean;
}

function ordinal(i: number) {
    var j = i % 10,
        k = i % 100;
    if (j == 1 && k != 11) {
        return i + "st";
    }
    if (j == 2 && k != 12) {
        return i + "nd";
    }
    if (j == 3 && k != 13) {
        return i + "rd";
    }
    return i + "th";
}

export class RecommendedMachineComponent extends React.Component<IProps, IState> {
    _isMounted = false

    constructor(props: IProps) {
        super(props);
        this.state = {
            waiting: false,
            spinning: false,
            showNoRequirementsPopup: false,
            showNoFileUploadsPopup: false,
            showStartSessionPopup: false,
        };
    }

    private handleLaunchClick = async () => {
		const current = Global.tracker.currentWidget;
		if (current != null) {
            this.setState({ waiting: true, spinning: false });
            setTimeout(() => this.checkAndSetState({ spinning: true }), 1000);
            const notebook: any = current.model.toJSON();
            // Clear any cell outputs and execution counts
            const optumi: OptumiMetadata = new OptumiMetadata(notebook["metadata"]["optumi"] || {});
            if (!optumi.interactive) {
                notebook.cells.unshift({
                    "cell_type": "code",
                    "source": "## Install Requirements",
                    "metadata": {},
                    });
                for (var cell of notebook.cells) {
                    cell.outputs = [];
                    cell.execution_count = null;
                }
            }
            // Save the notebook before transferring
            await current.context.save();
            const app = new App(current.context.path, notebook);
            app.setupNotebook(Global.user.appTracker).then(
                // on success or error, we stop waiting
                () => this.checkAndSetState({ waiting: false }),
                () => this.checkAndSetState({ waiting: false })
            );
		}
	}

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('MachineRender (' + new Date().getSeconds() + ')');
        var machine: Machine = this.props.machine
        var tags: JSX.Element[] = []
        // if (this.props.preview && machine == null) tags.push(new Tag({label: 'No Machine'})) // doesn't work
        var specialTag: JSX.Element[] = []
        if (machine.rate != undefined) specialTag.push(<Tag key={'machineRate' + machine.rate} label={(machine.promo ? 'Promo: ' : '') + FormatUtils.styleRateUnitValue()(machine.rate)} />);
        var machineState: string = Machine.getStateMessage(this.props.machine.state);
        if (machineState != '') tags.push(<Tag key={'machineState' + machineState} label={machineState} />)
        const user: User = Global.user;
        return (
            <InfoSkirt
                leftButton={
                    <ExtraInfo reminder='See details'>
                        {this.props.machine.getPopupComponent()}
                    </ExtraInfo>
                }
                rightButton={
                    this.props.order == 1 ? (
                        <>
                            <WarningPopup
                                open={this.state.showNoRequirementsPopup && this.state.showNoFileUploadsPopup}
                                headerText="Heads up!"
                                bodyText={`If your notebook imports packages or reads local data files, you'll want to add them under "Packages" and "Files".`}
                                preventText="Don't warn me again"
                                cancel={{
                                    text: `Cancel`,
                                    onCancel: (prevent: boolean) => {
                                        this.checkAndSetState({ showNoRequirementsPopup: false, showNoFileUploadsPopup: false })
                                    },
                                }}
                                continue={{
                                    text: `Launch it`,
                                    onContinue: (prevent: boolean) => {
                                        this.checkAndSetState({ showNoRequirementsPopup: false, showNoFileUploadsPopup: false })
                                        Global.user.noRequirementsPreventEnabled = prevent
                                        Global.user.noFileUploadsPreventEnabled = prevent
                                        this.handleLaunchClick()
                                    },
                                    color: `primary`,
                                }}
                            />
                            <WarningPopup
                                open={this.state.showNoRequirementsPopup && !this.state.showNoFileUploadsPopup}
                                headerText="Heads up!"
                                bodyText={`If your notebook imports packages, you'll want to add a requirements file under "Packages".`}
                                preventText="Don't warn me again"
                                cancel={{
                                    text: `Cancel`,
                                    onCancel: (prevent: boolean) => {
                                        this.checkAndSetState({ showNoRequirementsPopup: false })
                                    },
                                }}
                                continue={{
                                    text: `Launch it`,
                                    onContinue: (prevent: boolean) => {
                                        this.checkAndSetState({ showNoRequirementsPopup: false })
                                        Global.user.noRequirementsPreventEnabled = prevent
                                        this.handleLaunchClick()
                                    },
                                    color: `primary`,
                                }}
                            />
                            <WarningPopup
                                open={this.state.showNoFileUploadsPopup && !this.state.showNoRequirementsPopup}
                                headerText="Heads up!"
                                bodyText={`If your notebook reads local data files, you'll want to add them under "Files".`}
                                preventText="Don't warn me again"
                                cancel={{
                                    text: `Cancel`,
                                    onCancel: (prevent: boolean) => {
                                        this.checkAndSetState({ showNoFileUploadsPopup: false })
                                    },
                                }}
                                continue={{
                                    text: `Launch it`,
                                    onContinue: (prevent: boolean) => {
                                        this.checkAndSetState({ showNoFileUploadsPopup: false })
                                        Global.user.noFileUploadsPreventEnabled = prevent
                                        this.handleLaunchClick()
                                    },
                                    color: `primary`,
                                }}
                            />
                            <WarningPopup
                                open={this.state.showStartSessionPopup}
                                headerText="Heads up!"
                                bodyText={`You are about to launch a session which will remain active until you manually close it.`}
                                preventText="Don't warn me again"
                                cancel={{
                                    text: `Cancel`,
                                    onCancel: (prevent: boolean) => {
                                        this.checkAndSetState({ showStartSessionPopup: false })
                                    },
                                }}
                                continue={{
                                    text: `Launch it`,
                                    onContinue: (prevent: boolean) => {
                                        this.checkAndSetState({ showStartSessionPopup: false })
                                        Global.user.startSessionPreventEnabled = prevent
                                        this.handleLaunchClick()
                                    },
                                    color: `primary`,
                                }}
                            />
                            <ExtraInfo reminder='Launch'>
                                <Button
                                    variant='contained'
                                    color='primary'
                                    disabled={machine instanceof NoMachine || this.state.waiting || user.appTracker.getDisplayNum() >= Global.user.maxJobs }
                                    onClick={() => {
                                        const optumi = Global.metadata.getMetadata().metadata;
                                    const requirementsEmpty = optumi.upload.requirements == null || optumi.upload.requirements == "";
                                        const fileUploadsEmpty = optumi.upload.files.length == 0;
                                        const user = Global.user;
                                        if (optumi.interactive) {
                                            if (!user.startSessionPreventEnabled) {
                                                this.checkAndSetState({ showStartSessionPopup: true});
                                            } else {
                                                this.handleLaunchClick();
                                            }
                                        } else {
                                            if (requirementsEmpty && fileUploadsEmpty) {
                                                if (user.noRequirementsPreventEnabled && user.noFileUploadsPreventEnabled) {
                                                    this.handleLaunchClick();
                                                } else if (user.noRequirementsPreventEnabled) {
                                                    this.checkAndSetState({ showNoFileUploadsPopup: true});
                                                } else if (user.noFileUploadsPreventEnabled) {
                                                    this.checkAndSetState({ showNoRequirementsPopup: true});
                                                } else {
                                                    this.checkAndSetState({ showNoRequirementsPopup: true, showNoFileUploadsPopup: true});
                                                }
                                            } else if (requirementsEmpty) {
                                                if (user.noRequirementsPreventEnabled) {
                                                    this.handleLaunchClick();
                                                } else {
                                                    this.checkAndSetState({ showNoRequirementsPopup: true});
                                                }
                                            } else if (fileUploadsEmpty) {
                                                if (user.noFileUploadsPreventEnabled) {
                                                    this.handleLaunchClick();
                                                } else {
                                                    this.checkAndSetState({ showNoFileUploadsPopup: true});
                                                }
                                            } else {
                                                this.handleLaunchClick();
                                            }
                                        }
                                    }}
                                    style={{
                                        position: 'relative',
                                        minWidth: '0px',
                                        minHeight: '0px',
                                        width: '42px',
                                        height: '42px',
                                        borderRadius: '21px',
                                        color: 'var(--jp-layout-color2)',
                                    }}
                                >
                                    <SvgIcon viewBox="0, 0, 400,446" style={{position: 'relative', width: '30px', height: '30px'}}>
                                        <path d="M348.000 58.232 C 324.618 61.984,306.000 66.674,306.000 68.813 C 306.000 71.851,369.545 135.122,371.067 133.599 C 372.905 131.761,382.000 74.336,382.000 64.567 L 382.000 56.000 370.500 56.234 C 364.175 56.362,354.050 57.262,348.000 58.232 M261.029 86.235 C 214.374 111.539,184.827 137.455,151.438 182.354 C 131.859 208.683,134.247 207.280,105.973 209.077 C 77.646 210.877,78.107 210.586,46.111 246.944 C 14.709 282.628,13.657 285.006,24.595 295.608 C 33.914 304.640,38.535 303.841,62.774 289.000 C 74.453 281.850,85.356 276.000,87.004 276.000 C 90.397 276.000,91.021 279.133,88.000 281.000 C 80.966 285.347,86.211 293.260,115.524 322.525 C 145.290 352.241,154.153 357.842,159.000 350.000 C 161.093 346.613,163.948 347.791,162.638 351.500 C 161.957 353.425,155.685 364.580,148.700 376.288 C 133.629 401.551,133.207 405.011,144.006 414.767 C 155.049 424.744,153.659 425.401,190.701 392.696 C 227.821 359.922,227.156 360.976,229.004 332.000 C 230.748 304.673,229.916 306.203,252.454 288.864 C 308.578 245.687,341.585 206.858,361.005 161.165 C 368.325 143.941,367.373 141.488,347.134 125.396 C 330.680 112.314,319.724 100.874,305.577 82.000 C 295.803 68.959,292.260 69.296,261.029 86.235 M281.518 145.989 C 295.397 154.451,299.651 169.944,291.460 182.204 C 279.075 200.744,254.612 198.973,245.060 178.845 C 234.650 156.906,260.788 133.350,281.518 145.989 M65.116 318.984 C 41.834 327.278,33.655 343.820,22.828 404.507 C 19.046 425.702,19.740 429.180,26.337 422.099 C 32.573 415.406,48.022 408.969,72.496 402.867 C 109.336 393.683,120.097 382.787,119.904 354.869 L 119.808 341.000 116.404 347.823 C 111.679 357.294,105.398 361.342,88.000 366.125 C 79.750 368.394,70.975 371.564,68.500 373.171 C 63.012 376.734,63.005 376.424,68.070 354.701 C 73.737 330.396,81.234 320.000,93.094 320.000 C 94.692 320.000,96.000 319.100,96.000 318.000 C 96.000 315.041,74.239 315.734,65.116 318.984 " />
                                    </SvgIcon>
                                    {this.state.waiting && this.state.spinning && <CircularProgress size='42px' style={{position: 'absolute'}}/>}
                                </Button>
                            </ExtraInfo>
                        </>
                    ) : (
                        <div style={{
                            textAlign: 'center',
                            position: 'relative',
                            minWidth: '0px',
                            minHeight: '0px',
                            width: '42px',
                            height: '42px',
                        }}>
                            {ordinal(this.props.order) + ' choice'}
                        </div>
                    )
                }
                tags={tags}
                specialTag={specialTag}
            >
                {this.props.machine.getIdentityComponent()}
            </InfoSkirt>
        )
    }

    handleAppsChanged = () => this.forceUpdate();

	componentDidMount = () => {
		this._isMounted = true;
        Global.user.appTracker.appsChanged.connect(this.handleAppsChanged);
	}

	componentWillUnmount = () => {
        Global.user.appTracker.appsChanged.disconnect(this.handleAppsChanged);
		this._isMounted = false;
    }

    // This is only ever needed to set state after a promise
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
