import { API_URL } from './config'

const apirequest = (server, method, request, data = null) => {
  let url;
  switch (server) {
    case 'apiRequest':
      if(data !== null){
        url = API_URL + request + data
      }else{
        url = API_URL + request
      }
      /* url = data !== null
        ? ${API_URL + request}/${data}
        : ${API_URL + request}; */
      return fetch(
        url,
        {
          method,
          /* headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          }, */
        },
      );

    default:
        break;
  }
};

export default apirequest;