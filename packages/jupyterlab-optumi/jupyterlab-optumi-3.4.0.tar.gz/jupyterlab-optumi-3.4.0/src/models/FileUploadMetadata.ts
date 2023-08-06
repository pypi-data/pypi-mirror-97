/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

export class FileUploadMetadata {
    public path: string;
    public type: 'file' | 'notebook' | 'directory';
    public mimetype: string;

    constructor(map: any) {
        this.path = map.path;
        this.type = map.type || 'file';
        this.mimetype = map.mimetype || 'text/plain';
    }
}
