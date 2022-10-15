import 'src/App.css'
import './button.css'

function Button(props) {

  return (
    <div id="button_container">
      <div id="inner_button_container" onClick={props.onClick}>
        <div id='button_label' className='nohighlight'>
          {props.label}
        </div>
      </div>
    </div>
  )
}

export default Button
