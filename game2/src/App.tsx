import { useState, useEffect } from 'react';
import './App.css'

function getConnectionEffect(setIsConnected: any, socket: any){
  return () => {
    function onConnect() {
      setIsConnected(true);
    }

    function onDisconnect() {
      setIsConnected(false);
    }

    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);

    return () => {
      socket.off('connect', onConnect);
      socket.off('disconnect', onDisconnect);
    };
  }
}

function App({ gameKey, thisPlayer, socket }: any) {

  const [isConnected, setIsConnected] = useState(socket.connected);
  const [gameData, setGameData] = useState<any>({})

  useEffect(getConnectionEffect(setIsConnected, socket), []);

  socket.on('game_data', (gameData:any)=>{
    setGameData(gameData);
  })

  return isConnected ?
         Game(gameKey, thisPlayer, gameData.current_player, gameData.board, gameData.big_winner) :
         Loading();
}

function Loading(){
  return (
    <div>Loading...</div>
  )
}

function Game(gameKey, thisPlayer, currentPlayer, board, bigWinner){
  return (
    <>
      <Turn thisPlayer={thisPlayer} currentPlayer={currentPlayer} />
      <GameKey gameKey={ gameKey} />
      <Board boardData={ board } />
    </>
  )
}

function Turn({ thisPlayer, currentPlayer }: any){
  return (
    <h1>You: { thisPlayer } - Turn: { currentPlayer }</h1>
  )
}

function GameKey({ gameKey }: any){
  return (
    <form action="reset" method="POST" id="reset-form">
      Game Key: <input readOnly disabled value={ gameKey } />
      <button type="submit">
          Rage Quit
      </button>
    </form>
  )
}

function Board({ boardData }: any){
  return (
    <div>board data</div>
  )
}

export default App
