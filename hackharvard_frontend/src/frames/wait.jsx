import "./wait.css"
import {backend_url} from "../backendUrl";

function WaitingScreen(props) {

  return (
    <div id="wait_container">
      <div id="wait_info" className="info_text">
        {props.info.state}
      </div>
      <img src={backend_url + props.info.image} />
    </div>
  )
}

export default WaitingScreen
