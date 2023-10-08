import { io } from 'socket.io-client';

let socket = {}

export const getSocket = function(gameKey){
  if(socket[gameKey] === undefined){
    socket[gameKey] = process.env.NODE_ENV === 'production' ?
              io() :
              io('http://localhost:5000')
  }
  return socket[gameKey];
}