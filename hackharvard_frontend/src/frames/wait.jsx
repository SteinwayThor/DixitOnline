import "./wait.css"
import {backend_url} from "../backendUrl";

function WaitingScreen(props) {

  let ims = []
  if(props.info.image){
    ims.push(<img src={backend_url + props.info.image} alt={"Waiting screen"}/>)
  }

  return (
    <div id="wait_container">
      <div id="wait_info" className="info_text">
        {props.info.state}
      </div>
      {ims}
    </div>
  )
}

export default WaitingScreen
