/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { ServerConnection } from '@jupyterlab/services';

export default class FileServerUtils {
	// Return two booleans, the first is if the path exists, the second is if it is a file (true) or directory (false)
	public static async checkIfPathExists(filePath: string): Promise<boolean[]> {
		const splitPath = filePath.split("/");
		let path = "";
		for (let i = 0; i < splitPath.length-1; i++) {
			path += splitPath[i]
			if (i != splitPath.length-2) {
				path += "/"
			}
		}
		const fileName = splitPath[splitPath.length-1]
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "api/contents/" + path;
		const response = ServerConnection.makeRequest(
			url, 
			{}, 
			settings
		).then((response: Response) => {
			if (response.status !== 200) {
				throw new ServerConnection.ResponseError(response);
			}
			return response.json();
		})
		try {
			const body = (await response);
			return [body.content.some((x: any) => x.name === fileName), body.content.some((x: any) => x.name == fileName && x.type != 'directory')];
		} catch (e) {
			// If we can't find the file, the second value is invalid
			return [false, undefined]
		}
	}

	public static async getRecursiveTree(fileName: string): Promise<string[]> {
		var files: string[] = [];
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "api/contents/" + fileName;
		const response = ServerConnection.makeRequest(
			url, 
			{}, 
			settings
		).then((response: Response) => {
			if (response.status !== 200 && response.status !== 201) {
				throw new ServerConnection.ResponseError(response);
			}
			return response.json();
		});
		const body = (await response);

		if (body.type == 'directory') {
			const promises: Promise<string[]>[] = [];
			for (var file of body.content) {
				if (file.type == 'directory') {
					promises.push(this.getRecursiveTree(file.path));
				} else {
					files.push(file.path);
				}
			}
			for (var promise of promises) {
				files = files.concat(await promise);
			}
		} else {
			files.push(body.path);
		}
		return files;
	}

	public static async saveNotebook(path: string, notebook: any): Promise<boolean> {
		const settings = ServerConnection.makeSettings();
		const url = settings.baseUrl + "api/contents/" + path;
		const response = ServerConnection.makeRequest(
			url, 
			{
				body: JSON.stringify({
					content: notebook,
					'format': 'json',
					'type': 'notebook',
				}),
				method: 'PUT'
			}, 
			settings
		).then(response => {
			if (response.status !== 200 && response.status !== 201) {
				throw new ServerConnection.ResponseError(response);
			}
			return response.json();
		});
		const body = (await response);
		if (body) return true;
		return false;
	}
}
