import { io } from 'socket.io-client';

let sockets = {}

export const getSocket = function(gameKey){
  let args = {query: {gameKey}}
  if(sockets[gameKey] === undefined){
    sockets[gameKey] = process.env.NODE_ENV === 'production' ?
              io(args) :
              io('http://localhost:5000', args)
  }
  return sockets[gameKey];
}