/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react';
import { IdentityMachineComponent } from './IdentityMachineComponent';
import { MachineComponent } from './MachineComponent';
import { PopupMachineComponent } from './PopupMachineComponent';
import { RecommendedMachineComponent } from './RecommendedMachineComponent';

export class Machine {
    computeCores: number = 0
    computeFrequency: number = 0
    computeRating: number = 0
    computeScore: number = 0
    graphicsCardType: string = 'None'
    graphicsCores: number = 0
    graphicsFrequency: number = 0
    graphicsMemory: number = 0
    graphicsNumCards: number = 0
    graphicsRating: number = 0
    graphicsScore: number = 0
    memoryRating: number = 0
    memorySize: number = 0
    storageRating: number = 0
    storageSize: number = 0
    storageIops: number = 0
    storageThroughput: number = 0
    uuid: string
    name: string
    rate: number
    promo: boolean
    state: string

    public getComponent(): React.CElement<any, MachineComponent> {
        return React.createElement(MachineComponent, {key: this.uuid, machine: this});
    }

    public getRecommendedComponent(order: number): React.CElement<any, RecommendedMachineComponent> {
        return React.createElement(RecommendedMachineComponent, {key: this.uuid + order, machine: this, order: order});
    }

    public getIdentityComponent(): React.CElement<any, IdentityMachineComponent> {
        return React.createElement(IdentityMachineComponent, {key: this.uuid, machine: this});
    }

    public getPopupComponent(): React.CElement<any, PopupMachineComponent> {
        return React.createElement(PopupMachineComponent, {key: this.uuid, machine: this});
    }

    static getStateMessage(state: string): string {
        switch (state) {
            case 'requisition requested':
            case 'requisition in progress':
                return 'Acquiring...'
            case 'requisition completed':
            case 'setup completed':
                return 'Ready'
            case 'teardown requested':
            case 'sequestration requested':
            case 'sequestration in progress':
            case 'sequestration completed':
                return 'Releasing...'
            case 'unused':
            default:
                return ''
        }
    }
}

export class NoMachine extends Machine {
    // Use this class to indicate there is no machine that matches
}