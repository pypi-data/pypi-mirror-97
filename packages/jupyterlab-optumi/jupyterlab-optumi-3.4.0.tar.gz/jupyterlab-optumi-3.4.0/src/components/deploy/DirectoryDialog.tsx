// /*
// **  Copyright (C) Optumi Inc - All rights reserved.
// **
// **  You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
// **  To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
// **/

// import { Button, Checkbox, Dialog, DialogContent, IconButton, List, ListItem, ListItemText, TextField, withStyles } from '@material-ui/core';
// import * as React from 'react';
// import { Global } from '../../Global';
// import PopupIcon from '@material-ui/icons/MoreVert';
// import MuiDialogTitle from '@material-ui/core/DialogTitle';
// import { CSSProperties } from '@material-ui/core/styles/withStyles';
// import { ShadowedDivider } from '../../core';
// import CloseIcon from '@material-ui/icons/Close';
// import { OptumiMetadataTracker } from '../../models/OptumiMetadataTracker';
// import FileServerUtils from '../../utils/FileServerUtils';

// const StyledDialog = withStyles({
//     paper: {
//         width: '80%',
//         height: '80%',
//         overflowY: 'visible',
//         backgroundColor: 'var(--jp-layout-color1)',
//         maxWidth: 'inherit',
//     },
// })(Dialog);

// interface IProps {
// 	style?: CSSProperties
// 	disabled?: boolean
// 	path: string;
// 	onClose?: () => void
// }

// // Properties for this component
// interface IState {
// 	open: boolean;
// 	filter: string;
//     files: string[];      // The files in the directory
// 	isDirectory: boolean; // everything referencing this is unnecessary. We don't add this component unless it is a directory
// }

// // TODO:Beck The popup needs to be abstracted out, there is too much going on to reproduce it in more than one file
// export class DirectoryDialog extends React.Component<IProps, IState> {

// 	constructor(props: IProps) {
// 		super(props);
// 		this.state = {
// 			open: false,
// 			filter: "",
//             files: [],
// 			isDirectory: this.isDirectory(),
//         };
//         FileServerUtils.getRecursiveTree(this.props.path).then((diskFileNames: string[]) => {
//             // Delete files form the directory that are no longer on the disk
//             var userFiles = this.getList();
//             for (let file of this.state.files) {
//                 if (!diskFileNames.includes(file)) {
//                     userFiles = userFiles.filter(value => value != file);
//                 }
// 			}
//             this.saveList(userFiles);
//             this.setState({ files: diskFileNames });
//         });
//     }

// 	private isDirectory(): boolean {
// 		const tracker: OptumiMetadataTracker = Global.metadata;
// 		const optumi = tracker.getMetadata();
// 		const upload = optumi.metadata.upload.fileVars;
// 		for (var path of upload) {
// 			if (path.path == this.props.path) {
// 				return path.type == 'directory';
// 			}
// 		}
// 		return false;
// 	}

// 	private getList(): string[] {
// 		const tracker: OptumiMetadataTracker = Global.metadata;
// 		const optumi = tracker.getMetadata();
// 		const upload = optumi.metadata.upload.fileVars;
// 		for (var path of upload) {
// 			if (path.path == this.props.path) {
// 				return path.files;
// 			}
// 		}
// 		return [];
//     }
    
//     private saveList(files: string[]) {
//         const tracker: OptumiMetadataTracker = Global.metadata;
// 		const optumi = tracker.getMetadata();
// 		const upload = optumi.metadata.upload.fileVars;
// 		for (var path of upload) {
// 			if (path.path == this.props.path) {
//                 path.files = files;
// 			}
//         }
//         tracker.setMetadata(optumi);
//     }

// 	private handleClickOpen = () => {
// 		this.setState({ open: this.state.isDirectory ? true : false });
// 	}

// 	private handleClose = () => {
// 		this.setState({ open: false });
// 		if (this.state.isDirectory && this.props.onClose) this.props.onClose()
// 	}

// 	private handleSelectAll = async () => {
//         this.saveList(this.state.files.filter((value: string) => value.includes(this.state.filter)));
//         this.forceUpdate();
// 	}

// 	private handleDeselectAll = async () => {
//         this.saveList(this.state.files.filter((value: string) => !value.includes(this.state.filter)));
//         this.forceUpdate();
// 	}

//     private handleChange = async (filePath: string) => {
// 		const tracker: OptumiMetadataTracker = Global.metadata;
// 		const optumi = tracker.getMetadata();
// 		const upload = optumi.metadata.upload.fileVars;
// 		for (var path of upload) {
// 			if (path.path == this.props.path) {
// 				if (path.files.includes(filePath)) {
//                     // Remove it
//                     path.files = path.files.filter(x => x != filePath);
//                 } else {
//                     // Add it
//                     path.files.push(filePath);
//                 }
// 			}
// 		}
//         tracker.setMetadata(optumi);
//         this.forceUpdate();
//     }

