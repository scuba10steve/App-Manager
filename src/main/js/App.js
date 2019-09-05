import React from 'react';
import './App.css';
import {AppBar, Container, GridList, GridListTile, Typography} from "@material-ui/core";
import Axios from "axios";


class App extends React.Component {
    state = {
        apps: []
    };

    componentDidMount = () => {
        this.loadApps()
    };

    loadApps = () => {
        let that = this;
        Axios.get("/apps").then(function(response) {
            that.setState({
                apps: response.data
            })
        }).catch(function(err) {
            console.log(err)
        })
    };


  render = () => (
    <div className="App">
      <Container>
                <AppBar color="primary">
                    <Typography variant="h6">
                        Application Manager
                    </Typography>
                </AppBar>
                <GridList>
                    <GridListTile>
                        { this.state.apps.map( app => <div key={app.app_id}>{app.name}</div> )}
                    </GridListTile>
                </GridList>
            </Container>
    </div>
  );
}

export default App;
