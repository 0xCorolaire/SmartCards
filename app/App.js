import React from 'react';
import AppContainer from './Navigation/Navigation'
import { Provider } from 'react-redux'
import Store from './Store/configureStore'


export default class App extends React.Component {
  render() {
    return (
    <Provider store={Store}>
      <AppContainer/>
    </Provider>
    );
  }
}
