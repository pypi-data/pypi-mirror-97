/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { DataService } from "../components/deploy/dataConnectorBrowser/DataConnectorDirListingItemIcon";

export class DataConnectorUploadMetadata {
    public name: string;
    public dataService: DataService;

    constructor(map: any) {
        this.name = map.name;
        this.dataService = map.dataService || DataService.GOOGLE_DRIVE;
    }
}
