import api from '../../api';

export class BaseTableStore {
    // url = `${process.env.APP_SERVER_URL}/elimination-defects/incidents/table`
    url = ''
    
    limitOptions = [10, 20, 30, 100];
    limit = 20;
    
    data = [];
    total = -1;
    page = 1;
    
    loading = false;
    
    // async fetch() {
    //     try {
    //         console.log('fetch', this.url)
    //         this.loading = true;
    //         const filterString = this.filters.map(f => `${f.key}=${f.value}`).join('&');
    //         const orderString = `order=${JSON.stringify(this.order)}`;
            
    //         const res = await api
    //         .get(
    //             `${this.url}?limit=${this.limit}&page=${this.page}`
    //         )
    //         .json();
    //         this.data = res.data;
    //         this.total = res.total;
    //         this.loading = false;
    //     } catch (error) {
    //         console.log(error);
    //         this.loading = false;
    //     }
    // }
    
    async fetch(url_args) {
            const _url = (typeof this.url === 'function') ? this.url(url_args) : this.url;
            console.log('fetch', this.url)
            this.loading = true;
            
            const res = await api
            .get(
                `${_url}?limit=${this.limit}&page=${this.page}`
            )
            .json();
            this.data = res.data;
            this.total = res.total;
            this.loading = false;
        
    }

    paginationChange(nextPage, limit, url_args) {
        this.page = nextPage;
        this.limit = limit;
        this.fetch(url_args);
    }
}

// import { proxy } from 'valtio';
// export const baseTableStore = proxy(new BaseTableStore());