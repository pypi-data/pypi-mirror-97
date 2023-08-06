const { encode, decode } = MessagePack.initialize(2**22);

class WSClient {

    constructor(wsd) {
	this.WSD = wsd;
	this.EVENT = wsd.EVENT;
	this.encode = encode;
	this.decode = decode;
	
	this._last_rid = 0;
	this.next_rid = 
	    () => {return this._next_rid(this);};

	this._ws = new WebSocket(wsd.websocket_url);
	this._ws.binaryType = 'arraybuffer';
	this._ws.onopen = 
	    (event) => {this._ws_onopen(this, event);};
	this._ws.onmessage = 
	    (event) => {this._ws_onmessage(this, event);};
	this._ws.onerror =
	    (event) => {this._ws_onerror(this, event);}
	this._ws.onclose =
	    (event) => {this._ws_onclose(this, event);}

	this._onopen_event_handler = null;
	this.set_onopen_event_handler = 
	    (handler) => {this._onopen_event_handler = handler;};

	this._onmessage_default_handler =
	    (rid, eid, data) => {console.log("unhnalded message:"+eid+":"+data);};
	this._onmessage_handlers = {};
	
	this.set_onmessage_handler = 
	    (event_id, handler) => {this._onmessage_handlers[event_id] = handler;};
	this.set_onmessage_default_handler = 
	    (handler) => {this._onmessage_default_handler = handler;};

	this.send = 
	    (request_id, event_id, data) => {this._send(this, request_id, event_id, data)};

    }

    _next_rid(self) {
	let next_id = new Date().getTime();
	if (next_id <= self._last_rid) {
	    next_id = self._last_rid + 1;
	}
	self._last_rid = next_id;
	return next_id;
    }

    _send(self, request_id, event_id, data) {
	const msgpack = self.encode([request_id, event_id, data])
	self._ws.send(msgpack)
    }

    _ws_onopen(self, event) {
	console.log("WebSocket is open now.");
	let rid = self.next_rid();
	let eid = self.EVENT.ALIVE_MONITORING;
	let value = ''
	self.send(rid, eid, value);
	if (self._onopen_event_handler != null) {
	    self._onopen_event_handler(self);
	}
    }

    _ws_onmessage(self, event) {
	try {
	    const [rid, eid, data] = self.decode(MessagePack.Buffer.from(event.data));
	    console.log('on_message eid='+eid)
	    const handler = self._onmessage_handlers[eid];
	    if (handler != null) {
		handler(rid, eid, data);
	    } else if (eid == self.EVENT.ALIVE_MONITORING) {
		console.log('alive...')
	    } else {
		self._onmessage_default_handler(rid, eid, data);
	    }
	}
	catch (e) {
	    console.error(e);
	}
    }

    _ws_onerror(self, event) {
	console.error(event);
    }

    _ws_onclose(self, event) {
	console.log('closed');
    }

}


class AudioRecorder {
    
    constructor() {

	this._isEdge = navigator.userAgent.indexOf('Edge') !== -1 && (!!navigator.msSaveOrOpenBlob || !!navigator.msSaveBlob);
	this._isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
	this._recorder; // globally accessible
	this._microphone;

	this.get_user_media =
	    (callback) => {this._get_user_media(this, callback)};
	    
	this.start_recording =
	    () => {this._start_recording(this, null)};
	    
	this.stop_recording =
	    () => {this._stop_recording(this)};

	this._ondata_event_handler = null;
	this.set_ondata_event_handler = 
	    (handler) => {this._ondata_event_handler = handler;};

	this._recorder_event_handler = null;
	this.set_recorder_event_handler = 
	    (handler) => {this._recorder_event_handler = handler;};

	this._recorder_error_handler = null;
	this.set_recorder_error_handler = 
	    (handler) => {this._recorder_error_handler = handler;};

	

    }

    _get_user_media(self, callback) {
	console.log('get_user_media');
	if(self._microphone) {
	    callback(self._microphone);
	    return;
	}
	if(typeof navigator.mediaDevices === 'undefined' || !navigator.mediaDevices.getUserMedia) {
	    alert('This browser does not supports WebRTC getUserMedia API.');
	    if(!!navigator.getUserMedia) {
		alert('This browser seems supporting deprecated getUserMedia API.');
	    }
	}
	navigator.mediaDevices.getUserMedia({
	    audio: isEdge ? true : {
		echoCancellation: false
	    }
	}).then(function(mic) {
	    callback(mic);
	}).catch(function(error) {
	    alert('Unable to capture your microphone. Please check console logs.');
	    console.error(error);
	});
    }

