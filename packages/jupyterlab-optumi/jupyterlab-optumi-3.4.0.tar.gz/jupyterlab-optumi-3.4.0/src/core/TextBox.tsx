/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../Global';
import withStyles, { CSSProperties } from '@material-ui/core/styles/withStyles';
import { Button, OutlinedInput, FormControl, InputLabel, InputAdornment, IconButton, FormHelperText } from '@material-ui/core';
import CloseIcon from '@material-ui/icons/Close';
import DoneIcon from '@material-ui/icons/Done';
import VisibilityIcon from '@material-ui/icons/Visibility';
import VisibilityOffIcon from '@material-ui/icons/VisibilityOff';
import LockIcon from '@material-ui/icons/Lock';
import ExtraInfo from '../utils/ExtraInfo';

interface IProps<T> {
    style?: CSSProperties
    label?: string
    labelWidth?: string
    getValue: () => T
    saveValue: (value: T) => string | void
    editPressRequired?: boolean
    editPopup?: JSX.Element
    disabled?: boolean
    disabledMessage?: string
    password?: boolean
    placeholder?: string
    styledUnitValue?: (value: T) => string
    unstyleUnitValue?: (value: string) => T
    minValue?: T
    maxValue?: T
    helperText?: string
    onFocus?: (event: React.FocusEvent<HTMLInputElement>) => void
    onBlur?: (event: React.FocusEvent<HTMLInputElement>) => void
    multiline?: boolean
    minLines?: number
    required?: boolean
}

interface IState<T> {
    value: T
    textValue: string
    editing: boolean
    invalidTextMessage: string
    hovered: boolean
    hidePassword: boolean
}

export class TextBox<T> extends React.Component<IProps<T>, IState<T>> {
    StyledOutlinedInput: any
    StyledInputLabel: any;
    textField: React.RefObject<HTMLInputElement>

    static defaultProps: Partial<IProps<any>> = {
        styledUnitValue: (value: any) => { return value.toString() },
    }

    constructor(props: IProps<T>) {
        super(props);
        this.StyledOutlinedInput = this.getStyledOutlinedInput();
        this.StyledInputLabel = this.getStyledInputLabel();
        this.textField = React.createRef();
        const value: any = this.props.getValue();
        this.state = {
            value: value,
            textValue: this.props.styledUnitValue(value),
            editing: false,
            hovered: false,
            invalidTextMessage: '',
            hidePassword: true,
        }
    }

    private getStyledOutlinedInput = () => {
        return withStyles({
            root: {
                padding: '0px',
            },
            input: {
                fontSize: '12px',
                padding: '3px 6px 3px 6px',
            },
            adornedEnd: {
                paddingRight: '0px',
            },
        }) (OutlinedInput);
    }

    private getStyledInputLabel = () => {
        return withStyles({
            root: {
                fontSize: '12px',
                backgroundColor: 'var(--jp-layout-color1)',
                padding: '1px 2px',
            },
            outlined: {
                transform: 'translate(6px, 6px) scale(1)',
                '&$shrink': {
                    transform: 'translate(9px, -6px) scale(0.8)',
                }
            },
            formControl: {
                transform: 'translate(6px, 6px) scale(1)',
            },
            shrink: {
                transform: 'translate(9px, -6px) scale(0.8)',
            },
        }) (InputLabel);
    }

    // This turns the textbox red if it is not a valid value determined by the unstyle function
    private handleChange = async (event: React.FormEvent<HTMLInputElement>) => {
        const value = event.currentTarget.value
        this.setState({ textValue: value });
        if (this.props.unstyleUnitValue == undefined) {
            if (typeof value === 'number') {
                if (this.props.minValue !== undefined && value < this.props.minValue) {
                    this.setState({ invalidTextMessage: 'Minimum value is ' + this.props.styledUnitValue(this.props.minValue) })
                } else if (this.props.maxValue !== undefined && value > this.props.maxValue) {
                    this.setState({ invalidTextMessage: 'Maximum value is ' + this.props.styledUnitValue(this.props.maxValue) })
                } else {
                    if (!this.props.editPressRequired) this.setState({ value: value as unknown as T, invalidTextMessage: '' });
                }
            } else {
                if (!this.props.editPressRequired) this.setState({ value: value as unknown as T, invalidTextMessage: '' });
            }
        } else {
            var unstyledValue: any = this.props.unstyleUnitValue(value);
            if (!isNaN(unstyledValue)) {
                if (this.props.minValue !== undefined && unstyledValue < this.props.minValue) {
                    this.setState({ invalidTextMessage: 'Minimum value is ' + this.props.styledUnitValue(this.props.minValue) })
                } else if (this.props.maxValue !== undefined && unstyledValue > this.props.maxValue) {
                    this.setState({ invalidTextMessage: 'Maximum value is ' + this.props.styledUnitValue(this.props.maxValue) })
                } else {
                    if (!this.props.editPressRequired) this.setState({ value: unstyledValue as unknown as T, invalidTextMessage: '' });
                }
            } else {
                this.setState({ invalidTextMessage: 'Invalid format' })
            }
        }
    }

