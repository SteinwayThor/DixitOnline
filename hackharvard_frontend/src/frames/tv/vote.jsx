import { useState } from "react"
import {backend_url} from "../../backendUrl.jsx";
import "./vote.css"

function TvVote(props) {

    let items = []
    for (let card in props.info.images) {
        items.push(
            <div className="card_image">
              <img src={backend_url + props.info.images[card]} alt={"Card"} key={card}/>
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

