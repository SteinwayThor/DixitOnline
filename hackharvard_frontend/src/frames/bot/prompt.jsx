import Button from "src/components/button.jsx"
import "src/App.css"
import "./prompt.css"

function BotPlayerPrompt(props) {

    var inputStyles = {
        "width": "100%",
        "height": "30px",
        "fontSize": "30px"
    };

    function handleBPPSubmit() {
        console.log("bot player prompt submitted");
    }

    if (props.active) {
        return (
            <div id="container">
                <div id="bpp_info" className="info_text">
                    {"Enter a prompt to mimic the active players clue."}
                    <br />
                    {"Input an image prompt."}
                </div>

                <input style={inputStyles} onSubmit={handleBPPSubmit} />
            </div >
        )
    }

}

export default BotPlayerPrompt
