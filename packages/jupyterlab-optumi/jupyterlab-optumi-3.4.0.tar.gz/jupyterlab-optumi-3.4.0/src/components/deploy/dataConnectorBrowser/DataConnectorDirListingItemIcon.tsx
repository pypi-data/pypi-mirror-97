/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import * as React from 'react'
import { fileIcon } from '@jupyterlab/ui-components'
import { CSSProperties } from '@material-ui/core/styles/withStyles'

export enum DataService {
    AMAZON_S3 = 'amazon s3',
    WASABI = 'wasabi',
    GOOGLE_CLOUD_STORAGE = 'google cloud storage',
    GOOGLE_DRIVE = 'google drive',
    KAGGLE = 'kaggle',
    EMPTY = '--',
}

interface DataConnectorType {
    dataService: DataService,
    iconClass: string,
}

const dataConnectorTypes: DataConnectorType[] = [
    {dataService: DataService.AMAZON_S3,            iconClass: 'jp-s3-logo'},
    {dataService: DataService.WASABI,               iconClass: 'jp-wasabi-logo'},
    {dataService: DataService.GOOGLE_DRIVE,         iconClass: 'jp-drive-logo'},
    {dataService: DataService.GOOGLE_CLOUD_STORAGE, iconClass: 'jp-cloud-logo'},
    {dataService: DataService.KAGGLE,               iconClass: 'jp-kaggle-logo'},
    {dataService: DataService.EMPTY,                iconClass: ''},
]

interface IProps {
    dataService: DataService,
    style?: CSSProperties,
}

interface IState {}

export default class DataConnectorDirListingItemIcon extends React.Component<IProps, IState> {

    constructor(props: IProps) {
        super(props)
    }

    public render = (): JSX.Element => {
        return (
            <span className='jp-DirListing-itemIcon'>
                {(() => {
                    for (const dataConnectorType of dataConnectorTypes) {
                        if (dataConnectorType.dataService === this.props.dataService) {
                            return (
                                <div
                                    title={dataConnectorType.dataService}
                                    className={dataConnectorType.iconClass}
                                    style={Object.assign({
                                        width: '16px',
                                        height: '16px',
                                        backgroundSize: 'contain',
                                        display: 'block'
                                    }, this.props.style)}
                                />
                            )
                        }
                    }
                    return <fileIcon.react display='block'/>
                })()}
            </span>
        )
    }
}