var nds_wsd = __TEMPLATE_WSD__;

var nds_libs = [
    'https://unpkg.com/what-the-pack/dist/MessagePack.min.js'
    ,'https://www.WebRTC-Experiment.com/RecordRTC.js'
    //' /libs/MessagePack.min.js'
    , '__TEMPLATE_DUCTS_LIBS__main.js'
]
var nds_libs_index = 0;
(function append_next_lib() {
    if (nds_libs_index < nds_libs.length) {
	var lib_script = document.createElement('script');
	lib_script.src = nds_libs[nds_libs_index];
	document.body.appendChild(lib_script);
	nds_libs_index++;
    }
    if (nds_libs_index < nds_libs.length) {
	lib_script.onload = append_next_lib;
    } else {
	lib_script.onload = function() { __TEMPLATE_CALLBACK__(nds_wsd); };
    }
})();


