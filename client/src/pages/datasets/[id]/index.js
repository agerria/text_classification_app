import { useParams } from "react-router-dom";

import Page from "../../../components/Page";
import DatasetsInfo from "../../../components/Datasets/Info";

const DatasetsInfoPage = () => {
    const { id } = useParams();

    return (
        <Page>
            <DatasetsInfo id={id}/>
        </Page>
    )
}

export default DatasetsInfoPage;