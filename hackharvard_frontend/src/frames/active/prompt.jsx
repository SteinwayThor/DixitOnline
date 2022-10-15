import Button from "src/components/button.jsx"
import "src/App.css"
import "./prompt.css"

function ActivePlayerPrompt(props) {

  var inputStyles = {
    "width": "100%",
    "height": "30px",
    "fontSize": "30px"
  };

  function handleAPPSubmit() {
    console.log("active player prompt submitted");
  }

  if (props.active) {
    return (
      <div id="container">
        <div id="app_info" className="info_text">
          {"You are the active player."}
          <br />
          {"Input an image prompt."}
        </div>

        <input style={inputStyles} onSubmit={handleAPPSubmit} />
      </div >
    )
  }

}

export default ActivePlayerPrompt
