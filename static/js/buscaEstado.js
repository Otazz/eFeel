jQuery(function($){
	var est = [];
	$("#ate").attr('disabled','disabled');
	$("#pesquisar").submit(function(){
		var rg = $("#regiao").val();
		var jsonData = $.ajax({
			url: 'static/json/estados.json',
			dataType: 'json'
		}).done(function (results) {
			$.each(results,function(k,v){
				if(k == rg){
					est = v;
				}
			});
			var jsonData = $.ajax({
				url: 'static/json/geral.json',
				dataType: 'json'
			}).done(function (results) {
				$("#rsEstados").empty();
				var ddEst = [],dd01 = [],dd02 = [];
				var cont = 0;
				$.each(results,function(k,v){
					$.each(v[0],function(k,v){
						for(i = 0;i < est.length;i++){
							if(est[i] == k){
								dd01[cont] = v;
								ddEst[cont] = k;
								cont++;
								console.log(k);
								console.log(v);
							}	
						}
					});
					cont02 = 0;
					$.each(v[1],function(k,v){
						for(i = 0;i < est.length;i++){
							if(est[i] == k){
								dd02[cont02] = v;
								cont02++;
							}	
						}
					});
				});
				for(i = 0;i < dd01.length;i++){
					var icon;
					if(dd01[i] >= 0){
						icon = '<img src="static/images/iconBem.png"/>';
					}else{
						icon = '<img src="static/images/iconBad.png"/>';
					}
					$("#rsEstados").append(
					        '<div class="col-md-4">'+
							'<div class="box box-widget widget-user-2">'+
					            '<div class="widget-user-header bg-blue">'+
					              '<h3 class="widget-user-username">'+ddEst[i]+'</h3>'+
					            '</div>'+
					            '<div class="box-footer no-padding">'+
					              '<ul class="nav nav-stacked">'+
					                "<li id='"+ddEst[i]+"'><a href='#' onclick='Marca(\""+ddEst[i]+"\");return false;'>Minha marca na mídia <span class='pull-right'>"+icon+"</span></a></li>"+
							        '<li id="rsMidia_'+ddEst[i]+'" style="display:none;"><a href="#">Nível de satisfação <span class="pull-right badge bg-green">'+Math.ceil(dd01[i]*100)+' %</span></a></li>'+
					                '<li><a href="#">Emplacamentos efetuados <span class="pull-right badge bg-green">'+Math.ceil(dd02[i])+' </span></a></li>'+
					              '</ul>'+
					            '</div>'+
					          '</div>'+
				          '</div>'	
					);						
				}
			});
		});
		return false;
	});
	
	Marca = function(uf){		
		$("#rsMidia_"+uf).show('down');
	}
});
