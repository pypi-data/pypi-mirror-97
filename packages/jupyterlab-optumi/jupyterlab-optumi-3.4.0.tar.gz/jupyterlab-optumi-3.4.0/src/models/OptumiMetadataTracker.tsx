/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { ISignal, Signal } from '@lumino/signaling';

import { NotebookPanel, NotebookTracker } from '@jupyterlab/notebook';
import { OptumiMetadata } from './OptumiMetadata';

export class OptumiMetadataTracker {
    private _optumiMetadata = new Map<string, TrackedOptumiMetadata>();

    private _tracker: NotebookTracker;

    constructor(tracker: NotebookTracker) {
        this._tracker = tracker;
        tracker.currentChanged.connect(() => {
            this.handleCurrentChanged(this._tracker.currentWidget);
        });
        this.handleCurrentChanged(this._tracker.currentWidget);
	}

	private handleCurrentChanged = async (current: NotebookPanel) => {
        if (current == null) {
            setTimeout(() => this.handleCurrentChanged(this._tracker.currentWidget), 250);
            return;
        }
        if (!current.context.isReady) await current.context.ready;
        // If the path changes we need to add a new entry into our map
        current.context.pathChanged.connect(() => this.handleCurrentChanged(current));
        const path = current.context.path;
        const rawMetadata = current.model.metadata;
        const metadata = new OptumiMetadata(rawMetadata.get("optumi") || {});
		this._optumiMetadata.set(path, new TrackedOptumiMetadata(path, metadata));
        // Save the metadata to make sure all files have valid metadata
		rawMetadata.set("optumi", JSON.parse(JSON.stringify(metadata)));
		this._metadataChanged.emit(void 0);
	}

	public getMetadata = (): TrackedOptumiMetadata => {
        const path: string = this._tracker.currentWidget.context.path;
        if (!this._optumiMetadata.has(path)) {
            // If for some reason we can't find the metadata, return empty metadata to avoid a crash
            return new TrackedOptumiMetadata(path, new OptumiMetadata({}));
        }
        return this._optumiMetadata.get(path);
	}

	public setMetadata = (optumi: TrackedOptumiMetadata) => {
		const rawMetadata = this._tracker.find(x => x.context.path == optumi.path).model.metadata;
		rawMetadata.set("optumi", JSON.parse(JSON.stringify(optumi.metadata)));
		this._metadataChanged.emit(void 0);
	}

	public getMetadataChanged = (): ISignal<this, void> => {
		return this._metadataChanged;
	}

    private _metadataChanged = new Signal<this, void>(this);
}

export class TrackedOptumiMetadata {
    public path: string;
    public metadata: OptumiMetadata;

    constructor(path: string, metadata: OptumiMetadata) {
        this.path = path;
        this.metadata = metadata;
    }
}
