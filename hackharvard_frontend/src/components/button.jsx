import 'src/App.css'
import './button.css'

function Button(props) {

  var clickStyle;
  if (props.clickable == true || props.clickable == undefined) {
    clickStyle = "clickable_button";
  } else {
    clickStyle = "unclickable_button"
  }

  return (
    <div id="button_container">
      <div id="inner_button_container" className={clickStyle} onClick={props.onClick}>
        <div id='button_label' className='nohighlight'>
          {props.label}
        </div>
      </div>
    </div>
  )
}

export default Button
