import { useState } from "react"
import "./vote.css"

function TvVote(props) {

    let items = []
    for (let card in props.card_images) {
        items.push(<img src={card} alt={"Card"} key={card}/>)
    }

    return (
        <div id="container">
            <div id="tvvote_info" className="info_text">
                items
            </div>
        </div>
    )
}

export default TvVote

