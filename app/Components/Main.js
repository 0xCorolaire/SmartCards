import React from 'react'
import {Button, StyleSheet, Text, View } from 'react-native'
import TakePhoto from '../Components/TakePhoto'

class Main extends React.Component{

    render(){
        console.log('render')
        return(
            <View style={styles.main_container}>
                <Text>Votre main</Text>
                <TakePhoto/>
            </View>
        )
    }
}

const styles = StyleSheet.create({
    main_container: {
        flex: 1,
        alignItems: 'center',
        backgroundColor: '#27ae60',
        justifyContent: 'center'
    },
})

export default Main