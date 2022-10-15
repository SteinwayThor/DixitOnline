import './App.css'
import RoleSelect from 'src/frames/roleSelect.jsx'
import WaitingScreen from 'src/frames/wait.jsx'
import ActivePlayerPrompt from 'src/frames/active/prompt'
import ActivePlayerClue from 'src/frames/active/clue'
import BotPlayerPrompt from './frames/bot/prompt'
import { useState, useEffect } from 'react'

import socket from './socketConfig'
import PlayerList from "./frames/tv/playerList";
import Vote from "./frames/tv/vote";

function AppTv() {

  const [gameState, setGameState] = useState("player_list");
  const [frameInfo, setFrameInfo] = useState({"names": []});

  useEffect(() => {
    socket.io.on("tv_show_player_list", (msg) => {
      setGameState("player_list");
      setFrameInfo(msg);
    })

    socket.io.on("display_waiting_screen", (msg) => {
      setGameState("wait");
      setFrameInfo(msg);
    })

    socket.io.on("tv_show_cards_vote", (msg) => {
      setGameState("vote");
      setFrameInfo(msg);
    })

  }, []);

  let screen = []
  if(gameState === "player_list"){
    screen.push(<PlayerList key={"playerlist"} names={frameInfo.names}></PlayerList>)
  } else if(gameState === "wait"){
    screen.push(<WaitingScreen key={"waitingscreen"} active={true} info={frameInfo}></WaitingScreen>)
  } else if(gameState === "vote"){
    screen.push(<Vote key={"vote"} card_images={frameInfo.images}></Vote>)
  }

  return (
    <div id="app_frame">
      {screen}
    </div>
  )

}

export default AppTv