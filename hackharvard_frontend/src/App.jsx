import './App.css'
import socket from './socketConfig'

import ActivePlayerPrompt from 'src/frames/active/prompt'
import RoleSelect from 'src/frames/roleSelect.jsx'
import WaitingScreen from 'src/frames/wait.jsx'
import BotPlayerPrompt from './frames/bot/prompt'

import { useEffect, useState } from 'react'

function App() {

  const [gameState, setGameState] = useState("roleSelect");
  const [frameInfo, setFrameInfo] = useState({});

  useEffect(() => {
    socket.io.on("display_waiting_screen", (msg) => {
      setGameState("wait");
      setFrameInfo(msg);
    });

    socket.io.on("display_active_player_ok", (msg) => {
      setGameState("active_player_clue");
      setFrameInfo(msg);
    });

    socket.io.on("display_vote", (msg) => {
      setGameState("bot_vote");
      setFrameInfo(msg);
    })

    socket.io.on("display_prompt", (msg) => {
      setGameState("prompt");
      setFrameInfo(msg);
    })

    socket.io.on("display_results", (msg) => {
      setGameState("player_results");
      setFrameInfo(msg);
    })

    socket.io.on("tv_show_player_list", (msg) => {
      setGameState("lobby");
      setFrameInfo(msg);
    })

    socket.io.on("tv_show_cards_vote", (msg) => {
      setGameState("tv_vote");
      setFrameInfo(msg);
    });

    socket.io.on("tv_show_results", (msg) => {
      setGameState("tv_results");
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