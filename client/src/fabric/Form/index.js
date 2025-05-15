import { Button } from "antd";
import { useSnapshot } from "valtio";

import Selector from "./Selector";
import { fabricStore } from "../store";

const Form = () => {
    const $fabricStore = useSnapshot(fabricStore);

    const onClickProcess = () => {
        console.log($fabricStore.selectors)
    }

    return (
        <div className=" flex flex-col h-full  border-gray-200 border-2 p-2 rounded-lg shadow-sm">
            <div className="">
                <Selector title='Транслятор'    field='translator'/>
                <Selector title='Векторизатор'  field='vectorizator'/>
                <Selector title='Классификатор' field='classifier'/>
                <Selector title='Оценщик'       field='reporter'/>
            </div>
            <div className="flex justify-center">
                <Button  type="primary" onClick={onClickProcess}>Обработать</Button>
            </div>
        </div>
    )
}

export default Form;