const API_CHECK_INTERVAL = 5 * 60 * 1000; // 5 minutes in milliseconds

chrome.runtime.onInstalled.addListener(() => {
   // Check the API immediately
   fetchAPIReminders();

   // Set up the interval to check the API periodically
   chrome.alarms.create('fetchReminders', { periodInMinutes: 1 });
});

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'fetchReminders') {
    clearPastAlarms();

    fetchAPIReminders();
  }
});

async function fetchAPIReminders() {

  await chrome.storage.local.get('hasAuth', (result) => {
    if (!result.hasAuth)
        return
  });

  // Sync reminders local vs API

  const now = new Date();
    
  // Format the date to YYYY-MM-DDTHH:MM
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String('00').padStart(2, '0');
  const minutes = String('00').padStart(2, '0');

  const formattedDate = `${year}-${month}-${day}T${hours}:${minutes}`;

  const requestOptions = {
    method: 'GET',
    credentials: 'include'
  }

  // Get reminders for today
  await fetch('http://127.0.0.1:5001/reminder/?'+ new URLSearchParams({reminder_date: formattedDate,}).toString(), requestOptions)
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
    for(var key in data.result)
    {
        result = data.result[key];
        const alarmName = `notification-${result.reminder_id}`;
        chrome.alarms.get(alarmName, (alarm) => {
          if (!alarm) {
            const notificationTime = new Date(result.reminder_date).getTime();            
            if(notificationTime >= new Date().getTime())
            {
              chrome.alarms.create(alarmName, { when: notificationTime });
              chrome.storage.local.set({ [alarmName]: result.note });
            }
            
          }
        });
    }
  })
  .catch(error => {
    
  });
}

function showNotification(message) {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: '../img/icon-128.png',
    title: 'Reminder',
    message: message,
    priority: 1
  });
}

function clearPastAlarms() {
  chrome.alarms.getAll((alarms) => {
    const now = Date.now();
    alarms.forEach((alarm) => {
      if (alarm.name.startsWith('notification-') && alarm.scheduledTime < now) {
        chrome.alarms.clear(alarmName, (wasCleared) => {
        
        });
      }
    });
  });
}

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name.startsWith('notification-')) {
    const notificationId = alarm.name.split('-')[1];
    // Retrieve the stored notification message
    chrome.storage.local.get(alarm.name, (result) => {
      const message = result[alarm.name];
      showNotification(message);
    });
  }
});

