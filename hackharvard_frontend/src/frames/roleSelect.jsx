import 'src/App.css'
import './roleSelect.css'
import Button from 'src/components/button'

function RoleSelect(props) {

    function handleHostSelect(role) {
        console.log(`HOST role selected`)
    }

    function handlePlayerSelect(role) {
        console.log(`PLAYER role selected`)
    }

    return (
        <div id="rs_container">
            <div id="rs_info_text" className='info_text'>
                Choose your role!
            </div>
            <Button label={"Host"} onClick={handleHostSelect} />
            <Button label={"Player"} onClick={handlePlayerSelect} />
        </div>
    )
}

export default RoleSelect