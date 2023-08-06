$(function(){
    $.getJSON('./events.json')
	.done(function(json){
	    let src = ['<tr>'];
	    for (let key in json[0]) {src.push('<th>'+key+'</th>');}
	    src.push('</tr>');
	    $('#tab_event').append(src.join(""));
	    for (let evt of json) {
		let src = ['<tr>'];
		for (let [key, val] of Object.entries(evt)) {
		    if (key != 'id') {
			if (val == true) {
			    val = '<ons-icon icon="fa-check-circle"></ons-icon>';
			} else if (val == false){
			    val = '<ons-icon icon="fa-minus"></ons-icon>';
			}
		    }
		    src.push('<td>'+val+'</td>');
		}
		src.push('</tr>');
		$('#tab_event').append(src.join(""));
	    }
	    
	})
	.fail(function(){
	    console.log('events.json load error.');
	});
});

