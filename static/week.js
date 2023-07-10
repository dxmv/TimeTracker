const [keys,items]=[[],[]];
let sum=0;
const activities=document.querySelectorAll(".activity-name");
activities.forEach(item=>{
    const text=item.innerHTML;
    const [name,times]=text.split("-");
    keys.push(name);
    items.push(item.dataset.times);
    sum+=Number(item.dataset.times);
});
keys.push("Unknown");
items.push((7*48)-sum);

const ctx = document.getElementById('weekChart');
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