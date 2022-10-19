let ctx = document.getElementById('myChart').getContext('2d');
let labels = ['Positif', 'Negatif', 'Netral'];
let colorHex = ['#ff6484', '#36a2eb', '#ffce57'];

let myChart = new Chart(ctx, {
  type: 'pie',
  data: {
    datasets: [{
      data: [11387, 4502, 3334],
      backgroundColor: colorHex
    }],
    labels: labels
  },
  options: {
    responsive: true,
    plugins: {
        labels: {
            fontSize: 22,
            fontColor: '#fff',
            position: 'border',
            textShadow: true,

            outsidePadding: 4,
        }
    }
  }
})