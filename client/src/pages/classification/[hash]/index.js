import { useParams } from "react-router-dom";

import Page from "../../../components/Page";
import Classification from "../../../components/Classification";

const ClassificationViewPage = () => {
    const { hash } = useParams();

    return (
        <Page defaultTitle={`Классификация ${hash}`}>
            <Classification hash={hash}/>
        </Page>
    )
}

export default ClassificationViewPage;