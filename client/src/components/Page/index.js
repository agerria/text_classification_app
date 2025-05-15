import React, { useContext, useEffect } from "react";
import Nav from "./Nav";
import { TitleContext } from "../TitleContext";

const Page = ({ defaultTitle, children }) => {
    const { title, setTitle } = useContext(TitleContext);

    useEffect(() => {
        if (defaultTitle) {
            setTitle(defaultTitle);
        }
    }, [defaultTitle, setTitle]);

    return (
        <div className="flex h-screen w-screen p-2 space-x-3 overflow-hidden">
            <Nav />
            <div className="flex flex-col space-y-3 h-full w-full">
                <div className="main-div w-full min-h-[85px]">
                    <h1 className="px-4 text-black text-2xl h-full font-bold flex items-center">{title}</h1>
                </div>
                <div className="main-div h-full ">
                    <div className="p-3 h-full">{children}</div>
                </div>
            </div>
        </div>
    );
};

export default Page;
