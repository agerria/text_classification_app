export const hashsToQuery = (hashs) => {
    return hashs.join(',')
}

export const queryToHashs = (query) => {
    return query.split(',')
}

export const setHashs = (hashs, setParam) => {
    setParam(hashsToQuery(hashs))
}

export const getHashs = (param) => {
    return queryToHashs(param)
}