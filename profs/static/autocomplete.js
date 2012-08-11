$(function(){

	var personUrl = popitApiUrl+'person';

	var generateAutocompletion=  function( request, response ) {

		async.parallel([
    		function(callback){
    			$.ajax({
					url: personUrl,
					dataType: "jsonp",
					data: {
						name: request.term
					},
					success: function( data ) {
						callback(null, $.map( data.results, function( item ) {
							return {
								label: item.name,
								value: 'slug:'+item.slug,
								category: 'Match in name',
								rank: 8
							}
						}));
					},
					error: function( xhr, textStatus, errorThrown ) {
						console.log(xhr, textStatus, errorThrown)
						callback(errorThrown)
					}
				});
    		},
    		function(callback){
    			$.ajax({
					url: personUrl,
					dataType: "jsonp",
					data: {
						summary: request.term
					},
					success: function( data ) {
						callback(null, $.map( data.results, function( item ) {
							return {
								label: item.name,
								value: 'slug:'+item.slug,
								category: 'Match in summary',
								rank: 4
							}
						}));
					},
					error: function( xhr, textStatus, errorThrown ) {
						console.log(xhr, textStatus, errorThrown)
						callback(errorThrown)
					}
				});
    		},
    		function(callback){
    			all = [{
    				label: 'All Professors', 
    				value: 'all',
    				category: 'Special',
					rank: 2
    			}]
    			callback(null, all)
    		}
		], function(err, results) {
			if (err) {
				alert("Aww snap. An error occured.\n" + err);
				response()
			} else {
				suggestions = _.union(results[0], results[1], results[2]);
				suggestions = _.sortBy(suggestions, function(item) {return item.value+item.rank});
				suggestions = _.uniq(suggestions, true, function(item) {return item.value});
				suggestions = _.sortBy(suggestions, function(item) {return -item.rank});
				response(suggestions);
			}
		});
	}


	$.widget( "custom.catcomplete", $.ui.autocomplete, {
		_renderMenu: function( ul, items ) {
			var self = this,
				currentCategory = "";
			$.each( items, function( index, item ) {
				if ( item.category != currentCategory ) {
					ul.append( "<li class='ui-autocomplete-category'>" + item.category + "</li>" );
					currentCategory = item.category;
				}
				self._renderItem( ul, item );
			});
		}
	});


	$('.popit-autocomplete').catcomplete({
		source: function( request, response ) {
			generateAutocompletion(request, response)					
		},
		minLength: 1,
		autoFocus: false,
		select: function( event, ui ) {
			console.log( ui.item );
		}
	});
});