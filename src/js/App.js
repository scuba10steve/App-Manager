import React from 'react';
import './App.css';
import {AppBar, Switch, TableBody, TableHead, TableRow, Typography} from "@material-ui/core";
import Axios from "axios";
import Grid from "@material-ui/core/Grid";
import List from "@material-ui/core/List";
import ListItemText from "@material-ui/core/ListItemText";
import ListItem from "@material-ui/core/ListItem";
import LabelIcon from '@material-ui/icons/Label';
import AddCircle from '@material-ui/icons/AddCircle';
import ListItemIcon from "@material-ui/core/ListItemIcon";
import Container from "@material-ui/core/Container";
import Table from "@material-ui/core/Table";
import TableCell from "@material-ui/core/TableCell";


class App extends React.Component {
    state = {
        apps: [],
        selected_app: null
    };

    componentDidMount = () => {
        this.loadApps()
    };

    loadApps = () => {
        let that = this;
        Axios.get("/apps").then(function (response) {
            that.setState({
                apps: response.data
            })
        }).catch(function (err) {
            console.log(err)
        })
    };


    displayCreateAppModal = () => {

    };

    selectApp = (app) => {
        this.setState({
            selected_app: app
        });
    };

    handleInstalled = (event) => {
        this.setState({
            selected_app: {
                installed: event.target.value
            },
        })
    };

    render = () => (
        <Container maxWidth="xl" fixed={true} style={{paddingTop: "40px"}}>
            <AppBar color="primary" position="relative" style={{marginBottom: "10px"}}>
                <Typography variant="h5">
                    Application Manager
                </Typography>
            </AppBar>
            <Grid container spacing={3} alignContent="center">
                <Grid item xs={2}>
                    <List>
                        {this.state.apps.map(app =>
                            <ListItem key={app.app_id}
                                      style={this.state.selected_app === app ? {backgroundColor: "crimson"}: {backgroundColor: "aquamarine"}}
                                      onClick={this.selectApp.bind(this, app)}>
                                <ListItemIcon>
                                    <LabelIcon/>
                                </ListItemIcon>
                                <ListItemText key={app.app_id}
                                              primary={app.name}/>
                            </ListItem>
                        )}
                        <ListItem>
                            <ListItemIcon onClick={this.displayCreateAppModal}>
                                <AddCircle/>
                            </ListItemIcon>
                        </ListItem>
                    </List>
                </Grid>
                <Grid item xs={1} style={{backgroundColor: "aqua"}}/>
                <Grid item xs={9}>
                    <Table style={{paddingTop: "40px"}}>
                        <TableHead>
                        </TableHead>
                        <TableBody>
                            {this.state.selected_app && <React.Fragment>
                                <TableRow>
                                    <TableCell/>
                                    <TableCell>
                                        Name
                                    </TableCell>
                                    <TableCell>
                                        Download URL
                                    </TableCell>
                                    <TableCell>
                                        Intended System (OS Family)
                                    </TableCell>
                                    <TableCell>
                                        Installed
                                    </TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell>
                                        {this.state.selected_app.app_id}
                                    </TableCell>
                                    <TableCell>
                                        {this.state.selected_app.name}
                                    </TableCell>
                                    <TableCell>
                                        {this.state.selected_app.source_url}
                                    </TableCell>
                                    <TableCell>
                                        {this.state.selected_app.system}
                                    </TableCell>
                                    <TableCell>
                                        <Switch value={this.state.selected_app.installed} onChange={this.handleInstalled}/>
                                    </TableCell>
                                </TableRow>
                            </React.Fragment>}
                        </TableBody>
                    </Table>
                </Grid>
            </Grid>
        </Container>
    );
}

export default App;
