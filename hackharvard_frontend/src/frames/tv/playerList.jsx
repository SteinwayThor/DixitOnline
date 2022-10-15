import { useState } from "react"
import "./playerList.css"

function PlayerList(props) {

    let items = []
    for (let player_name in props.names) {
        items.push(<li key={player_name}>player_name</li>)
    }

    return (
        <div id="container">
            <h2>Players:</h2>
            <div id="playerlist" className="info_text">
                <ul>
                    { items }
                </ul>
            </div>
        </div>
    )
}

export default PlayerList

