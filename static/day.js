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

const cancelForm=()=>{
    const darkOverlay=document.getElementById("dark-overlay");
    darkOverlay.style.display="none";
}

const cancelButton=document.getElementById("editCancel");
cancelButton.onclick=cancelForm;

let map = new Map();
const activities=document.querySelectorAll(".activity-name");
activities.forEach(item=>{
    const text=item.innerHTML;
    if(map.has(text)){
        let current=map.get(text)+1;
        map.set(text,current);
    }
    else{
        map.set(text,1);
    }
});
const [keys,items]=[[],[]];
for (let key of map.keys()) {
    keys.push(key);
    items.push(map.get(key));
}

const ctx = document.getElementById('dayChart');
new Chart(ctx, {
type: 'doughnut',
data: {
  labels: keys,
  datasets: [{
    label: 'Activities',
    data: items,
    borderWidth: 1
  }]
},
});