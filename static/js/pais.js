var dtHome=[0,0,0,0,0,0,0,0,0,0,0,0];
var mes,jan=0,fev=0,mar=0,abr=0,mai=0,jun=0,jul=0,ago=0,set=0,out=0,nov=0,dez=0;
function doughnut() {
	var jsonData = $.ajax({
		url: "static/json/arquivo.json",
		dataType: 'json'
	}).done(function (results) {
		var labels = [], data=[];
		$.each(results,function(k,v){
			labels.push("# of Votes");
			data.push(parseFloat(v.pais));
		});
	  var ctx = document.getElementById("pais02").getContext('2d');
	  var myChart = new Chart(ctx, {
		  type: 'doughnut',
		  data: {
			labels: ["Não Gostaram", "Indiferente", "Gostaram"],
		    datasets: [{
		      data: data,
		      backgroundColor: [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)'
              ],
              borderColor: [
                  'rgba(255,99,132,1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)'
              ],
              borderWidth: 1
		    }]
		  }
	  });	  
	});
}
doughnut();

function line() {
	var data=[0,0,0,0,0,0,0,0,0,0,0,0];
	var i=0,j=0,x=0;
	var jsonData = $.ajax({
		url: 'static/json/data.json',
		dataType: 'json'
	}).done(function (results) {
		$.each(results,function(k,v){
			$.each(v,function(k,v){
				$.each(v,function(k,v){
					if(v.length == 10){
						var qb = v.split("-");
						switch(parseInt(qb[1])){
						case 01:
							dtHome[0]++;
							break;
						case 02:
							dtHome[1]++;
							break;
						case 03:
							dtHome[2]++;
							break;
						case 04:
							dtHome[3]++;
							break;
						case 05:
							dtHome[4]++;
							break;
						case 06:
							dtHome[5]++;
							break;
						case 07:
							dtHome[6]++;
							break;
						case 08:
							dtHome[7]++;
							break;
						case 09:
							dtHome[8]++;
							break;
						case 10:
							dtHome[9]++;
							break;
						case 11:
							dtHome[10]++;
							break;
						case 12:
							dtHome[11]++;
							break;
					}		
					}
				});

				j++;				
			});
			i++;
		});

			Chart.defaults.global.animationSteps = 50;
			Chart.defaults.global.tooltipYPadding = 16;
			Chart.defaults.global.tooltipCornerRadius = 0;
			Chart.defaults.global.tooltipTitleFontStyle = "normal";
			Chart.defaults.global.tooltipFillColor = "rgba(0,160,0,0.8)";
			Chart.defaults.global.animationEasing = "easeOutBounce";
			Chart.defaults.global.responsive = true;
			Chart.defaults.global.scaleLineColor = "black";
			Chart.defaults.global.scaleFontSize = 16;

			for(i = 0;i < dtHome.length;i++){
				dtHome[i] = dtHome[i] / 3;
			}
			
			var ctx = document.getElementById("pais").getContext("2d");
			  var myChart = new Chart(ctx, {
				  type: 'line',
				  data: {
					  labels: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul","Ago","Set","Out","Nov","Dez"],
					  datasets: [{
						label:"Média em 3 anos de dados",
				        fillColor: "rgba(220,220,220,0)",
				        strokeColor: "rgba(220,180,0,1)",
				        pointColor: "rgba(220,180,0,1)",
				        data: dtHome
				}]
				  }
			  });
	});
}
line();