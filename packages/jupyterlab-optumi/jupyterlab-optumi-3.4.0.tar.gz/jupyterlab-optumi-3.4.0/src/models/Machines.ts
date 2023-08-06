/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { ISignal, Signal } from '@lumino/signaling';

import { GraphicsCard } from './GraphicsCard';
import { Machine } from './machine/Machine';

export class Machines {
	public inventory: Machine[];

    private _changed = new Signal<this, Machines>(this);

	get changed(): ISignal<this, Machines> {
		return this._changed;
	}

    // Max compute values
    public absoluteComputeMaxCores = 0;
    public absoluteComputeMaxScore = 0;
    public absoluteComputeMaxFrequency = 0;
    // Max graphics values
    public absoluteGraphicsMaxScore = 0;
    public absoluteGraphicsMaxCores = 0;
    public absoluteGraphicsMaxMemory = 0;
    public absoluteGraphicsMaxFrequency = 0;
    public absoluteGraphicsMaxCards: GraphicsCard[] = [];
    // Max memory values
    public absoluteMemoryMaxSize = 0;
    // Max storage values
    public absoluteStorageMaxSize = 0;
    public absoluteStorageMaxIops = 0;
    public absoluteStorageMaxThroughput = 0;

    // Min compute values
    public absoluteComputeMinCores = 0;
    public absoluteComputeMinScore = 0;
    public absoluteComputeMinFrequency = 0;
    // Min graphics values
    public absoluteGraphicsMinScore = 0;
    public absoluteGraphicsMinCores = 0;
    public absoluteGraphicsMinMemory = 0;
    public absoluteGraphicsMinFrequency = 0;
    // public absoluteGraphicsMinCards: GraphicsCard[] = [];
    // Min memory values
    public absoluteMemoryMinSize = 0;
    // Min storage values
    public absoluteStorageMinSize = 0;
    public absoluteStorageMinIops = 0;
    public absoluteStorageMinThroughput = 0;

    // The cheapest machine available, so we can adjust the resource cap slider
    public cheapestMachine: Machine = null;
    // The most expensive machine available, incase we want to adjust the max resource cap in the future
    public mostExpensiveMachine: Machine = null;

    // A list of all graphics cards
    public graphicsCards: GraphicsCard[] = [];

	constructor(machines: Machine[], maxCost: number) {
        this.inventory = machines;
        this.setAbsoluteMaxResources(maxCost);
        // Global.onUserChange.connect(() => this.setAbsoluteMaxResources());
    }

    //  It is useful for us to know what the cost of the cheapest machine is
    public getCheapestMachineCost(): number {
        if (this.cheapestMachine != null) {
            return this.cheapestMachine.rate;
        }
        return 0;
    }

    public getMostExpensiveMachineCost(): number {
        if (this.mostExpensiveMachine != null) {
            return this.mostExpensiveMachine.rate
        }
        return 0;
    }

    public setAbsoluteMaxResources(maxCost: number) {
        for (let machine of this.inventory) {
            if (machine.rate > maxCost) continue;

            if (machine.graphicsNumCards != 0) {
                // Try to get card from list we have info about
                var graphicsCard: GraphicsCard = this.absoluteGraphicsMaxCards.filter(x => x.name == machine.graphicsCardType).pop();
                if (graphicsCard) {
                    // If we already have info about the card, add the new info about the card to the old info
                    graphicsCard.addConfig(machine.graphicsNumCards);
                } else {
                    // If this is a new card, add it to the list along with its info
                    this.absoluteGraphicsMaxCards.push(new GraphicsCard(machine.graphicsCardType, [machine.graphicsNumCards]));
                }
            }
        
            var computeCores: number = machine.computeCores;
            if (computeCores > this.absoluteComputeMaxCores) this.absoluteComputeMaxCores = computeCores;
            if (computeCores < this.absoluteComputeMinCores) this.absoluteComputeMinCores = computeCores;

            var computeScore: number = machine.computeScore;
            if (computeScore > this.absoluteComputeMaxScore) this.absoluteComputeMaxScore = computeScore;
            if (computeScore < this.absoluteComputeMinScore) this.absoluteComputeMinScore = computeScore;

            var computeFrequency: number = machine.computeFrequency;
            if (computeFrequency > this.absoluteComputeMaxFrequency) this.absoluteComputeMaxFrequency = computeFrequency;
            if (computeFrequency < this.absoluteComputeMinFrequency) this.absoluteComputeMinFrequency = computeFrequency;
            
            var graphicsScore: number = machine.graphicsScore;
            if (graphicsScore > this.absoluteGraphicsMaxScore) this.absoluteGraphicsMaxScore = graphicsScore;
            if (graphicsScore < this.absoluteGraphicsMinScore) this.absoluteGraphicsMinScore = graphicsScore;
            
            var graphicsCores: number = machine.graphicsCores;
            if (graphicsCores > this.absoluteGraphicsMaxCores) this.absoluteGraphicsMaxCores = graphicsCores;
            if (graphicsCores < this.absoluteGraphicsMinCores) this.absoluteGraphicsMinCores = graphicsCores;

            var graphicsMemory: number = machine.graphicsMemory;
            if (graphicsMemory > this.absoluteGraphicsMaxMemory) this.absoluteGraphicsMaxMemory = graphicsMemory;
            if (graphicsMemory < this.absoluteGraphicsMinMemory) this.absoluteGraphicsMinMemory = graphicsMemory;

            var graphicsFrequency: number = machine.graphicsFrequency;
            if (graphicsFrequency > this.absoluteGraphicsMaxFrequency) this.absoluteGraphicsMaxFrequency = graphicsFrequency;
            if (graphicsFrequency < this.absoluteGraphicsMinFrequency) this.absoluteGraphicsMinFrequency = graphicsFrequency;

            var memorySize = machine.memorySize;
            if (memorySize > this.absoluteMemoryMaxSize) this.absoluteMemoryMaxSize = memorySize;
            if (memorySize < this.absoluteMemoryMinSize) this.absoluteMemoryMinSize = memorySize;

            var storageSize = machine.storageSize;
            if (storageSize > this.absoluteStorageMaxSize) this.absoluteStorageMaxSize = storageSize;
            if (storageSize < this.absoluteStorageMinSize) this.absoluteStorageMinSize = storageSize;

            var storageIops = machine.storageIops;
            if (storageIops > this.absoluteStorageMaxIops) this.absoluteStorageMaxIops = storageIops;
            if (storageIops < this.absoluteStorageMinIops) this.absoluteStorageMinIops = storageIops;

            var storageThroughput = machine.storageThroughput;
            if (storageThroughput > this.absoluteStorageMaxThroughput) this.absoluteStorageMaxThroughput = storageThroughput;
            if (storageThroughput < this.absoluteStorageMinThroughput) this.absoluteStorageMinThroughput = storageThroughput;

            var rate = machine.rate;
            if (this.mostExpensiveMachine == null || rate > this.mostExpensiveMachine.rate) this.mostExpensiveMachine = machine;
            if (this.cheapestMachine == null || rate < this.cheapestMachine.rate) this.cheapestMachine = machine;
        }
    }
}
