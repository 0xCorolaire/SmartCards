import { createStore, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import SmartCards from '../Reducers/reducer'

const initialStore= {
    Detector: {
        resImage: null,
        nbPoints: null
    },
    Coinche: {
        nbPlayer: 4,
    }
}



export default Store = createStore(
    SmartCards,
    initialStore,
    applyMiddleware(thunk),
)