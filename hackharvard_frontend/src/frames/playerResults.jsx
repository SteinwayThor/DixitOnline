import 'src/App.css'
import "./playerResults.css"

// player_display_results
// {
//    is_active_player: bool
//    result: "everybody"|"split"|"nobody",
//    guessed_active_player: bool,
//    num_bonus_votes: int
//    player_round_score : int,
//    Player_total_score: int
// }


function PlayerResults(props) {
    var result_banner;
    if (props.info.result == "everybody") {
        result_banner = "Everybody guessed the image!";
    }
    else if (props.info.result == "nobody") {
        result_banner = "Nobody guessed the image!";
    }
    else if (props.info.result == "split") {
        if (props.info.is_active_player) {
            result_banner = "Split guess!";
        }
        else if (props.info.guessed_active_player) {
            result_banner = "You got it!";
        }
        else {
            result_banner = "L";
        }

    }

    return (
        <div id="player_results_container">
            <div id="pr_game_result">
                {result_banner}
            </div>
            <div id="pr_round_score">
                round score: <bold>{props.info.player_round_score}</bold>
            </div>
            <div id="pr_total_score">
                total score: <bold>{props.info.player_total_score}</bold>
            </div>
        </div>
    )
}

export default PlayerResults