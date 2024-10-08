
document.getElementById("create-reminder-btn").addEventListener("click", createReminder);
document.getElementById("back-btn").addEventListener("click", reload);
document.getElementById('open-reminders').addEventListener('click', openSidePanel);
document.getElementById('logout').addEventListener('click', logout);

var today = addMinutes(new Date(), 5).toISOString().slice(0, 16);
var datetimeInput = document.getElementById("date-time")
datetimeInput.min = today;

datetimeInput.addEventListener('input', function() {
    this.blur();
});

document.addEventListener('DOMContentLoaded', function() {

    setAuth();

    chrome.storage.local.get('hasAuth', (result) => {
        if (result.hasAuth)
        {
            document.getElementById("login-div").style.display = 'none';
            document.getElementById("logout").style.display = 'block';
        }
        else
        {
            document.getElementById("logout").style.display = 'none';
        }
    });
});

async function setAuth()
{
    var hasAuth = await checkAuth();
    chrome.storage.local.set({ ['hasAuth']: hasAuth });
}


function openSidePanel() {
    chrome.windows.getCurrent({ populate: true }, (window) => {
        chrome.sidePanel.open({ windowId: window.id });
    });
    window.close();
}

function reload() {
    location.reload();
}

function addSuccessMessage() {
    document.getElementById("status-message").textContent = 'Successfully Created Reminder';
    document.getElementById("status-message").style.backgroundColor = 'green';
    document.getElementById("status-message").style.color = 'white';
    document.getElementById("status-message").style.padding = '5px';
    document.getElementById("status-message").style.borderRadius = '5px';
    document.getElementById("status-message").style.marginTop = '0px';

    document.getElementById('create-reminder-btn').style.display = 'none'
    document.getElementById('back-btn').style.display = 'block'
}

function addErrorMessage(message) {
    document.getElementById("status-message").textContent = message;
        document.getElementById("status-message").style.backgroundColor = '#ff5d5d';
        document.getElementById("status-message").style.color = 'white';
        document.getElementById("status-message").style.padding = '5px';
        document.getElementById("status-message").style.borderRadius = '5px';
        document.getElementById("status-message").style.marginTop = '0px';
}

async function  createReminder() {

    var date = document.getElementById("date-time").value
    var text = document.getElementById("reminder-note").value

    if (!date || !text) {

        addErrorMessage('Please enter all details below');
    }
    else {

        await chrome.storage.local.get('hasAuth', (result) => {
            if (!result.hasAuth)
            {
                createAlarm(date, 0, text);
                return;
            }
            else
            {
                createAPIReminder(date, note);
            }
        })

        
    }
}

async function createAPIReminder(date, note) {
    // Send data to server and save it to local storage on the browser
    const requestOptions = {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({reminder_date: date, note: text}) 
    }

    await fetch('http://127.0.0.1:5001/reminder/create', requestOptions)
    .then(response => {
        // Check if the request was successful
        if (!response.ok) {
            return response.json().then(errorData => {
                var errorMessage = "";
                if (errorData.result && errorData.result.reminder_date)
                    errorMessage = errorData.result.reminder_date;
                else
                    errorMessage = errorData.message;
                throw new Error(errorMessage || 'Unknown error');
            });
        }
        return response.json();
    })
    .then(data => {
        addSuccessMessage()
        if (data.result)
        {
            createAlarm(data.result.reminder_date, data.result.reminder_id, data.result.note);
        }
    })
    .catch(error => {
        addErrorMessage(error)
    });
}

function createAlarm(reminder_date, reminder_id, note) {

    if (reminder_id <= 0)
    {
        reminder_id = note.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    }

    const notificationTime = new Date(reminder_date).getTime();
    const alarmName = `notification-${reminder_id}`;
    chrome.alarms.create(alarmName, { when: notificationTime });
    chrome.storage.local.set({ [alarmName]: note });
    addSuccessMessage();
}