import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import { socket } from './socket.tsx'

let gameKey = "ANANM";
let thisPlayer = "X";

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App gameKey={ gameKey } thisPlayer={ thisPlayer } socket={ socket }/>
  </React.StrictMode>,
)
