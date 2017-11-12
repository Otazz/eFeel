function drawLineChart() {

  // Add a helper to format timestamp data
  Date.prototype.formatMMDDYYYY = function() {
      return (this.getMonth() + 1) +
      "/" +  this.getDate() +
      "/" +  this.getFullYear();
  }
  
  var jsonData = $.ajax({
    url: "static/json/arquivo.json"
    dataType: 'json'
  }).done(function (results) {
    // Split timestamp and data into separate arrays
	  var labels = [], data=[];
	  $.each(results,function(k,v){
		 console.log(k+" | "+v.Votes);
		  labels.push("# of Votes");
		  data.push(parseFloat(v.Votes));
	  });
	  var ctx = document.getElementById("barGf").getContext('2d');
	  var myChart = new Chart(ctx, {
	      type: 'bar',
	      data: {
	          labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
	          datasets: [{
	              labels,
	              data,
	              backgroundColor: [
	                  'rgba(255, 99, 132, 0.2)',
	                  'rgba(54, 162, 235, 0.2)',
	                  'rgba(255, 206, 86, 0.2)',
	                  'rgba(75, 192, 192, 0.2)',
	                  'rgba(153, 102, 255, 0.2)',
	                  'rgba(255, 159, 64, 0.2)'
	              ],
	              borderColor: [
	                  'rgba(255,99,132,1)',
	                  'rgba(54, 162, 235, 1)',
	                  'rgba(255, 206, 86, 1)',
	                  'rgba(75, 192, 192, 1)',
	                  'rgba(153, 102, 255, 1)',
	                  'rgba(255, 159, 64, 1)'
	              ],
	              borderWidth: 1
	          }]
	      },
	      options: {
	          scales: {
	              yAxes: [{
	                  ticks: {
	                      beginAtZero:true
	                  }
	              }]
	          }
	      }
	  });
  });
}
drawLineChart();