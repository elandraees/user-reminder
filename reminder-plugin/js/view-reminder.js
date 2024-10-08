document.getElementById("search-reminders").addEventListener("click", getReminders);

var datetimeInput = document.getElementById('reminder-date-time');
datetimeInput.addEventListener('input', function() {
    this.blur();
});

document.addEventListener('DOMContentLoaded', function() {

    document.getElementById("reminder-list").innerHTML = '<h3>No reminders Found</h3>';

    chrome.storage.local.get('hasAuth', (result) => {
        if (!result.hasAuth)
            document.getElementById("view-reminder-header").style.display = 'none';
    });
        


    setDefaultDatetime()
    getReminders()

}, false);

function removeLocalReminder(alarmName) {

    chrome.alarms.clear(alarmName, (wasCleared) => {
        console.log(wasCleared);
    });

    chrome.storage.local.remove(alarmName, function() {
    });

    const listItem = document.getElementById('reminder-li-' + alarmName);
    listItem.remove;

    const lineItem = document.getElementById('reminder-line' + alarmName);
    lineItem.remove;

    location.reload();

}

function removeReminder(id) {

    const requestOptions = {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({reminder_id: id})
    }


    fetch('http://127.0.0.1:5001/reminder/remove', requestOptions)
    .then(response => {
        // Check if the request was successful
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.message || 'Unknown error');
            });
        }
        return response.json();
    })
    .then(data => {
    
        const listItem = document.getElementById('reminder-li-' + id);
        listItem.remove;

        const lineItem = document.getElementById('reminder-line' + id);
        lineItem.remove;

        location.reload();
    })
    .catch(error => {
        alert(error);
    });
    
}

function setDefaultDatetime() {
    const datetimeInput = document.getElementById('reminder-date-time');
    const now = new Date();
    
    // Format the date to YYYY-MM-DDTHH:MM
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String('00').padStart(2, '0');
    const minutes = String('00').padStart(2, '0');

    const formattedDate = `${year}-${month}-${day}T${hours}:${minutes}`;

    // Set the default value
    datetimeInput.value = formattedDate;
}

async function getReminders() {

    const reminderList = document.getElementById("reminder-list");
    reminderList.innerHTML = '<h3>Your Reminders:</h3>';

    await chrome.storage.local.get('hasAuth', (result) => {
        if (!result.hasAuth){
            getLocalReminders();
        }
        else {
            getAPIReminders();
        }
    })
}

function getAPIReminders()
{
    const requestOptions = {
        method: 'GET',
        credentials: 'include'
    }

    var reminderDate = document.getElementById('reminder-date-time').value;

    fetch('http://127.0.0.1:5001/reminder/?' + new URLSearchParams({
        reminder_date: reminderDate,
    }).toString(), requestOptions)
    .then(response => {
        // Check if the request was successful
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.message || 'Unknown error');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.result.length > 0)
            reminderList.innerHTML = '';
        
        for(var key in data.result)
        {
            result = data.result[key];

            createReminderItem(result.reminder_date, result.reminder_id, result.note, false)
        }

    })
    .catch(error => {
    
    });
}

function getLocalReminders()
{
    chrome.alarms.getAll((alarms) => {
        alarms.forEach((alarm) => {
          if (alarm.name.startsWith('notification-')) {
            chrome.storage.local.get(alarm.name, (result) => {
                const message = result[alarm.name];
                createReminderItem(alarm.scheduledTime, alarm.name, message, true);
            });
          }
        });
    });
}

function createReminderItem(reminder_date, reminder_id, text, isLocal)
{
    const reminderList = document.getElementById("reminder-list");

    const li = document.createElement('li');
    const div = document.createElement('div');
    const div2 = document.createElement('div');
    const span = document.createElement('span');
    const button = document.createElement('button');
    const icon = document.createElement('i')
    const note = document.createElement('p');
    const line = document.createElement('hr');

    // Style elements
    div2.style.display = 'flex';
    span.className = 'time';
    span.innerText = formatScheduledTime(reminder_date);
    button.className = 'delete-button';
    button.style.fontSize = '24px';
    button.title = 'Remove Reminder';
    button.id = reminder_id;
    li.id = 'reminder-li-' + reminder_id;
    line.id = 'reminder-line' + reminder_id;
    button.addEventListener('click', function() {
        if (isLocal)
            removeLocalReminder(button.id);
        else
            removeReminder(button.id);
    });
    icon.className = 'fa fa-trash-o';
    note.innerHTML = text;

    // Add elements
    reminderList.appendChild(li);
    reminderList.appendChild(line);
    li.appendChild(div);
    div.appendChild(div2);
    div.appendChild(note)
    div2.appendChild(span);
    div2.appendChild(button);
    button.appendChild(icon);
}

function formatScheduledTime(scheduledTime) {
    const date = new Date(scheduledTime);

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}`;
}