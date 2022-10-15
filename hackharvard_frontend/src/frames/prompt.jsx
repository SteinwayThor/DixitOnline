import Button from "src/components/button.jsx"
import "src/App.css"
import "./prompt.css"

function ActivePlayerPrompt(props) {

  var inputStyles = {
    "width": "100%",
    "height": "30px",
    "fontSize": "30px"
  };

  function handlePromptSubmit() {
    console.log("active player prompt submitted");
  }

  var promptInfo;
  if (props.frameInfo.isActive) {
    promptInfo = "You are the active player!"
  } else {
    promptInfo = "You are a bot, enter a prompt to visualize the active players clue!"
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
