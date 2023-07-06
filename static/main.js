const loadDayChart=()=>{
  const ctx = document.getElementById('dayChart');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
      datasets: [{
        label: '# of Votes',
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

const editFormOpen=(start,end,activityText)=>{
    const darkOverlay=document.getElementById("dark-overlay");
    darkOverlay.style.display="flex";
    const startTime=document.getElementById("startTime");
    const endTime=document.getElementById("endTime");
    const activity=document.getElementById("activity");
    startTime.value=start;
    endTime.value=end;
    activity.value=activityText;
};