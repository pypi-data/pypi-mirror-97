/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';
import { Slider, withStyles, darken, lighten } from '@material-ui/core';
import { Eco, Equalizer, FlashOn } from '@material-ui/icons';
import { SubHeader } from './Header';

interface IProps {
    getValue: () => number
    saveValue: (value: number) => void
    color: string
    style?: React.CSSProperties
}

interface IState {
    value: number,
}

let retrievingPreview: boolean = false;
let updatePreviewAgain: boolean = false;
let latestValue: number;

const icons = [
    <Eco style={{fill: 'var(--jp-layout-color2)'}} />,
    <Equalizer style={{fill: 'var(--jp-layout-color2)'}} />,
    <FlashOn style={{fill: 'var(--jp-layout-color2)'}} />
]

export class IntentSlider extends React.Component<IProps, IState> {
    private _isMounted = false;

    private StyledSlider: any;
    private isLightMode: boolean = false;

    public constructor(props: IProps) {
        super (props);
        this.StyledSlider = this.getStyledSlider();
        this.state = {
            value: this.props.getValue(),
        }
    }

    private getStyledSlider = () => {
        this.isLightMode = Global.themeManager == undefined || Global.themeManager.isLight(Global.themeManager.theme)
        return withStyles({
            root: {
                height: '16px',
                width: '100%',
                padding: '13px 0px',
            },
            thumb: { // hidden
                position: 'relative',
                height: '42px',
                width: '42px', // So we show the label any time the slider is hovered
                margin: '-13px -21px',
                transition: 'none',
                backgroundColor: this.props.color,
                padding: '0px',
                zIndex: 2,          // Draw the thumb over the custom marks we put in the bar
                '&$focusVisible,&:hover': {
                    boxShadow: 'none',
                },
                '&$active': {
                    boxShadow: 'none',
                },
                '&::after': {
                    left: 0,
                    top: 0,
                    right: 0,
                    bottom: 0,
                },
            },
            thumbColorPrimary: {
                '&$focusVisible,&:hover': {
                    boxShadow: 'none',
                },
                '&$active': {
                    boxShadow: 'none',
                },
            },
            active: {
                boxShadow: 'none',
            },
            track: { // left side
                height: '16px',
                color: this.props.color,
                opacity: 0,
                boxSizing: 'border-box',
                border: "1px solid " + darken(this.props.color, 0.25),
                borderRadius: '8px',
            },
            rail: { // right side
                height: '16px',
                width: '100%',
                opacity: 1,
                color: (this.isLightMode ? '#eeeeee' : '#424242'),
                boxSizing: 'border-box',
                border: '1px solid ' + (this.isLightMode ? darken('#eeeeee', 0.25) : lighten('#424242', 0.25)),
                borderRadius: '8px',
            },
            mark: {
                opacity: 0,
            },
            markActive: {
                opacity: 0,
            },
            markLabel: {
            },
            markLabelActive: {
            },
        }) (Slider);
    }

    private handleChange = async (event: React.ChangeEvent<{}>, newValue: number | number[]) => {
		if (newValue instanceof Array) {
			// This is invalid
		} else {
            this.checkAndSetState({ value: newValue / 100 });
            this.slowDownSaveValue(newValue / 100);
        }
    }

    private handleChangeCommitted = async (event: React.ChangeEvent<{}>, newValue: number | number[]) => {
		if (newValue instanceof Array) {
			// This is invalid
		} else {
            this.checkAndSetState({ value: newValue / 100 });
            this.props.saveValue(newValue / 100);
        }
    }

    private delay = (ms: number) => { return new Promise(resolve => setTimeout(resolve, ms)) }
    private slowDownSaveValue = (newValue: number, bypassLimiter?: boolean) => {
        if (newValue != null) latestValue = newValue;
        if (bypassLimiter || !retrievingPreview) {
            retrievingPreview = true;
            this.delay(100).then(() => {
                this.props.saveValue(latestValue);
                if (updatePreviewAgain) {
                    updatePreviewAgain = false;
                    this.slowDownSaveValue(null, true);
                } else {
                    retrievingPreview = false;
                }
            }, () => {
                retrievingPreview = false;
            });
        } else {
            updatePreviewAgain = true;
        }
	}

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('IntentSliderRender (' + new Date().getSeconds() + ')');
        const icon = this.state.value < 0.33 ? 0 : this.state.value < 0.66 ? 1 : 2
        return (
            <div style={this.props.style}>
                <SubHeader title='Resource Tradeoff'/>
                <div style={{position: 'relative', margin: '0px 6px'}}>
                    <this.StyledSlider
                        // style={{position: 'relative'}}
                        onChange={this.handleChange}
                        onChangeCommitted={this.handleChangeCommitted}
                        min={0}
                        max={100}
                        value={this.state.value * 100}
                        ThumbComponent={(props: any) => (
                            <span style={{transform: 'translate(' + (50 - (100 * this.state.value)) + '%, 0px)', left: this.state.value + '%'}} {...props}>
                                {icons[icon]}
                            </span>
                        )}
                    />
                    <div style={{
                            position: 'absolute', 
                            zIndex: 1,
                            top: 'calc(50% - 8px)', 
                            left: '10px', 
                            color: (this.isLightMode ? '#424242' : '#eeeeee'), 
                            fontSize: '12px',
                            opacity: this.state.value < 0.37 ? 0 : 1,
                            transition: 'opacity 250ms ease 0s',
                            fontStyle: 'italic',
                            height: '0px', overflow: 'visible', pointerEvents: 'none' // Pass click events to the slider behind
                        }}
                    >
                        {'< Cheaper'}
                    </div>
                    <div style={{
                            position: 'absolute',
                            zIndex: 1,
                            top: 'calc(50% - 8px)', 
                            right: '10px', 
                            color: (this.isLightMode ? '#424242' : '#eeeeee'), 
                            fontSize: '12px',
                            opacity: this.state.value > 0.7 ? 0 : 1,
                            transition: 'opacity 250ms ease 0s',
                            fontStyle: 'italic',
                            height: '0px', overflow: 'visible', pointerEvents: 'none' // Pass click events to the slider behind    
                        }}
                    >
                        {'Faster >'}
                    </div>
                </div>
            </div>
        )
    }

    private handleMetadataChange = () => this.checkAndSetState({ value: this.props.getValue(), weGotADot: '' })
    private handleThemeChange = () => {
        this.StyledSlider = this.getStyledSlider();
        if (this._isMounted) this.forceUpdate();
    }

    // Will be called automatically when the component is mounted
	componentDidMount = () => {
		this._isMounted = true;
        Global.metadata.getMetadataChanged().connect(this.handleMetadataChange);
        Global.themeManager.themeChanged.connect(this.handleThemeChange);
	}

	// Will be called automatically when the component is unmounted
	componentWillUnmount = () => {
		Global.metadata.getMetadataChanged().disconnect(this.handleMetadataChange);
        Global.themeManager.themeChanged.disconnect(this.handleThemeChange);
		this._isMounted = false;
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

    private checkAndSetState = (map: any) => {
		if (this._isMounted) {
			this.setState(map);
		}
	}
}
