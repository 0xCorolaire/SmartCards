import {
    GET_POINTS_REQUEST,
    GET_POINTS_ERROR,
    GET_POINTS_SUCCESS,
} from '../constants/constants'

import {
    getPointsFromCards
} from '../utils/apiCalls'

export function getPointsRequest(){
    console.log("action getPoints request")
    return {
        type: GET_POINTS_REQUEST,
    }
}

export function getPointsSuccess(data){
    console.log("action getPoinsSuccess")
    return {
        type: GET_POINTS_SUCCESS,
        nbPoints: data.userId,  //ici mettre les data reçues par l'api
        resImage: data.title,
    }
}

export function getPointsError(error){
    console.log("action getPointsError")
    return {
        type: GET_POINTS_ERROR,
        error,
    }
}

export function getPoints(image){
    console.log("action getPoints")
    return (dispatch) => {
        dispatch(getPointsRequest())
        getPointsFromCards((data) =>{
            dispatch(getPointsSuccess(data))
        },
        (error) => {
            dispatch(getPointsError(error))
        })
    }
}