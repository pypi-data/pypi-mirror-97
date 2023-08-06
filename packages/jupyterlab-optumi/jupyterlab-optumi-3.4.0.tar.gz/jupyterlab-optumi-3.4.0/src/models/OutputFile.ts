/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

export class OutputFile {
    public path: string;
    public lastModified: string;
    public size: number;
    public lastDownloaded: string;

    constructor(path: string, lastModified: string, size: string) {
        this.path = path;
        this.lastModified = lastModified;
        this.size = +size;
        this.lastDownloaded = "";
    }
}