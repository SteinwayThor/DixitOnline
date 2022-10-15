import "./wait.css"

function WaitingScreen(props) {

  return (
    <div id="wait_container">
      <div id="wait_info" className="info_text">
        {"waiting :)"}
      </div>
      <img src={"https://pbs.twimg.com/media/Eo35eTdUwAEFmHg.jpg"} />
    </div>
  )
}

export default WaitingScreen