// 	private handleFilterChange = (e: React.ChangeEvent<HTMLInputElement>) => {
// 		this.setState({filter: e.target.value});
// 	}

//     private generate = () => {
//         const userFiles = this.getList();
//         return this.state.files.filter((value: string) => value.includes(this.state.filter)).map((value) => 
// 			React.cloneElement(
// 				(<ListItem style={{paddingTop: '0px', paddingBottom: '0px'}}>
//                     <Checkbox
//                         checked={userFiles.includes(value)}
//                         onClick={() => this.handleChange(value)}
//                     />
//                     <ListItemText
//                     	primary={value}
//                     />
//                   </ListItem>)
// 			, { key: value }
// 			)
// 		);
//     }

//     public render = (): JSX.Element => {
//         if (Global.shouldLogOnRender) console.log('DirectoryDialogRender (' + new Date().getSeconds() + ')');
//         return (
//             <>
// 				<div style={Object.assign({position: 'relative', width: '18px'}, this.props.style)}>
// 					<IconButton
// 						style={{
// 							position: 'absolute',
// 							left: '-6px',
// 							display: 'inline-block',
// 							width: '24px',
// 							height: '24px',
// 						}}
// 						onClick={this.handleClickOpen}
// 						disabled={!this.state.isDirectory || this.props.disabled}
// 					>
// 						<PopupIcon style={{position: 'relative', top: '-12px'}} />
// 					</IconButton>
// 				</div>
//                 <StyledDialog
// 					open={this.state.open}
// 					onClose={this.handleClose}
//                     scroll='paper'
// 				>
// 					<MuiDialogTitle
//                         disableTypography
//                         style={{
//                             display: 'inline-flex',
//                             backgroundColor: 'var(--jp-layout-color2)',
//                             height: '48px',
//                             padding: '6px',
//                             borderRadius: '4px',
//                         }}
//                     >
//                         <div style={{
// 							width: '100%',
// 							display: 'inline-flex',
//                             fontSize: '16px',
//                             fontWeight: 'bold',
// 							padding: '10px',
// 						}}>
// 							Files under directory '{this.props.path}'
//                         </div>
//                         <IconButton
//                             onClick={this.handleClose}
//                             style={{
//                                 display: 'inline-block',
//                                 width: '36px',
//                                 height: '36px',
//                                 padding: '3px',
//                             }}
//                         >
//                             <CloseIcon
//                                 style={{
//                                     width: '30px',
//                                     height: '30px',
//                                     padding: '3px',
//                                 }}
//                             />
//                         </IconButton>
// 					</MuiDialogTitle>
//                     <ShadowedDivider />
// 					<DialogContent style={{ display: 'flex', flexFlow: 'column', overflow: 'hidden', padding: '6px', width: '100%', height: 'calc(100% - 48px - 2px)' }}>
// 						<div style={{display: 'flex'}}>	
// 							<TextField
// 								size='small'
// 								variant="outlined"
// 								label="Search"
// 								style={{width: '100%', margin: '6px'}}
// 								onChange={this.handleFilterChange}
// 							/>
// 							<Button
// 								variant="contained"
// 								onClick={this.handleSelectAll}
// 								style={{minWidth: '150px', margin: '6px'}}
// 							>
// 								SELECT ALL
// 							</Button>
// 							<Button
// 								variant="contained"
// 								onClick={this.handleDeselectAll}
// 								style={{minWidth: '150px', margin: '6px'}}
// 							>
// 								DESELECT ALL
// 							</Button>
// 						</div>
// 						<span style={{padding: '0px 6px', color: 'rgba(0, 0, 0, 0.54)'}}>
// 							We will upload all selected files. Make sure to deselect the files you want us to ignore.
// 						</span>
// 						<List style={{flexGrow: 1, overflowY: 'auto'}}>
// 							{this.generate()}
// 						</List>
// 					</DialogContent>
// 				</StyledDialog>
//             </>
//         )
// 	}
	
// 	public shouldComponentUpdate = (nextProps: IProps, nextState: IState): boolean => {
// 		try {
// 			if (JSON.stringify(this.props) != JSON.stringify(nextProps)) return true;
// 			if (JSON.stringify(this.state) != JSON.stringify(nextState)) return true;
// 			if (Global.shouldLogOnRender) console.log('SuppressedRender')
// 			return false;
// 		} catch (error) {
// 			return true;
// 		}
// 	}
// }
