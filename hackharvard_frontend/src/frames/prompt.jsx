import Button from "src/components/button.jsx"
import "src/App.css"
import "./prompt.css"
import socket from "../socketConfig.jsx";
import {useState} from "react";

function Prompt(props) {

  const [inputText, setInputText] = useState("");

  var inputStyles = {
    "width": "100%",
    "height": "30px",
    "fontSize": "30px"
  };

  function handlePromptSubmit(event) {
    socket.emit("enter_prompt", {
      "prompt": inputText
    })
    console.log("active player prompt submitted");
  }

  function handleChange(e){
    setInputText(e.target.value);
  }

  var promptInfo;
  if (props.info.isActive) {
    promptInfo = "You are the active player! Enter any prompt to describe an image."
  } else {
    promptInfo = "Enter a prompt to visualize the active players clue!"
  }

  return (
    <div id="prompt_container">
      <div id="prompt_info" className="info_text">
        {promptInfo}
      </div>
      <input style={inputStyles} onChange={handleChange} />
      <Button label={"Submit"} onClick={handlePromptSubmit} clickable={inputText.length > 0}></Button>
    </div >
  )
}


export default Prompt
