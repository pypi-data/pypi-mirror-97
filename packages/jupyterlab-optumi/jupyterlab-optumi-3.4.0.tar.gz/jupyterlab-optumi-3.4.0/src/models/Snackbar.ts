/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { OptionsObject } from "notistack";

/// NOTE: Look here for possible props: https://iamhosseindhv.com/notistack/api#enqueuesnackbar-options

export const providerOptions = {
    success: { backgroundColor: '#68da7c!important' },
    error: { backgroundColor: '#f48f8d!important' },
    warning: { backgroundColor: '#ffba7d!important' },
    info: { backgroundColor: '#10A0F9!important' },
}

export class Snackbar {
    message: String;
    options: OptionsObject;

    private standardOptions: OptionsObject = {
        anchorOrigin: {
            vertical: 'bottom',
            horizontal: 'center',
        },
    }

    constructor(message: String, options: OptionsObject) {
        this.message = message;
        this.options = Object.assign({}, options, this.standardOptions);
    }
}