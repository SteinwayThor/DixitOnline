import "src/App.css"
import "./clue.css"

import Button from "src/components/button.jsx"

function ActivePlayerClue(props) {

    var inputStyles = {
        "width": "100%",
        "height": "30px",
        "fontSize": "30px",
        // "border": "none",
        // "outline": "none"
    };

    function handleAPCDone() {
        console.log('Done sharing clue');
    }

    return (
        <div id="container">
            <div id="apc_info" className="info_text">
                {"You are the active player."}
                <br />
                {"Share your clue with the other players!"}
            </div>
            <Button label="Done" onClick={handleAPCDone} />
        </div >
    )
}

export default ActivePlayerClue