    _start_recording(self, microphone) {

	console.log('start_recording:mic='+microphone)
	
	if (!self._microphone) {
	    if (!microphone) {
		self.get_user_media(function(stream) {
		    self._start_recording(self, stream);
		});
	    } else {
		self._microphone = microphone;
		if(self._isSafari) {
		    alert('Please click startRecording button again. First time we tried to access your microphone. Now we will record it.');
		    return;
		}
		self._start_recording(self, microphone);
	    }
	    return;
	}
	var options = {
	    type: 'audio',
	    recorderType: RecordRTC.StereoAudioRecorder,
	    mimeType: 'audio/wav',
	    //disableLogs: false,
	    //numberOfAudioChannels: isEdge ? 1 : 2,
	    desiredSampRate: 16000,
	    numberOfAudioChannels: 1,
	    checkForInactiveTracks: true,
	    bufferSize: 16384,
	    timeSlice: 1000
	};
	/**
	if(navigator.platform && navigator.platform.toString().toLowerCase().indexOf('win') === -1) {
	    options.sampleRate = 48000; // or 44100 or remove this line for default
	}
	if(self._isSafari) {
	    options.sampleRate = 44100;
	    options.bufferSize = 4096;
	    options.numberOfAudioChannels = 2;
	}
	*/
	if(self._recorder) {
	    self._recorder.destroy();
	    self._recorder = null;
	}
	
	options.ondataavailable = (blob) => {
	    if (this._ondata_event_handler) {
		let fileReader = new FileReader();
		fileReader.onload = (event) => {self._ondata_event_handler(self, event.target.result);};
		fileReader.readAsArrayBuffer(blob);
	    } else {
		console.log('dataavailable:e='+blob);
	    }
	}
	
	self._recorder = RecordRTC(self._microphone, options);
	
	self._recorder.startRecording();

    }

    _stop_recording(self) {
	self._recorder.stopRecording(self._stopRecordingCallback);
    }

    _stopRecordingCallback() {

    }

    _release_microphone(self) {
	if(self._microphone) {
	    self._microphone.stop();
	    self._microphone = null;
	}
	if(self._recorder) {
	    // click(btnStopRecording);
	}
    }



    _start_recording_sample(self) {
	
	if (!self._microphone) {
	    self._get_user_media(self, function(mic) {
		self._microphone = mic;
		if(self._isSafari) {
		    //replaceAudio();
		    alert('Please click startRecording button again. First time we tried to access your microphone. Now we will record it.');
		    return;
		}
		
		self._start_recording(self);
	    });
	    return;
	}
	//replaceAudio();
	var options = {
	    type: 'audio',
	    recorderType: RecordRTC.StereoAudioRecorder,
	    mimeType: 'audio/wav',
	    timeSlice: 3000,
	    disableLogs: false,
	    //numberOfAudioChannels: isEdge ? 1 : 2,
	    numberOfAudioChannels: 1,
	    checkForInactiveTracks: true,
	    bufferSize: 16384
	};
	
	if(self._isSafari || self._isEdge) {
	    options.recorderType = StereoAudioRecorder;
	}
	
	if(navigator.platform && navigator.platform.toString().toLowerCase().indexOf('win') === -1) {
	    options.sampleRate = 48000; // or 44100 or remove this line for default
	}
	
	if(self._isSafari) {
	    options.sampleRate = 44100;
	    options.bufferSize = 4096;
	    options.numberOfAudioChannels = 2;
	}
	
	if(self._recorder) {
	    self._recorder.destroy();
	    self._recorder = null;
	}
	
    
	options.ondataavailable = (blob) => { 
	    console.log('dataavailable:e='+blob);
	    let fileReader = new FileReader();
	    fileReader.onload = (event) => {audio_recorder(self, event.target.result);};
	    fileReader.readAsArrayBuffer(blob);
	}
	
	self._recorder = RecordRTC(self._microphone, options);
	
	self._recorder.startRecording();

    }

    
    

}




class SimpleMediaRecorderOld {

    constructor(wsd) {
	this._recorder = null;
	//this.audio = document.querySelector('audio');
	
	this.open_user_media =
	    (constraints = {audio: {echoCancellation: false}}, timeslice = 2000) => {this._open_user_media(this, constraints, timeslice)};    //{ audio: true }
	this.start_recording = 
	    () => {this._start_recording(this)};
	this.stop_recording =
	    () => {this._stop_recording(this)};

	this._ondata_event_handler = null;
	this.set_ondata_event_handler = 
	    (handler) => {this._ondata_event_handler = handler;};

	this._recorder_event_handler = null;
	this.set_recorder_event_handler = 
	    (handler) => {this._recorder_event_handler = handler;};

	this._recorder_error_handler = null;
	this.set_recorder_error_handler = 
	    (handler) => {this._recorder_error_handler = handler;};

	if(typeof navigator.mediaDevices === 'undefined' || !navigator.mediaDevices.getUserMedia) {
	    alert('This browser does not supports WebRTC getUserMedia API.');

	    if(!!navigator.getUserMedia) {
		alert('This browser seems supporting deprecated getUserMedia API.');
	    }
	}
    }

