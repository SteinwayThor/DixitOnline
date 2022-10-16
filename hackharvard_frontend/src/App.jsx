import './App.css'
import socket from './socketConfig'

import ActivePlayerClue from 'src/frames/active/clue'
import RoleSelect from 'src/frames/roleSelect.jsx'
import WaitingScreen from 'src/frames/wait.jsx'
import PlayerResults from 'src/frames/playerResults'
import Prompt from 'src/frames/prompt.jsx';

import { useEffect, useState } from 'react'
import BotVote from './frames/bot/vote'

function App() {
  const [gameState, setGameState] = useState("role_select");
  const [frameInfo, setFrameInfo] = useState({});

  useEffect(() => {
    socket.on("display_waiting_screen", (msg) => {
      console.log("Display waiting")
      setGameState("wait");
      setFrameInfo(msg);
    });

    socket.on("display_active_player_ok", (msg) => {
      console.log("Display active player ok")
      setGameState("active_player_clue");
      setFrameInfo(msg);
    });

    socket.on("display_vote", (msg) => {
      console.log("Display vote")
      setGameState("bot_vote");
      setFrameInfo(msg);
    })

    socket.on("display_prompt", (msg) => {
      console.log("Display prompt")
      setGameState("prompt");
      setFrameInfo(msg);
    })

    socket.on("player_display_results", (msg) => {
      console.log("Display player results")
      setGameState("player_results");
      setFrameInfo(msg);
    })

    socket.on("tv_show_player_list", (msg) => {
      console.log("Tv show player list");
      setGameState("lobby");
      setFrameInfo(msg);
    })

    socket.on("tv_show_cards_vote", (msg) => {
      console.log("Tv show cards vote");
      setGameState("tv_vote");
      setFrameInfo(msg);
    });

    socket.on("tv_display_results", (msg) => {
      console.log("Tv display results");
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