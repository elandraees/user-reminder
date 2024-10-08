async function checkAuth()
{
  const requestOptions = {
      method: 'GET',
      credentials: 'include'
  }

  var hasAuth = false;

  await fetch('http://127.0.0.1:5001/users/has_auth', requestOptions)
  .then(response => {
      // Check if the request was successful
      if (!response.ok) {
          return response.json().then(errorData => {
              throw new Error();
          });
      }
      return response.json();
  })
  .then(data => {
    hasAuth = true;
  })
  .catch(error => {
    hasAuth = false;
  });

  return hasAuth;
}

async function hasAuth() {
    await chrome.storage.local.get('hasAuth', (result) => {
        return result.hasAuth;
    });
}

async function logout()
{
    const requestOptions = {
        method: 'GET',
        credentials: 'include'
    }
  
  
    await fetch('http://127.0.0.1:5001/users/logout', requestOptions)
    .then(response => {
        // Check if the request was successful
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error();
            });
        }
        return response.json();
    })
    .then(data => {
        chrome.storage.local.set({ ['hasAuth']: false });
    })
    .catch(error => {
    });

    location.reload();
  
}

function addMinutes(date, minutes) {
    return new Date(date.getTime() + minutes*60000);
}