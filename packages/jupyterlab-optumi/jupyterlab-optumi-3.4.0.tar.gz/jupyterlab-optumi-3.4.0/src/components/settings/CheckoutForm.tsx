/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../Global';

import { ServerConnection } from '@jupyterlab/services';

import {
    loadStripe,
	Stripe,
    StripeError,
} from '@stripe/stripe-js';
import { Button, Select, MenuItem, withStyles, CircularProgress } from '@material-ui/core';


// Properties from parent
interface IProps {}

// Properties for this component
interface IState {
    amount: number
    waiting: false,
}

const StyledSelect = withStyles({
    root: {
        fontSize: "var(--jp-ui-font-size1)",
    },
    iconOutlined: {
        right: '0px'
    }
}) (Select)

const StyledMenuItem = withStyles({
    root: {
        fontSize: 'var(--jp-ui-font-size1)',
        padding: '3px 3px 3px 6px',
    }
}) (MenuItem)

// const stripePromise = loadStripe("pk_test_51HIzv8LdDawhowJuVhTKv6KRnt72In8txUs0Dss0eT4KgFFcRfQlkWEDX9kzhAeiTjiYbxgxRvKbR6TfSJcqiD4o00irQVFdtY");
const stripePromise = loadStripe("pk_live_51HIzv8LdDawhowJuSfMFb1yBW8F9VfK87tSAfMF2UdwTNVdaixpy7xjYUcP6d5GGWs1bDfLGEexyjbYj0dkKHJac00HMDHWhxU");

export class CheckoutForm extends React.Component<IProps, IState> {
    _isMounted = false;

    constructor(props: IProps) {
        super(props);
        this.state = {
            amount: 10,
            waiting: false,
        }
    
    }

    private handleClick = async () => {
        // Get Stripe.js instance    
        // Call your backend to create the Checkout Session
        
        this.checkAndSetState({ waiting: true });

        const stripe: Stripe = await stripePromise;
        
        const settings = ServerConnection.makeSettings();
        const url = settings.baseUrl + "optumi/create-checkout";
        const init: RequestInit = {
            method: 'POST',
            body: JSON.stringify({
                items: [Math.round(this.state.amount).toString() + ' credits'],
                redirect: settings.baseUrl,
            }),
        };
        ServerConnection.makeRequest(
            url,
            init,
            settings
        ).then((response: Response) => {
            Global.handleResponse(response);
            return response.json();
        }).then((body: any) => {
            // When the customer clicks on the button, redirect them to Checkout.
            return stripe.redirectToCheckout({
                sessionId: body.id,
            });
        }).then((result: {error: StripeError}) => {
            this.checkAndSetState({ waiting: false });
            if (result.error) {
                // If `redirectToCheckout` fails due to a browser or network
                // error, display the localized error message to your customer
                // using `result.error.message`.
                
            }
        });
    };

    
    private handleAmountChange = (event: React.ChangeEvent<{ value: unknown }>) => {
        const value: number = event.target.value as number;
        this.checkAndSetState({ amount: value });
    }

    private isCustom(amount: number): boolean {
        return !(this.state.amount == 5 || this.state.amount == 10 || this.state.amount == 25 || this.state.amount == 50 || this.state.amount == 100);
    }

	// The contents of the component
	render() {
		if (Global.shouldLogOnRender) console.log('CheckoutForm (' + new Date().getSeconds() + ')');
		return (
            <>
                <div style={{display: 'inline-flex', width: '100%', padding: '3px 0px'}}>
                    <div 
                        style={{
                        lineHeight: '24px',
                        margin: '0px 12px',
                        flexGrow: 1,
                    }}
                    >
                        {'Increase balance by'}
                    </div>
                    <div style={{padding: '0px 6px 0px 6px'}}>
                        <StyledSelect
                            value={ this.isCustom(this.state.amount) ?   -1 : this.state.amount }
                            variant='outlined'
                            onChange={this.handleAmountChange}
                            SelectDisplayProps={{style: {padding: '3px 20px 3px 6px'}}}
                            MenuProps={{MenuListProps: {style: {paddingTop: '6px', paddingBottom: '6px'}}}}
                        >
                            <StyledMenuItem value={5}>$5</StyledMenuItem>
                            <StyledMenuItem value={10}>$10</StyledMenuItem>
                            <StyledMenuItem value={25}>$25</StyledMenuItem>
                            <StyledMenuItem value={50}>$50</StyledMenuItem>
                            <StyledMenuItem value={100}>$100</StyledMenuItem>
                        </StyledSelect>
                    </div>
                </div>
                <div style={{padding: '6px', width: '100%'}}>
                    <Button 
                        disabled={this.state.waiting} 
                        color="primary" 
                        variant="contained"
                        style={{width: '100%'}}
                        onClick={this.handleClick}
                    >
                        {this.state.waiting ? (<CircularProgress size='1.75em'/>) : 'Checkout'}
                    </Button>
                </div>
            </>
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
}