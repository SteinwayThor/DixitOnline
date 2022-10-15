import { useState } from "react"
import "./vote.css"

function TvVote(props) {

    let items = []
    for (let card in props.card_images) {
        items.push(
            <div className="card_image">
              <img src={card} alt={"Card"} key={card}/>
            </div>);
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

