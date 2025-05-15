import { Link } from 'react-router-dom';
import { Tooltip } from "antd";

const Item = ({ Icon, title, color, href, blank=false }) => {
    const target = blank ?  '_blank' : ''
    return (
        <Tooltip title={title} arrow={false} placement="right">
            <div className="nav-item flex" style={{'borderColor': color}}>
                <Link to={href} target={target}>
                    <Icon style={{color: color}}/>
                </Link>
            </div>
        </Tooltip>
    )
}

export default Item;