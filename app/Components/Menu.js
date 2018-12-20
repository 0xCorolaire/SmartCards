import React from 'react'
import {Button, StyleSheet, Text, View } from 'react-native'

class Menu extends React.Component{

    render(){
        console.log('render')
        return(
            <View style={styles.main_container}>
                <View style={styles.text_container}>
                <Text style={styles.title}>Guide d'utilisation</Text>
                <Text style={styles.guide}>1. Selectionne le joueur qui commence.</Text>
                <Text style={styles.guide}>2. Entre les différentes annonces.</Text>
                <Text style={styles.guide}>3. Prend en photo ton jeu.</Text>
                <Text style={styles.guide}>4. Fait le meilleur choix !</Text>
                </View>
                <View style={styles.button_container}>
                <View style={styles.bouton}>
                <Button
                    onPress={()=>{this.props.navigation.navigate('Main')}}
                    title="Nombre de points"
                    color="#1abc9c"
                />
                </View>
                <View style={styles.bouton}>
                <Button
                    onPress={()=>{console.log("bouton")}}
                    title="Crédits"
                    color="#1abc9c"
                />
                </View>
                </View>
            </View>
        )
    }
}

const styles = StyleSheet.create({
    main_container: {
        flex: 1,
        backgroundColor: '#27ae60',
        
    },
    bouton: {
        marginTop: 30
        
    },
    guide: {
        color: '#FFFFFF',
        marginTop: 10,
    },
    title: {
        color: '#FFFFFF',
        fontWeight: 'bold',
        marginTop: 20,
    },
    text_container: {
        flex: 2,
        alignItems: 'center',
    },
    button_container: {
        flex: 1,
    }
})

export default Menu