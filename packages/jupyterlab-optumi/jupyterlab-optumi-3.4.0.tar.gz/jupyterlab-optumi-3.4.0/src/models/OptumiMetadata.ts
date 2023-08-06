/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { Global } from "../Global";
import { ComputeMetadata } from "./ComputeMetadata";
import { GraphicsMetadata } from "./GraphicsMetadata";
import { MemoryMetadata } from "./MemoryMetadata";
import { StorageMetadata } from "./StorageMetadata";

import { UploadMetadata } from "./UploadMetadata";
import { User } from "./User";

export enum Expertise {
	BASIC = "basic",
    RATING = "rating",
    SIMPLIFIED = "simplified",
	COMPONENT = "component",
	EQUIPMENT = "equipment"
}

export class OptumiMetadata {
	public version: string = Global.version;
	public intent: number;
	public compute: ComputeMetadata;
	public graphics: GraphicsMetadata;
    public memory: MemoryMetadata;
    public storage: StorageMetadata;
	public upload: UploadMetadata;
	public interactive: boolean;
	
	constructor(map: any = {}, user: User = null) {
		if (!map.version) map.version = "None";
		switch (map.version) {
			case "None":
			case "0.3.0":
			case "0.3.1":
			case "0.3.2":
			case "0.3.3":
			case "0.3.4":
			case "0.3.5":
			case "0.3.6":
			case "0.3.7":
			case "0.3.8":
			case "0.3.9":
			case "0.3.10":
			case "0.3.11":
			case "0.3.12":
			case "0.3.13":
            case "0.3.14":
            case "0.3.15":
            case "0.3.16":
            case "0.3.17":
            case "20.9.0-0":
            case "20.9.1-0":
            case "20.9.1-1":
            case "20.10.0-0":
            case "20.10.1":
            case "20.10.1-1":
            case "20.10.1-2":
            case "20.10.1-3":
            case "20.10.1-4":
            case "20.10.1-5":
				/// Anything before this will result in default metadata
				map = {}
			case "20.12.0":
			case "20.12.0-1":
			case "2.1.0":
			case "2.1.1":
			case "2.1.2":
			case "2.2.0":
			case "3.3.0":
			case "3.3.1":
			case "3.3.2":
				break;
			default:
				console.log("Unknown map version: " + map.version);
        }
        
        this.intent = (map.intent != undefined ? map.intent : ((user) ? user.intent : 0));
		this.compute = new ComputeMetadata(map.compute || {}, user);
		this.graphics = new GraphicsMetadata(map.graphics || {}, user); 
        this.memory = new MemoryMetadata(map.memory || {}, user);
        this.storage = new StorageMetadata(map.storage || {});
		this.upload = new UploadMetadata(map.upload || {});
		this.interactive = map.interactive == undefined ? true : map.interactive;
	}
}
