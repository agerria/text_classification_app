import ky from 'ky-universal'
import Cookie from 'js-cookie'

const api = ky.extend({
    hooks: {
        beforeRequest: [
            (request) => {
                request.headers.set('Authorization', Cookie.get('token'))
            },
        ],
        afterResponse: [
            async (request, options, response) => {
                if (response.status === 401) {
                    window.location.href = '/login/'
                }
            }
        ]
    },
    timeout: 60000 * 15,
})

export default api
