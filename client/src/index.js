import React, { useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import {
    createBrowserRouter,
    RouterProvider,
    useNavigate,
} from "react-router-dom";

import './index.css';
import { TitleProvider } from './components/TitleContext';


import Fabric from './fabric';

import LoginPage from './pages/login';

import DatasetsPage from './pages/datasets';
import DatasetsInfoPage from './pages/datasets/[id]';


import ClassificationPage from './pages/classification';
import ClassificationViewPage from './pages/classification/[hash]';
import ComparisonPage from './pages/comparison';
import ComparisonReportPage from './pages/comparison/report';


const Test = () => {
    const navigate = useNavigate(); 
    useEffect(() => {
        navigate('/datasets/')
    })
    
    return (
        <></>
    )
}



const router = createBrowserRouter([
    {
        path: '/',
        element: <Test />,
    },
    {
        path: '/login/',
        element: <LoginPage />,
    },
    {
        path: "/fabric/",
        element: <Fabric />,
    },
    {
        path: "/datasets/",
        element: <DatasetsPage />,
    },
    {
        path: "/datasets/:id",
        element: <DatasetsInfoPage />,
    },
    {
        path: "/classification/",
        element: <ClassificationPage />,
    },
    {
        path: "/classification/:hash/",
        element: <ClassificationViewPage />,
    },
    {
        path: "/comparison/",
        element: <ComparisonPage />,
    },
    {
        path: "/comparison/report",
        element: <ComparisonReportPage />,
    },
]);


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <TitleProvider>
            <RouterProvider router={router} />
        </TitleProvider>
    </React.StrictMode>
);

