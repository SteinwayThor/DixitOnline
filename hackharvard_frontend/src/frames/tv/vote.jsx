import { useState } from "react"
import {backend_url} from "../../backendUrl.jsx";
import "./vote.css"

function TvVote(props) {

    let items = []
    for (let card in props.images) {
        items.push(
            <div key={card} className="card_image">
              <img src={backend_url + props.images[card]} alt={"Card"}/>
            </div>);
    }

    return (
        <div id="container">
            <div id="tvvote_info" className="info_text">
              {items}
            </div>
        </div>
    )
}

export default TvVote

