import Button from "src/components/button.jsx"
import "src/App.css"
import "./prompt.css"
import socket from "../socketConfig.jsx";

function ActivePlayerPrompt(props) {

  var inputStyles = {
    "width": "100%",
    "height": "30px",
    "fontSize": "30px"
  };

  function handlePromptSubmit(event) {
    socket.io.emit("enter_prompt", {
      "prompt": event.target.value
    })
    console.log("active player prompt submitted");
  }

  var promptInfo;
  if (props.frameInfo.isActive) {
    promptInfo = "You are the active player! Enter any prompt to describe an image."
  } else {
    promptInfo = "Enter a prompt to visualize the active players clue!"
  }

  if (props.active) {
    return (
      <div id="container">
        <div id="prompt_info" className="info_text">
          {promptInfo}
        </div>

        <input style={inputStyles} onSubmit={handlePromptSubmit} />
      </div >
    )
  }

}

export default ActivePlayerPrompt
