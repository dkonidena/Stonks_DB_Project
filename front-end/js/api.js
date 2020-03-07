const TIMEOUT = 100000;
const API_ENDPOINT = "/api";

const api = {
    getUserID: () => { return getCurrentUserID() },
    get: {
        users: (dryRun, res, err) => {
            request("GET", `${API_ENDPOINT}/users?&isDryRun=${dryRun}`, res, err);
        },
        currencies: (date, dryRun, res, err) => {
            let options = `isDryRun=${dryRun}`;
            if (date !== null) {
                options += `&date=${date.toISOString()}`
            }
            request("GET", `${API_ENDPOINT}/currencies?${options}`, res, err);
        },
        companies: (date, order, dryRun, res, err) => {
            let options = `isDryRun=${dryRun}&order=${order}`;
            if (date !== null) {
                options += `&date=${date.toISOString()}`
            }
            request("GET", `${API_ENDPOINT}/companies?${options}`, res, err);
        },
        products: (date, dryRun, res, err) => {
            let options = `isDryRun=${dryRun}`;
            if (date !== null) {
                options += `&date=${date.toISOString()}`
            }
            request("GET", `${API_ENDPOINT}/products?${options}`, res, err);
        },
        trades: (filter, dryRun, res, err) => {
            request("GET", `${API_ENDPOINT}/trades?filter=${JSON.stringify(filter)}&isDryRun=${dryRun}`, res, err);
        },
        tradesOffset: (filter, offset, count, dryRun, res, err) => {
            request("GET", `${API_ENDPOINT}/trades?filter=${JSON.stringify(filter)}&isDryRun=${dryRun}&offset=${offset}&count=${count}`, res, err);
        },
        reports: (filter, dryRun, res, err) => {
            request("GET", `${API_ENDPOINT}/reports?filter=${JSON.stringify(filter)}&isDryRun=${dryRun}`, res, err);
        },
        config: (res, err) => {
            request("GET", `${API_ENDPOINT}/config`, res, err);
        },
        events: (res, err) => {
            request("GET", `${API_ENDPOINT}/events`, res, err);
        }
    },
    post: {
        // need to add nonce to all of these
        check_trade: (trade, res, err) => {
            request("POST", `${API_ENDPOINT}/check_trade`, res, err, trade);
        },
        trades: (trade, res, err) => {
            request("POST", `${API_ENDPOINT}/trades`, res, err, trade);
        },
        rules: (rule, res, err) => {
            request("POST", `${API_ENDPOINT}/rules`, res, err, rule);
        },
        companies: (company, res, err) => {
            request("POST", `${API_ENDPOINT}/companies`, res, err, company);
        },
        products: (product, res, err) => {
            request("POST", `${API_ENDPOINT}/products`, res, err, product);
        }
    },
    patch: {
        trades: (id, trade, res, err) => {
            request("PATCH", `${API_ENDPOINT}/trades?id=${id}`, res, err, trade);
        },
        rules: (id, rule, res, err) => {
            request("PATCH", `${API_ENDPOINT}/rules?id=${id}`, res, err, rule);
        },
        companies: (id, company, res, err) => {
            request("PATCH", `${API_ENDPOINT}/companies?id=${id}`, res, err, company);
        },
        products: (id, product, res, err) => {
            request("PATCH", `${API_ENDPOINT}/products?id=${id}`, res, err, product);
        },
        config: (config, res, err) => {
            request("PATCH", `${API_ENDPOINT}/config`, res, err, config);
        }
    },
    delete: {
        trades: (id, res, err) => {
            request("DELETE", `${API_ENDPOINT}/trades?id=${id}`, res, err);
        },
        rules: (id, res, err) => {
            request("DELETE", `${API_ENDPOINT}/rules?id=${id}`, res, err);
        },
        companies: (id, res, err) => {
            request("DELETE", `${API_ENDPOINT}/companies?id=${id}`, res, err);
        },
        products: (id, res, err) => {
            request("DELETE", `${API_ENDPOINT}/products?id=${id}`, res, err);
        }
    }
}

function request(method, url, onSuccess, onFail, data) {
    let payload;

    if (['POST', 'PATCH'].includes(method)) {
        try {
            payload = JSON.stringify(data);
        } catch (error) {
            onFail(error);
            return;
        }
    }

    const debugData = {
        url: url,
        method: method,
        body: data
    }

    Promise.race([
        fetch(encodeURI(url), {
            method: method,
            headers: { 'Content-Type': 'application/json', 'userID': api.getUserID() },
            body: payload
        }),
        new Promise((resolve) => {
            setTimeout(resolve, TIMEOUT, { timeExpired: true });
        })
    ])
    .then((response) => {
        if (response.timeExpired) {
            throw new TypeError(`NetworkError: timeout after ${TIMEOUT}ms`);
        } else if (!response.ok) {
            throw new TypeError(`HTTP Error: ${response.status} - ${response.statusText}`);
        }
        return response.json();
    })
    .then(onSuccess)
    .catch((err) => {
        onFail(err.message, debugData);
    });
}

// calls func1 with the object returned by the server
// or, if HTTP/network/JSON decode error (any type of failure) occurs, call func2 with the error object
// request("GET", "http://0.0.0.0:8000/", func1, func2)
// works the same for DELETE

// POSTs the object named "data" to the address
// then calls func1 with the object returned by the server
// or, if HTTP/network/JSON decode error (any type of failure) occurs, call func2 with the error object
// request("POST", "http://0.0.0.0:8000/", func1, func2, data)
// works the same for PATCH
