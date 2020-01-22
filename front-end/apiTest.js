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

  fetch(url, {
    method: method,
    headers: {'Content-Type': 'application/json'},
    body: payload
  })
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP Error ${response.status}: ${response.statusText}`);
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