    _start_recording(self) {
	if (self._recorder == null) {
	    console.log("start_recording method was called but was ignored.");
	    return;
	}
	console.log('start_recording')
	self._recorder.startRecording();
    }

    _stop_recording(self) {
	if (self._recorder == null) {
	    console.log("stop_recording method was called but was ignored.");
	    return;
	}
	console.log("stop_recording method called.");
	self._recorder.stopRecording( () => {
	    console.log("stop_recording callback!!!!!!!!!!!!!!!!!!!!!");
	    //if(self._recorder_event_handler != null) {
	    if(self._ondata_event_handler != null) {
		const blob = self._recorder.getBlob()
		console.log('close:blob='+blob);
		let fileReader = new FileReader();
		fileReader.onload = (event) => {self._ondata_event_handler(self, blob);};
		fileReader.readAsArrayBuffer(blob);
		//self._recorder_event_handler('stop', '')
	    }
	});

    }

    _open_user_media(self, constraints, timeslice) {
	navigator.mediaDevices.getUserMedia(constraints) 
	    .then((stream) => {self._media_onopen(self, stream, timeslice)});
    }
    
    _media_onopen(self, stream, timeslice) {
	console.log('media opened. stream='+stream + " timeslice="+timeslice);
        self._recorder = RecordRTC(stream, {
	    recorderType: RecordRTC.StereoAudioRecorder,
	    mimeType: 'audio/wav',
	    timeSlice: 3000,
	    disableLogs: false,
	    ondataavailable: function(blob) {
		console.log('dataavailable:e='+blob);
		let fileReader = new FileReader();
		fileReader.onload = (event) => {self._ondata_event_handler(self, event.target.result);};
		fileReader.readAsArrayBuffer(blob);
            }
	});
	self._recorder.startRecording();
    }

	
    _media_onopen_old2(self, stream, timeslice) {
	let options = {
	    type: 'audio',
	    mimeType: 'audio/wav',
	    recorderType: RecordRTC.StereoAudioRecorder,
	    disableLogs: false,
	    //timeSlice: 1000, // pass this parameter
	    // both for audio and video tracks
	    bitsPerSecond: 128000,
	    
	    // only for audio track
	    audioBitsPerSecond: 128000,
	    
	    // used by StereoAudioRecorder
	    // the range 22050 to 96000.
	    sampleRate: 96000,

	    // used by StereoAudioRecorder
	    // the range 22050 to 96000.
	    // let us force 16khz recording:
	    desiredSampRate: 16000,

	    // used by StereoAudioRecorder
	    // Legal values are (256, 512, 1024, 2048, 4096, 8192, 16384).
	    bufferSize: 16384,

	    // used by StereoAudioRecorder
	    // 1 or 2
	    numberOfAudioChannels: 1,
	    
	    ondataavailable: function(blob) {
		console.log('dataavailable:e='+blob);
		let fileReader = new FileReader();
		fileReader.onload = (event) => {self._ondata_event_handler(self, event.target.result);};
		fileReader.readAsArrayBuffer(blob);
            }
	};
        self._recorder = RecordRTC(stream, options);
        self._recorder.ondataavailable = ( (blob) => {
	    console.log('!!!!!!!!!!!!!!!!!dataavailable:e='+blob);
            let fileReader = new FileReader();
            fileReader.onload = (event) => {self._ondata_event_handler(self, event.target.result);};
            fileReader.readAsArrayBuffer(blob);
        });
	
	console.log('******************************');
    }

    _media_onopen_old(self, stream, timeslice) {
	console.log('media opened. stream='+stream + " timeslice="+timeslice);
	let options = {
	    type: 'audio',
	    mimeType: 'audio/wav',
	    numberOfAudioChannels: isEdge ? 1 : 2,
	    checkForInactiveTracks: true,
	    bufferSize: 16384,
	    timeSlice: 1000, // pass this parameter
	};
	if (timeslice > 0) {
	    options.timeSlice = 1000;
	    options.ondataavailable = (blob) => {
		console.log('dataavailable:e='+blob);
		let fileReader = new FileReader();
		fileReader.onload = (event) => {self._ondata_event_handler(self, event.target.result);};
		fileReader.readAsArrayBuffer(blob);
            }
	}
	options.recorderType = RecordRTC.StereoAudioRecorder;
	
	if(navigator.platform && navigator.platform.toString().toLowerCase().indexOf('win') === -1) {
	    options.sampleRate = 48000; // or 44100 or remove this line for default
	}
	if(isSafari) {
	    options.sampleRate = 44100;
	    options.bufferSize = 4096;
	    options.numberOfAudioChannels = 1;
	}
	//options.sampleRate = 16000;
	options.numberOfAudioChannels = 1;
        self._recorder = RecordRTC(stream, options);
    }

}

