import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Input, message } from 'antd';
import { EyeInvisibleOutlined, EyeTwoTone } from '@ant-design/icons';
import cookie from 'js-cookie';

import CmcIcon from '../../components/Page/Nav/CmcLogo';

const LoginPage = () => {
    const [login, setLogin] = useState('');
    const [password, setPassword] = useState('');

    const navigate = useNavigate();


    const handleChangeLogin = event => {
        setLogin(event.target.value);
    };

    const handleChangePassword = event => {
        setPassword(event.target.value);
    };

    const handleSubmit = async event => {
        event.preventDefault();

        try {
            const fetcher = await fetch(`${process.env.REACT_APP_SERVER_URL}/users/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    login: login,
                    password: password,
                }),
            });
            if (fetcher.ok) {
                const { token } = await fetcher.json();
                cookie.set('token', token);
                navigate('/datasets/');
            } else {
                message.error('Неверный логин или пароль')
            }

        } catch (error) {
            message.error('Сервер недоступен')
            console.error('Fetcher failure: ', error);
        }
    };


    useEffect(() => {
        const keyDownHandler = event => {
            if (event.key === 'Enter') {
                event.preventDefault();
                if(login !== '' && password !== '')
                    handleSubmit(event)
            }
        };

        document.addEventListener('keydown', keyDownHandler);

        return () => {
            document.removeEventListener('keydown', keyDownHandler);
        };
    }, [login, password]);




    return (
        <div className="flex flex-col justify-center items-center h-screen">

            <div className="main-div flex flex-col h-56 xl:w-3/12 lg:w-5/12 md:w-6/12">
                <div className='flex pb-2 justify-center'>
                    <CmcIcon className='m-1 text-5xl' />
                    <h1 className="px-5 py-4 text-2xl text-primary text-center">
                        Вход в систему
                    </h1>
                </div>
                <div className='px-10 space-y-3 h-full'>
                    <Input
                        placeholder="Логин"
                        value={login}
                        onChange={handleChangeLogin}
                    />
                    <Input.Password
                        placeholder="Пароль"
                        value={password}
                        onChange={handleChangePassword}
                        iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
                    />
                </div>
                <div className='py-2 flex justify-center'>
                    <Button
                        color='red'
                        disabled={!login || !password}
                        onClick={handleSubmit}
                    >
                        Войти
                    </Button>
                </div>
            </div>
        </div>
    )
}

export default LoginPage;


