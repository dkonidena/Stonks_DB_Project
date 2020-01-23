const TIMEOUT = 10000

function request(method, url, onSuccess, onFail, data) {
  let payload

  if (['POST', 'PATCH'].includes(method)) {
    try {
      payload = JSON.stringify(data)
    } catch (error) {
      onFail(error)
      return
    }
  }

  let timeout = new Promise((resolve) => {
    setTimeout(resolve, TIMEOUT, { timeExpired: true })
  })

  Promise.race([
    fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: payload
    }),
    timeout
  ])
  .then((response) => {
    if (response.timeExpired) {
      throw new TypeError(`NetworkError: timeout after ${TIMEOUT}ms`)
    } else if (!response.ok) {
      throw new TypeError(`HTTP Error: ${response.status} - ${response.statusText}`)
    }
    return response.json()
  })
  .then(onSuccess)
  .catch(onFail)
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
