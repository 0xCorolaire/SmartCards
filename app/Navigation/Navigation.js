import React from 'react'
import { createStackNavigator, createAppContainer} from 'react-navigation'
import Menu from '../Components/Menu'
import Main from '../Components/Main'

const MenuStackNavigator = createStackNavigator({
    Menu: {
        screen: Menu,
        navigationOptions: {
            title: 'Cards Assistant',
            headerTintColor: '#16a085',
            headerTitleStyle: {
                fontWeight: 'bold',
            }
        },
    },
    Main:{
        screen: Main,
        navigationOptions: {
            title: 'Cards Assistant',
            headerTintColor: '#16a085',
            headerTitleStyle: {
                fontWeight: 'bold',
            },
        },
    },
})

const AppContainer = createAppContainer(MenuStackNavigator)

export default AppContainer