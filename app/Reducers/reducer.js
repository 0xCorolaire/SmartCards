import { combineReducers } from 'redux'
import {
    GET_POINTS_REQUEST,
    GET_POINTS_ERROR,
    GET_POINTS_SUCCESS,
} from '../constants/constants'

function Detector(state = {}, action){
    console.log("Detector reducer")
    switch(action.type){
        case GET_POINTS_REQUEST:
            return state
        
        case GET_POINTS_SUCCESS:
            console.log("reducer : GET_POINTS_SUCCESS")
            state = Object.assign({}, state,{
                nbPoints: action.nbPoints, //ici c'est les data de action donc le même nom
                resImage: action.resImage,
            })
            return state
        
        case GET_POINTS_ERROR:
            console.error('Erreur reducer')
            return state

        default:
            return state
    }
    
}

function Coinche(state = {}, action){
    switch(action.type){
        default:
            return state
    }
    
}

export default combineReducers({
    Detector,
    Coinche,
})