import apirequest from './apiRequest'

export const getPointsFromCards = (success, failure) => {
    console.log("appel API")
    apirequest("apiRequest", 'GET', '/posts/1', null)
    .then(res => res.json())
    .then((result) => {
        success(result)
    },
    error => {
        console.log(error)
        failure(error)
    }).catch((err) => {failure(err)})
}
    
