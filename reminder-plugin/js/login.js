document.getElementById('login').addEventListener('click', login);

document.addEventListener('DOMContentLoaded', function() {
    //setAuth();
});

async function setAuth()
{
    var hasAuth = await checkAuth();
    chrome.storage.local.set({ ['hasAuth']: hasAuth });

    if (hasAuth) {

        location.replace('../html/create-reminder.html')
    }

}

function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    const requestOptions = {
        method: 'GET',
        credentials: 'include',
        headers : {
            'Authorization': 'Basic ' + btoa(username + ":" + password)
        },
    }

    fetch('http://127.0.0.1:5001/users/authenticate', requestOptions)
    .then(response => {
        // Check if the request was successful
        if (!response.ok) {
            return response.json().then(errorData => {
                addErrorMessage(errorData.message)
                throw new Error(errorData.message || 'Unknown error');
            });
        }
        return response.json();
      })
      .then(data => {
        addSuccessMessage("Success")
        chrome.storage.local.set({ ['hasAuth']: true });
        location.replace('../html/create-reminder.html')
      })
      .catch(error => {
        addErrorMessage(error)
      });
}

function addErrorMessage(message){
    document.getElementById("status-message").innerHTML = message
    document.getElementById("status").style.backgroundColor = 'red'
}

function addSuccessMessage(message){
    document.getElementById("status-message").innerHTML = message
    document.getElementById("status").style.backgroundColor = 'green'
}