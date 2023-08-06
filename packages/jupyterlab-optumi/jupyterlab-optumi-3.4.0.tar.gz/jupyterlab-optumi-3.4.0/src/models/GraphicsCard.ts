/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

export class GraphicsCard {
	private _name: string;
	private _configs: number[];

	constructor(name: string, configs: number[]) {
		this._name = name;
		this._configs = configs;
    }
    
    get name() {
        return this._name;
    }

    get configs() {
        return this._configs;
    }

    public addConfig(value: number) {
        if (!this._configs.includes(value)) {
            this._configs.push(value);
        }
    }
}