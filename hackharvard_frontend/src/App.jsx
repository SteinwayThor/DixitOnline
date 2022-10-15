import './App.css'
import socket from './socketConfig'

import ActivePlayerClue from 'src/frames/active/clue'
import RoleSelect from 'src/frames/roleSelect.jsx'
import WaitingScreen from 'src/frames/wait.jsx'
import PlayerResults from 'src/frames/playerResults'

import { useEffect, useState } from 'react'
import BotVote from './frames/bot/vote'

function App() {
  const [gameState, setGameState] = useState("role_select");
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

    socket.io.on("player_display_results", (msg) => {
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

    socket.io.on("tv_display_results", (msg) => {
      setGameState("tv_results");
      setFrameInfo(msg);
    })
  }, []);


  // ajsdkjalskdjalksjdlakjsdlkajsdlkjaslkdjaslkdjalskdjalksdjaslkdjalskdjalskdjalskdjaslkdj

  if (gameState == "role_select") {
    return (
      <div id="app_frame">
        <RoleSelect info={frameInfo} />
      </div>
    )
  }

  if (gameState == "wait") {
    return (
      <div id="app_frame">
        <WaitingScreen info={frameInfo} />
      </div>
    )
  }

  if (gameState == "active_player_clue") {
    return (
      <div id="app_frame">
        <ActivePlayerClue info={frameInfo} />
      </div>
    )
  }

  if (gameState == "bot_vote") {
    return (
      <div id="app_frame">
        <BotVote info={frameInfo} />
      </div>
    )
  }

  if (gameState == "prompt") {
    return (
      <div id="app_frame">
        <Prompt info={frameInfo} />
      </div>
    )
  }

  if (gameState == "player_results") {
    return (
      <div id="app_frame">
        <PlayerResults info={frameInfo} />
      </div>
    )
  }





}

export default App