import Item from './Item';

import CmcIcon from './CmcLogo';
import {
    DatabaseOutlined,
    ExperimentOutlined,
    DotChartOutlined,
    SettingOutlined,
    // UserOutlined,
    ApiOutlined,
    LogoutOutlined,
} from '@ant-design/icons';

const Nav = () => {
    return (
        <div className="main-div w-[85px] flex flex-col items-center">
            <div className='pt-1'>
                <Item
                    Icon={CmcIcon}
                    color='#005e8f'
                />
            </div>
            <div className='flex flex-col pt-7 space-y-3 h-full'>
                <Item
                    Icon={DatabaseOutlined}
                    title='Датасеты'
                    color='red'
                    href='/datasets/'
                />
                <Item
                    Icon={ExperimentOutlined}
                    title='Классификация'
                    color='green'
                    href='/classification/'
                />
                <Item
                    Icon={DotChartOutlined}
                    title='Сравнение'
                    color='brown'
                    href='/comparison/'
                />
            </div>
            <div className='pb-1 space-y-3'>
                {/* <Item
                    Icon={UserOutlined}
                    title='Пользователь'
                    color='grey'
                /> */}
                <Item
                    Icon={LogoutOutlined}
                    title='Выход'
                    color='grey'
                    href='/login/'
                />
                <Item
                    Icon={SettingOutlined}
                    title='Admin'
                    color='black'
                    href={`${process.env.REACT_APP_SERVER_URL}/admin`}
                    blank
                />
                <Item
                    Icon={ApiOutlined}
                    title='API'
                    color='black'
                    href={`${process.env.REACT_APP_SERVER_URL}/docs`}
                    blank
                />
            </div>
        </div>
    )
}

export default Nav;