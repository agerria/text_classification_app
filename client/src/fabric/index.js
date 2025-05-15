import { Splitter } from "antd";

import Page from "../components/Page";
import Form from "./Form";



const Fabric = () => {
    return (
        <Page title='Фабрика'>
            <Splitter
                className="w-ful h-full"
            >
                <Splitter.Panel defaultSize="30%" className=" mr-1">
                    <Form />
                </Splitter.Panel>
                <Splitter.Panel className='h-full ml-1'>
                    <div className="h-full bg-orange-300">
                        Report
                    </div>
                </Splitter.Panel>
            </Splitter>
        </Page>
    )
}

export default Fabric;