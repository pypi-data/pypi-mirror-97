/*
**  Copyright (C) Optumi Inc - All rights reserved.
**
**  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
**  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
**/

import { CSSProperties } from '@material-ui/core/styles/withStyles';
import * as React from 'react'
import { Global } from '../../Global';
import { DataConnectorMetadata } from './dataConnectorBrowser/DataConnectorBrowser';
import DataConnectorDirListingItem from './dataConnectorBrowser/DataConnectorDirListingItem';
import { DataService } from './dataConnectorBrowser/DataConnectorDirListingItemIcon';


interface IProps {
    iconClass: string;
    dataService: DataService;
    description?: string;
    handleClick?: () => any;
    style?: CSSProperties;
}

interface IState {}

export class CreateDataConnector extends React.Component<IProps, IState> {

    public render = (): JSX.Element => {
        if (Global.shouldLogOnRender) console.log('GoogleDriveDataConnectorPopupRender (' + new Date().getSeconds() + ')');
        return (
            <div style={Object.assign({}, this.props.style)}>
                <DataConnectorDirListingItem
                        key={this.props.dataService}
                        dataConnectorMetadata={{
                            name: this.props.description,
                            dataService: this.props.dataService,
                        } as DataConnectorMetadata}
                        selected={false}
                        handleButtonClick={this.props.handleClick}
                        buttonText='Create'
                        buttonColor='#10A0F9'
                        onClick={() => false}
                        onDoubleClick={() => false}
                    />
            </div>
            // <div style={{margin: '6px'}}>
            //     <div style={{display: 'inline-flex', width: '100%', height: '40px'}}>
            //         <div className={this.props.iconClass} style={{width: '30px', margin: '6px 6px 6px 12px'}}/>
            //         <div style={{margin: 'auto 6px', lineHeight: '14px', width: this.props.description && '92px'}}>
            //             <div style={{fontWeight: 'bold'}}>
            //                 {this.props.provider}
            //             </div>
            //             {this.props.service != '' && (
            //                 <div>
            //                     {this.props.service}
            //                 </div>
            //             )}
            //         </div>
            //         {this.props.description && <div style={{flexGrow: 1, margin: 'auto 12px', maxWidth: '160px'}}>
            //             {this.props.description}
            //         </div>}
            //         {this.props.handleClick && <Button
            //             onClick={this.props.handleClick}
            //             style={{
            //             //     padding: '6px',
            //             //     fontWeight: 'bold',
            //             //     height: '24px',
            //                 margin: 'auto 12px',
            //             }}
            //             variant='outlined'
            //             color='primary'
            //             disableElevation
            //         >
            //             Create   
            //         </Button>}
            //     </div>
            // </div>
        )
    }
}
