import { useState, useEffect } from 'react';

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

  socket.on('game_data', (newGameData:any)=>{
    setGameData(newGameData);
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
      <Board board={ board } />
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

function Board({ board }: any){
  console.log(board)
  return (
    <table className="big-table">
      <tbody>
        {board.map((bigRow:any, bigRowIndex:number) => (
          <tr key={bigRowIndex} className="big-tr">
            {bigRow.map((bigCol:any, bigColIndex:number) => (
              <td key={bigColIndex} className="big-td">
                <SmallBoardWinner player={bigCol.winner} />
                <SmallBoard smallRows={ bigCol.small_board } />
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )
}

function SmallBoardWinner({ player }:any){
  if(player){
    return (
      <div className="small-board-winner">
        { player }
      </div>
    )
  } else {
    return (<></>)
  }
}

function SmallBoard({ smallRows }:any){
  return (
    <table className="small-table">
      <tbody>
        {smallRows.map((smallRow:any, smallRowIndex:number) => (
          <tr key={smallRowIndex} className="small-tr" >
            {smallRow.map((smallSquareData:any, smallColIndex:number) => (
              <SmallSquare key={smallColIndex} {...smallSquareData} />
            ))}
          </tr>
        ))}
      </tbody>
    </table>
    
  )
}

function SmallSquare({player, move_is_legal}: any){
  let innerContent = player ? player : <MoveButton moveIsLegal={move_is_legal} />
  return (
    <td>{ innerContent }</td>
  )
}

function MoveButton({moveIsLegal}: any){
  let disabled = !moveIsLegal;
  return (
    <button disabled={disabled}>Go</button>
  )
}

export default App
