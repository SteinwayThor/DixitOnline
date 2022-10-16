import "src/App.css"
import Button from "../../components/button.jsx";
import socket from "../../socketConfig.jsx";

function BotVote(props) {
  let vote_buttons = []

  function voteFor(num){
    socket.emit("vote", {"vote": num})
  }

  for(let i = 0; i < props.info.number; i++){
    vote_buttons.push(
        <Button id="votes" key={i} label={i} onClick={()=>voteFor(i)} clickable={true}></Button>
    )
  }
    return (
        <div id="vote_container">
          {vote_buttons}
        </div>
    )
}

export default BotVote