    private startEdit = () => {
        this.setState({editing: true})
        this.textField.current.disabled = false
        this.textField.current.focus()
    }

    private discardChanges = () => {
        this.setState({
            editing: false,
            textValue: this.props.styledUnitValue(this.state.value),
            invalidTextMessage: '',
        })
    }

    // If save clicked, or if unfocused if save not required. Saves value if it is a valid value determined by the unstyle function or lack thereof
    private saveChanges = () => {
        var invalidTextMessage: string = '';
        var unstyledValue: any = this.state.textValue;
        if (this.props.unstyleUnitValue != undefined) {
            unstyledValue = this.props.unstyleUnitValue(this.state.textValue);
            if (isNaN(unstyledValue)) {
                invalidTextMessage = 'Invalid format'
            } else if (this.props.minValue !== undefined && unstyledValue < this.props.minValue) {
                invalidTextMessage = 'Minimum value is ' + this.props.styledUnitValue(this.props.minValue)
            } else if (this.props.maxValue !== undefined && unstyledValue > this.props.maxValue) {
                invalidTextMessage = 'Maximum value is ' + this.props.styledUnitValue(this.props.maxValue)
            }
        }
        this.setState({invalidTextMessage: invalidTextMessage});
        if (invalidTextMessage == '') {
            this.setState({editing: false, value: unstyledValue, textValue: this.props.styledUnitValue(unstyledValue)})
            var saveReturn = this.props.saveValue(unstyledValue)
            this.setState({invalidTextMessage: saveReturn == undefined ? '' : saveReturn as string})
        }
    }

    private startHover = () => {
        this.setState({hovered: true})
    }

    private stopHover = () => {
        this.setState({hovered: false})
    }

    private renderPopupButton = (render: boolean): JSX.Element => {
        return this.props.editPopup !== undefined ? React.cloneElement(this.props.editPopup, {
            style: {
                display: render ? 'flex' : 'none',
            },
            onOpen: () => {
                this.setState({editing: true})
            },
            onClose: () => {
                this.setState({hovered: false, editing: false})
            }
        }) : <></>
    }

    private renderEditButton = (render: boolean): JSX.Element => {
        return (
            <Button
                onClick={this.startEdit}
                style={{
                    display: render ? 'flex' : 'none',
                    width: '100%',
                    minWidth: '0px',
                    paddingTop: '6px',
                }}
                variant="outlined"
            >
                Edit
            </Button>
        )
    }

    private renderConfirmCancelButtons = (render: boolean): JSX.Element => {
        return (
            <>
                <Button
                    onClick={this.discardChanges}
                    variant="outlined"
                    color="primary"
                    style={{
                        display: render ? 'flex' : 'none',
                        width: '50%',
                        minWidth: '0px',
                        paddingTop: '6px',
                        borderTopRightRadius: '0px',
                        borderBottomRightRadius: '0px',
                        borderRight: '0px',
                    }}
                >
                    <CloseIcon style={{width: '20px', height: '20px'}} />
                </Button>
                <Button
                    onClick={this.saveChanges}
                    variant="outlined"
                    color="primary"
                    style={{
                        display: render ? 'flex' : 'none',
                        width: '50%',
                        minWidth: '0px',
                        paddingTop: '6px',
                        borderTopLeftRadius: '0px',
                        borderBottomLeftRadius: '0px',
                    }}
                >
                    <DoneIcon style={{width: '20px', height: '20px'}} />
                </Button>
            </>
        )
    }

    private renderLabelOverButton = (render: boolean): JSX.Element => {
        return (
            <this.StyledInputLabel shrink={true} style={{display: render ? 'flex' : 'none', position: 'absolute'}}>
                {this.props.label}
            </this.StyledInputLabel>
        )
    }

    private renderLabel = (render: boolean): JSX.Element => {
        return (
            <span style={{display: render ? 'inline' : 'none', width: '100%', color: !(this.props.disabledMessage == undefined || this.props.disabledMessage == '') ? 'var(--jp-ui-font-color3)' : 'var(--jp-ui-font-color1)'}}>
                {this.props.label + (this.props.required ? '*' : '')}
            </span>
        )
    }

    private handleFocus = (event: React.FocusEvent<HTMLInputElement>) => {
        if (this.props.onFocus) {
            this.props.onFocus(event)
        }
    }

