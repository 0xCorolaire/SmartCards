import React, {Component} from 'react'
import { Button ,StyleSheet, Image, View, Text } from 'react-native'
import ImagePicker from 'react-native-image-picker'
import { connect } from 'react-redux'
import { getPoints } from '../actions/actions'

class TakePhoto extends Component{

    constructor(props){
        super(props)
    this._photoClicked = this._photoClicked.bind(this)
    }


    _displayImage(){
        console.log("display image")
        if(this.props.resImage){
            return(
                <View>
                <Text>{this.props.nbPoints}</Text>
                <Text>{this.props.resImage}</Text>
                </View>
            )
        }
    }
    

    _photoClicked(){
        const {getPoints} = this.props
          ImagePicker.showImagePicker({}, (response)=>{
            if(response.didCancel){
                console.log('L\'utilisateur a annulé')
            }
            else if(response.error){
                console.log('Erreur : ', response.error)
            }
            else {
                const image = {
                    uri: response.uri,
                    name: response.fileName,
                    type: response.type,
                }
                console.log("photoclicked")
                getPoints(image)
            }
        })
    }

    render(){
            return(
                <View style={styles.main_container}>
                    {this._displayImage()}
                    <Button
                        onPress={this._photoClicked}
                        title="Envoyer le jeu"
                    />
                </View>
            )
    }
}


const styles = StyleSheet.create({
    Image: {
        height: 100,
        width: 100,
    },
    main_container:{
        flex: 1
    }
})

let mapStateToProps = (state) => {
    return{
        nbPoints: state.Detector.nbPoints || null,
        resImage: state.Detector.resImage || null,
    }
}

let mapDispatchToProps = (dispatch) => {
    return{
        getPoints: (img) => dispatch(getPoints(img)),
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(TakePhoto)