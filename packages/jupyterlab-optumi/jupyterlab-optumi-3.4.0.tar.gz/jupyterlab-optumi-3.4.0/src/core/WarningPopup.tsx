/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Button, Checkbox, Dialog, DialogActions, DialogContent, DialogTitle, ListItemText, Theme, withStyles } from '@material-ui/core'
import * as React from 'react'
import { Header } from './Header'
import { ShadowedDivider } from './ShadowedDivider'

const StyledDialog = withStyles((theme: Theme) => ({
    root: {
        margin: '12px',
        padding: '0px',
    },
    paper: {
        backgroundColor: 'var(--jp-layout-color1)',
    },
}))(Dialog)

interface IProps {
    open: boolean,
    headerText?: string
    bodyText?: string
    preventText?: string
    cancel?: {
        text: string
        onCancel: (prevent: boolean) => void
    }
    continue: {
        text: string
        onContinue: (prevent: boolean) => void
        color: 'primary' | 'secondary' | 'error' | 'success' | 'warning' | 'info'
    }
}

interface IState {
    prevent: boolean
}

export default class WarningPopup extends React.Component<IProps, IState> {
    private ContinueButton: any;

    constructor(props: IProps) {
        super(props)
        this.state = {
            prevent: false,
        }
        this.ContinueButton = withStyles((theme: Theme) => {
            const paletteColor = (() => {
                switch (this.props.continue.color) {
                    case 'primary': return theme.palette.primary
                    case 'secondary': return theme.palette.secondary
                    case 'success': return theme.palette.success
                    case 'error': return theme.palette.error
                    case 'warning': return theme.palette.warning
                    case 'info': return theme.palette.info
                }
            })()
            return ({
                root: {
                    color: paletteColor.contrastText,
                    backgroundColor: paletteColor.main,
                    '&:hover': {
                        backgroundColor: paletteColor.dark,
                        // Reset on touch devices, it doesn't add specificity
                        '@media (hover: none)': {
                            backgroundColor: paletteColor.main,
                        },
                    },
                },
            })
        })(Button);
    }

    public render = (): JSX.Element => {
        return (
            <StyledDialog
                disableBackdropClick
                disableEscapeKeyDown
                open={this.props.open}
            >
                {this.props.headerText &&
                    <DialogTitle
                        disableTypography
                        style={{
                            backgroundColor: 'var(--jp-layout-color2)',
                            height: '48px',
                            padding: '6px 30px',
                        }}
                    >
                        <Header
                            title={this.props.headerText}
                            style={{lineHeight: '24px'}}
                        />
                    </DialogTitle>
                }
                <ShadowedDivider />
                <div style={{padding: '18px'}}>
                    {this.props.bodyText &&
                        <DialogContent style={{padding: '6px 18px'}}>
                            {this.props.bodyText}
                        </DialogContent>
                    }
                    <DialogActions style={{padding: '12px 6px 6px 6px'}}>
                        {this.props.preventText &&
                            <>
                                <Checkbox
                                    checked={this.state.prevent}
                                    onClick={() => this.setState({prevent: !this.state.prevent})}
                                />
                                <ListItemText
                                    disableTypography
                                    primary={this.props.preventText}
                                    style={{marginLeft: '0px', fontSize: '14px'}}
                                />
                            </>
                        }
                        {this.props.cancel &&
                            <Button
                                variant='contained'
                                onClick={() => {
                                    this.setState({prevent: false})
                                    this.props.cancel.onCancel(this.state.prevent)
                                }}
                                color={'default'}
                            >
                                {this.props.cancel.text}
                            </Button>
                        }
                        <this.ContinueButton
                            variant='contained'
                            onClick={() => this.props.continue.onContinue(this.state.prevent)}
                            style={{marginLeft: '18px'}}
                        >
                            {this.props.continue.text}
                        </this.ContinueButton>
                    </DialogActions>
                </div>
           </StyledDialog>
        )
    }
}