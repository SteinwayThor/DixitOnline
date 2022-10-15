import './App.css'
import RoleSelect from 'src/frames/roleSelect.jsx'
import WaitingScreen from 'src/frames/wait.jsx'
import ActivePlayerPrompt from 'src/frames/active/prompt'
import ActivePlayerClue from 'src/frames/active/clue'
import BotPlayerPrompt from './frames/bot/prompt'
import { useState } from 'react'

function App() {

  const [gameState, changeGameState] = useState(0);

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