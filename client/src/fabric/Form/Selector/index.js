import { Select, Input } from "antd"
import { useSnapshot } from "valtio";

import { fabricStore } from "../../store";

const SelectorArg = ({ field, argKey, title, value }) => {
    console.log({ field, argKey, title, value })
    const onChange = (e) => {
         fabricStore.setSelectorArg(field, argKey, e.target.value)
    }

    return (
        <div className="p-1 flex justify-between m-1">
            <span className='font-semibold mt-1'>{title}</span>
            <Input className='w-1/2' onChange={onChange}/>
        </div>
    )
}

const Selector = ({ title, field }) => {
    const $fabricStore = useSnapshot(fabricStore);

    const value = $fabricStore.selectors[field];
    const options = $fabricStore.schema[field];
    const args = $fabricStore.selectors[field]?.args;
    console.log(title, value, args)
    const onChange = (_, value) => {
        fabricStore.setSelectorValue(field, value)
    }

    return (
        <div className="flex flex-col bg-teal-200 my-2 rounded-lg p-1">
            <span className="font-semibold text-base">{title}</span>
            <Select
                className="w-full"
                options={options}
                value={value}
                onChange={onChange}
            />
            <div>
                { args 
                  ? Object.keys(args).map((argKey) => {
                        return (<SelectorArg field={field} argKey={argKey} {...args[argKey]} />)
                    })
                  : <></>
                }
            </div>
        </div>
    )
}

export default Selector