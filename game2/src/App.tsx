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

  const [currentPlayer, setCurrentPlayer] = useState('')
  const [board, setBoard] = useState([])
  const [bigWinner, setBigWinner] = useState('')

  useEffect(getConnectionEffect(setIsConnected, socket), []);

  socket.on('game_data', (newGameData:any) => {
    setCurrentPlayer(newGameData.current_player);
    setBoard(newGameData.board)
    setBigWinner(newGameData.big_winner);
  });

  let makeMove = (coords: Array<number>) => {
    socket.emit("make-move", {gameKey, coords})
    return null;
  }

  let reset = () => {
    let message = "Reset game?";
    if(confirm(message)){
      socket.emit("reset", {gameKey})
    }
    return null;
  }

  let gameContextValue = {
    makeMove,
    reset,
    thisPlayer,
    currentPlayer
  };

  let gameInContext = (
    <GameContext.Provider value={gameContextValue}>
      <Game gameKey={gameKey} thisPlayer={thisPlayer} currentPlayer={currentPlayer}
            board={board} bigWinner={bigWinner} />
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
      <GameKey gameKey={ gameKey} bigWinner={ bigWinner } />
      <Board board={ board } bigWinner={ bigWinner }/>
    </>
  )
}

function Turn({ thisPlayer, currentPlayer }: any){
  return (
    <h1>You: { thisPlayer } - Turn: { currentPlayer }</h1>
  )
}

function GameKey({ gameKey, bigWinner }: any){

  const {reset}:any = useContext(GameContext);

  let buttonText = bigWinner ? "Reset" : "Rage Quit"

  return (
    <div>
      Game Key: <input readOnly disabled value={ gameKey } />
      <button type="button" onClick={reset}>
        { buttonText }
      </button>
    </div>
  )
}

function Board({ board, bigWinner }: any){
  return (
    <div id="big-board-wrapper">
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
      <BigBoardWinner player={bigWinner} />
    </div>
  )
}

function SmallBoardWinner({ player }:any){
  if(!player){return;}
  return (
    <div className="small-board-winner">
      { player }
    </div>
  )
}

function BigBoardWinner({ player }:any){
  if(!player){return;}
  return (
    <div className="big-board-winner">
      { player }
    </div>
  )
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
