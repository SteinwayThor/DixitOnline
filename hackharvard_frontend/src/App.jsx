import './App.css'
import RoleSelect from 'src/frames/roleSelect.jsx'
import WaitingScreen from 'src/frames/wait.jsx'
import ActivePlayerPrompt from 'src/frames/active/prompt'
import ActivePlayerClue from 'src/frames/active/clue'
import BotPlayerPrompt from './frames/bot/prompt'
import { useState } from 'react'

import socket from './socketConfig'

function App() {

  const [gameState, setGameState] = useState("roleSelect");
  const [frameInfo, setFrameInfo] = useState({});

  useEffect(() => {
    socket.io.on("display_waiting_screen", (msg) => {
      setGameState("wait");
      setFrameInfo(msg);
    })

    socket.io.on("display_active_player_ok", (msg) => {
      setGameState("active_player_clue");
      setFrameInfo(msg);
    })

  }, []);



  return (
    <div id="app_frame">

      <RoleSelect active={false} />
      <WaitingScreen active={false} />
      <ActivePlayerPrompt active={false} />
      <ActivePlayerClue active={false} />
      <BotPlayerPrompt active={true} />

    </div>
  )

}

export default App