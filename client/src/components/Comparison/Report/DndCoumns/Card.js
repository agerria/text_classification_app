import { useSnapshot } from "valtio";
import { comparisonReportStore as store } from "../store";
import { Spin, Tag } from "antd";

import { TITLE_HEIGHT } from "../consts";

const TitleTag = ({color, title, args}) => {
    const tags = args ? Object.keys(args).map(key => `${key}: ${args[key]}`) : [];

    return (
        <Tag color={color} className="text-sm w-full p-1 flex justify-between"> 
            {title} 
            <div>
                {/* <Tag >test</Tag>
                <Tag >test</Tag>
                <Tag >test</Tag> */}
                { tags &&
                    tags.map((tag, i) =>
                        (<Tag className="" key={i}>{tag}</Tag>)
                    )
                }
            </div>
        </Tag>
    )
}

export const CardTitle = ({title}) => {
    return (
        <div className="flex flex-col font-bold px-2 border-[1px] rounded-md space-y-1 py-1 overflow-y-hidden max-h-[133px]">
            <TitleTag color='blue' title={title.dataset}/>
            <TitleTag color='green' title={title.vectorizer} args={title.vectorizer_args}/>
            <TitleTag color='red' title={title.classifier} args={title.classifier_args}/>
        </div>
    )
}

const CardReport = ({card}) => {
    return (
        <div className="h-full bg-gray-100 rounded p-2"></div>
    )
}

const Card = ({ hash }) => {
    const $store = useSnapshot(store);
    const card = $store.cardsInfo[hash];

    // const className = `${columnW} ${titleH} bg-white rounded-lg shadow-md p-2  overflow-y-hidden overflow-x-hidden`;
    const className = `bg-white rounded-lg shadow-md p-2  overflow-y-hidden overflow-x-hidden`;

    if (!card) {
        return (
            <div className={className}>
                <Spin />
            </div>
        )
    }

    return (
        <div className={className}>
            {/* <div className="font-bold text-lg mb-4">{hash}</div> */}
            <CardTitle card={card}/>
            {/* <CardReport card={card}/> */}
        </div>
    );
};

export default Card