    private handleBlur = (event: React.FocusEvent<HTMLInputElement>) => {
        if (this.props.onBlur) {
            this.props.onBlur(event)
        }
        if (!(this.props.editPressRequired || this.props.editPopup !== undefined)) {
            this.saveChanges()
        }
    }
    
    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('ResourceTextBoxRender (' + new Date().getSeconds() + ')');
        var showPopupButton = false, showEditButton = false, showConfirmCancelButtons = false, showLabel = false
        // There should never be an if without an else. That could lead to nothing being rendered to the left of the textbox
        if (this.props.editPopup === undefined && !this.props.editPressRequired) {
            showLabel = true
        } else if (!this.state.hovered && !this.state.editing) {
            showLabel = true
        } else {
            if (this.props.editPopup !== undefined) {
                showPopupButton = true
            } else {
                if (this.state.editing) {
                    showConfirmCancelButtons = true
                } else {
                    showEditButton = true
                }
            }
        }
        return (
            <div
                style={Object.assign({display: 'inline-flex', width: '100%', padding: '6px 0px'}, this.props.style)}
                onMouseOver={this.startHover}
                onMouseOut={this.stopHover}
            >
                {this.props.label && (
                    <div style={{
                        display: 'flex',
                        position: 'relative',
                        minWidth: this.props.labelWidth || '68px',
                        maxWidth: this.props.labelWidth || '68px',
                        height: '24px',
                        margin: '0px 12px',
                        lineHeight: '24px',
                        textAlign: 'center',
                    }}>
                        {this.renderLabel(showLabel)}
                        {this.renderPopupButton(showPopupButton)}
                        {this.renderEditButton(showEditButton)}
                        {this.renderConfirmCancelButtons(showConfirmCancelButtons)}
                        {this.renderLabelOverButton(!showLabel)}
                    </div>
                )}
                {/* <ExtraInfo reminder={this.state.invalidTextMessage}> */}
                    <FormControl
                        error={this.state.invalidTextMessage != ''}
                        variant='outlined'
                        style={{width: '100%', margin: '2px 6px', height: this.props.multiline ? '' : (this.props.helperText ? '32px' : '20px')}}
                    >
                        <this.StyledOutlinedInput
                            inputRef={this.textField}
                            value={this.state.textValue}
                            placeholder={this.props.placeholder}
                            disabled={
                                this.props.disabled ||
                                (!(this.props.disabledMessage == undefined || this.props.disabledMessage == '') ||
                                (this.props.editPressRequired && !this.state.editing) ||
                                this.props.editPopup !== undefined)
                            }
                            onChange={this.handleChange}
                            onKeyDown={(event: React.KeyboardEvent) => { if ((!this.props.multiline && event.key == 'Enter') || event.key == 'Escape') this.textField.current.blur() }}
                            onFocus={this.handleFocus}
                            onBlur={this.handleBlur}
                            type={this.props.password && this.state.hidePassword ? 'password' : 'text'}
                            multiline={this.props.multiline}
                            required={this.props.required}
                            rows={(() => {
                                const lines = this.state.textValue.split('\n').length;
                                if (this.props.minLines && lines < this.props.minLines) return this.props.minLines;
                                return lines;
                            })()}
                            endAdornment={
                                (this.props.disabled || !(this.props.disabledMessage == undefined || this.props.disabledMessage == '')) ? (
                                    <ExtraInfo reminder={this.props.disabledMessage}>
                                        <InputAdornment position="end" style={{height: '20px', margin: '0px 3px 0px 0px'}}>
                                            <IconButton
                                                disabled
                                                style={{padding: '3px 3px 3px 0px'}}
                                            >
                                                <LockIcon style={{width: '14px', height: '14px'}} />
                                            </IconButton>
                                        </InputAdornment>
                                    </ExtraInfo>
                                ) : this.props.password && (
                                    <ExtraInfo reminder={this.state.hidePassword ? 'Show Password' : 'Hide Password'}>
<                                        InputAdornment position="end" style={{height: '20px', margin: '0px 3px 0px 0px'}}>
                                            <IconButton
                                                onClick={() => this.setState({hidePassword: !this.state.hidePassword})}
                                                style={{padding: '3px 3px 3px 0px'}}
                                            >
                                                {this.state.hidePassword ? (
                                                    <VisibilityOffIcon style={{width: '14px', height: '14px'}} /> 
                                                ) : (
                                                    <VisibilityIcon style={{width: '14px', height: '14px'}} />
                                                )}
                                            </IconButton>
                                        </InputAdornment>
                                    </ExtraInfo>
                                )
                            }
                        />
                        {this.props.helperText && 
                            <FormHelperText style={{fontSize: '10px', lineHeight: '10px', margin: '4px 6px', whiteSpace: 'nowrap'}}>
                                {this.props.helperText}
                            </FormHelperText>
                        }
                    </FormControl>
                {/* </ExtraInfo> */}
            </div>
        )
    }

    public shouldComponentUpdate = (nextProps: IProps<any>, nextState: IState<any>): boolean => {
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
