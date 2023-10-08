import { useState, useEffect, createContext, useContext } from 'react';

const GameContext = createContext({});

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
  });

  let makeMove = (coords: Array<number>) => {
    socket.emit("make-move", {gameKey, coords})
    return null;
  }

  let gameContextValue = {makeMove, thisPlayer, currentPlayer: gameData.current_player};

  let gameInContext = (
    <GameContext.Provider value={gameContextValue}>
      <Game gameKey={gameKey} thisPlayer={thisPlayer} currentPlayer={gameData.current_player}
            board={gameData.board} bigWinner={gameData.big_winner} />
    </GameContext.Provider>
  )

  return isConnected ?
         gameInContext :
         <Loading />;
}

function Loading(){
  return (
    <div>Loading...</div>
  )
}

function Game({gameKey, thisPlayer, currentPlayer, board, bigWinner}: any){
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
  return (
    <table className="big-table">
      <tbody>
        {board.map((bigRow:any, bigRowIndex:number) => (
          <tr key={bigRowIndex} className="big-tr">
            {bigRow.map((bigCol:any, bigColIndex:number) => (
              <td key={bigColIndex} className="big-td">
                <SmallBoardWinner player={bigCol.winner} />
                <SmallBoard smallRows={bigCol.small_board} bigRowIndex={bigRowIndex} bigColIndex={bigColIndex} />
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

function SmallBoard({ smallRows, bigRowIndex, bigColIndex }:any){
  return (
    <table className="small-table">
      <tbody>
        {smallRows.map((smallRow:any, smallRowIndex:number) => (
          <tr key={smallRowIndex} className="small-tr" >
            {smallRow.map((smallSquareData:any, smallColIndex:number) => (
              <SmallSquare key={smallColIndex} coords={[bigRowIndex,bigColIndex,smallRowIndex,smallColIndex]} {...smallSquareData} />
            ))}
          </tr>
        ))}
      </tbody>
    </table>
    
  )
}

function SmallSquare({player, coords, move_is_legal}: any){
  let innerContent = player ? player : <MoveButton moveIsLegal={move_is_legal} coords={coords} />
  return (
    <td>{ innerContent }</td>
  )
}


function MoveButton({moveIsLegal, coords}: any){

  const {makeMove, thisPlayer, currentPlayer}:any = useContext(GameContext);

  if(!moveIsLegal){return <div></div>}

  let onClick = () => {makeMove(coords);}

  let enabled = thisPlayer == currentPlayer;

  return enabled ?
    (<button onClick={onClick} className="go-button">Go</button>) :
    (<button disabled={true} className="go-button">Go</button>) ;
}

export default App
