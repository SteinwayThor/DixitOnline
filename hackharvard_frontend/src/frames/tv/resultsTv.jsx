import { useState } from "react"
import "./resultsTv.css"

function TvResultsOneImage(props) {
  let card_image_class = "card_image";
  if(props.active){
    card_image_class += " card_image_active"
  }
  return (
      <div className="card_results">
        <div className={card_image_class}>
          <img src={props.image} alt={"Card Image"} />
        </div>
        <div className={"card_info"}>
          <div className={"author"}>
            {props.author}
          </div>
          <div className={"prompt"}>
            {props.prompt}
          </div>
          <div className={"voters"}>
            {
              props.votes.map((v)=>{
                <div className={"voter"} key={v}>{v}</div>
              })
            }
          </div>
        </div>
      </div>
  )
}

function TvLeaderboard(props) {
  return (
      <div id="results_leaderboard">
        {props.players.map((p)=> {
          <div key={p.name} className={"player_result"}>
            {p.name}: {p.total_score}({p.round_score})
          </div>
            })}
      </div>);
}

function TvResults(props) {

    let items = []
    for (let card in props.images) {
        items.push(<TvResultsOneImage key={card.image} active={card.is_active_player} image={card.image} votes={card.votes}></TvResultsOneImage>)
    }

    return (
        <div id="container">
            <div id="tv_results">
              <div id="results_cards">
                items
              </div>
              <TvLeaderboard players={props.players}>
              </TvLeaderboard>
            </div>
        </div>
    )
}

export default TvResults

