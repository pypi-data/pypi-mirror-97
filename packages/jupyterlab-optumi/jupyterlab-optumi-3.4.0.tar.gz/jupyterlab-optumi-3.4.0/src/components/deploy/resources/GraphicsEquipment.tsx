/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { Global } from '../../../Global';

import { GraphicsCard } from '../../../models/GraphicsCard';
import { MenuItem, Select, withStyles } from '@material-ui/core';
import { GraphicsMetadata } from '../../../models/GraphicsMetadata';
import { OptumiMetadataTracker } from '../../../models/OptumiMetadataTracker';

interface IProps {
    style?: React.CSSProperties,
}

interface IState {
    selectedCard: string
    selectedNumCard: number
}

const StyledSelect = withStyles({
    root: {
        fontSize: "var(--jp-ui-font-size1)",
        width: '68px',
    },
    iconOutlined: {
        right: '0px'
    }
}) (Select)

const StyledMenuItem = withStyles({
    root: {
        fontSize: 'var(--jp-ui-font-size1)',
        padding: '3px 3px 3px 6px',
        justifyContent: 'center',
    }
}) (MenuItem)

export class GraphicsEquipment extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props);
        var card = this.getCardValue();
        var numCard = this.getNumCardValue();
        // TODO:JJ Get this list of valid names/numbers from the available graphics cards
        card = ['None', 'K80', 'M60', 'P100', 'V100'].includes(card) ? card : 'None';
        numCard = [-1, 1, 2, 4].includes(numCard) ? numCard : -1;
        this.state = {
            selectedCard: numCard == -1 ? "None" : card,
            selectedNumCard: numCard,
        }
        this.saveCardValue(this.state.selectedCard);
        this.saveNumCardValue(this.state.selectedNumCard);
    }
    
    private getCardValue(): string {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsMetadata = optumi.metadata.graphics;
        return graphics.boardType;
	}

	private async saveCardValue(value: string) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsMetadata = optumi.metadata.graphics;
        graphics.boardType = value;
        tracker.setMetadata(optumi);
    }
    
    private getNumCardValue(): number {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsMetadata = optumi.metadata.graphics;
        return graphics.boardCount[0];
	}

	private async saveNumCardValue(value: number) {
        const tracker: OptumiMetadataTracker = Global.metadata;
        const optumi = tracker.getMetadata();
        const graphics: GraphicsMetadata = optumi.metadata.graphics;
        graphics.boardCount = [value, -1, -1];
        tracker.setMetadata(optumi);
	}

    private handleCardChange = (event: React.ChangeEvent<{ value: unknown }>) => {
        const value: string = event.target.value as string;
        this.setState({ selectedCard: value });
        this.saveCardValue(value);

        if (value != 'None') {
            const card = Global.user.machines.absoluteGraphicsMaxCards.filter(x => x.name == value).pop()
            for (var i = card.configs.length-1; i >= 0 ; i--) {
                if (this.state.selectedNumCard >= card.configs[i]) {
                    this.setState({selectedNumCard: card.configs[i]});
                    break;
                }
            }
        }
    }

    private handleNumCardChange = (event: React.ChangeEvent<{ value: unknown }>) => {
        const value: number = event.target.value as number;
        if (value == -1) {
            this.setState({ selectedNumCard: value, selectedCard: 'None' });
            this.saveNumCardValue(value);
            this.saveCardValue('None');
        } else {
            this.setState({ selectedNumCard: value });
            this.saveNumCardValue(value);
        }
    }

    private getCardItems = (): JSX.Element[] => {
        var cardItems: JSX.Element[] = new Array();
        cardItems.push(<StyledMenuItem key={'None'} value={'None'}>Any</StyledMenuItem>)
        const availableCards: GraphicsCard[] = Global.user.machines.absoluteGraphicsMaxCards;
        for (var i = 0; i < availableCards.length; i++) {
            var value = availableCards[i].name
            cardItems.push(<StyledMenuItem key={value} value={value}>{value}</StyledMenuItem>)
        }
        return cardItems;
    }

    private getNumCardItems = (cardName: string): JSX.Element[] => {
        var numCardItems: JSX.Element[] = new Array();
        numCardItems.push(<StyledMenuItem key={-1} value={-1}>{'At least 0'}</StyledMenuItem>)
        if (cardName == 'None') {
            numCardItems.push(<StyledMenuItem key={1} value={1}>{'At least 1'}</StyledMenuItem>)
            numCardItems.push(<StyledMenuItem key={2} value={2}>{'At least 2'}</StyledMenuItem>)
            numCardItems.push(<StyledMenuItem key={4} value={4}>{'At least 4'}</StyledMenuItem>)
        } else {
            const card = Global.user.machines.absoluteGraphicsMaxCards.filter(x => x.name == cardName).pop()
            if (card != undefined) {
                for (var i = 0; i < card.configs.length; i++) {
                    var value = card.configs[i]
                    numCardItems.push(<StyledMenuItem key={value} value={value}>{'At least ' + value}</StyledMenuItem>)
                }
            }
        }
        return numCardItems;
    }

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('GraphicsBasicRender (' + new Date().getSeconds() + ')');
        return (
            <div style={{display: 'inline-flex', width: '100%', padding: '3px 0px'}}>
                {/* <div 
                    style={{
                    minWidth: '68px',
                    lineHeight: '24px',
                    textAlign: 'center',
                    margin: '0px 6px',
                }}/> */}
                <div style={{display: 'inline-flex', width: '100%', justifyContent: 'center'}}>
                    <div style={{padding: '0px 6px 0px 6px'}}>
                        <StyledSelect
                            value={this.state.selectedNumCard}
                            variant='outlined'
                            onChange={this.handleNumCardChange}
                            SelectDisplayProps={{style: {padding: '3px 20px 3px 6px'}}}
                            MenuProps={{MenuListProps: {style: {paddingTop: '6px', paddingBottom: '6px'}}}}
                        >
                            {this.getNumCardItems(this.state.selectedCard)}
                        </StyledSelect>
                    </div>
                    <div style={{padding: '0px 6px 0px 6px'}}>
                        <StyledSelect
                            disabled={this.state.selectedNumCard == -1}
                            value={this.state.selectedCard}
                            variant='outlined'
                            onChange={this.handleCardChange}
                            SelectDisplayProps={{style: {padding: '3px 20px 3px 6px'}}}
                            MenuProps={{MenuListProps: {style: {paddingTop: '6px', paddingBottom: '6px'}}}}
                        >
                            {this.getCardItems()}
                        </StyledSelect>
                    </div>
                </div>               
                <div 
                    // title={this.props.tooltip || ''}
                    style={{
                    minWidth: '68px',
                    lineHeight: '24px',
                    textAlign: 'center',
                    margin: '0px 6px',
                }}>
                    {'Cards'}
                </div>
            </div>
        )
    }

    private handleMetadataChange = () => { this.forceUpdate() }

    // Will be called automatically when the component is mounted
	componentDidMount = () => {
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
