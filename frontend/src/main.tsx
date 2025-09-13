import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import { getSocket } from './socket.tsx'

function trim(str: string, ch: string) {
  var start = 0, 
      end = str.length;

  while(start < end && str[start] === ch)
      ++start;

  while(end > start && str[end - 1] === ch)
      --end;

  return (start > 0 || end < str.length) ? str.substring(start, end) : str;
}

let path = trim(window.location.pathname, '/')
let pathParts = path.split('/')

let gameKey = pathParts[0];
let thisPlayer = pathParts[1];

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App gameKey={ gameKey } thisPlayer={ thisPlayer } getSocket={ getSocket }/>
  </React.StrictMode>,
)
