const { encode, decode } = MessagePack.initialize(2**22);

class WSClient {

    constructor(wsd) {
	this.WSD = wsd;
	this.EVENT = wsd.EVENT;
	this.encode = encode;
	this.decode = decode;

	this.next_rid = () =>
	    {return this._next_rid(this);};
	
	this.set_onopen_event_handler = (handler) =>
	    {this._onopen_event_handler = handler;};

	this.set_onmessage_handler = (event_id, handler) =>
	    {this._onmessage_handlers[event_id] = handler;};

	this.set_onmessage_default_handler = (handler) =>
	    {this._onmessage_default_handler = handler;};
	
	this.send = (request_id, event_id, data) =>
	    {this._send(this, request_id, event_id, data)};

	
	this._last_rid = 0;
	
	this._ws = new WebSocket(wsd.websocket_url);
	this._ws.binaryType = 'arraybuffer';
	this._ws.onopen = 
	    (event) => {this._ws_onopen(this, event)};
	this._ws.onmessage = 
	    (event) => {this._ws_onmessage(this, event)};

	this._onopen_event_handler = null;
	this._onmessage_default_handler =
	    (rid, eid, data) => {console.log("unhnalded message:"+eid+":"+data);};
	this._onmessage_handlers = {};
	
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
	const [rid, eid, data] = self.decode(MessagePack.Buffer.from(event.data));
	const handler = self._onmessage_handlers[eid];
	if (handler != null) {
	    handler(rid, eid, data);
	} else if (eid == self.EVENT.ALIVE_MONITORING) {
	    console.log('alive...')
	} else {
	    self._onmessage_default_handler(rid, eid, data);
	}
    }

}
    
class SimpleMediaRecorder {

    constructor(wsd) {
	this._recorder = null;
	this.audio = document.querySelector('audio');
	
	this.open_user_media =
	    (constraints) => {this._open_user_media(this, constraints)};    //{ audio: true }
	this.start_recording = 
	    (timeslice = null) => {this._start_recording(this, timeslice)};
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

    _start_recording(self, timeslice) {
	if (timeslice > 0) {
	    //console.log("start_recording method called. timeslice="+timeslice);
	    //self._recorder.start(timeslice);
	    self._recorder.startRecording();
	} else {
	    //console.log("start_recording method called. without timeslice:"+timeslice);
	    //self._recorder.start();
	    self._recorder.startRecording();
	}
    }

    _stop_recording(self) {
	//console.log("stop_recording method called.");
	self._recorder.stopRecording( () => {
	    if(self._recorder_event_handler != null) {
		const blob = self._recorder.getBlob()
		console.log('close:blob='+blob);
		let fileReader = new FileReader();
		fileReader.onload = (event) => {self._ondata_event_handler(self, event.target.result);};
		fileReader.readAsArrayBuffer(blob);
		self._recorder_event_handler('stop', '')
	    }
	});

    }

    _open_user_media(self, constraints) {
//	navigator.mediaDevices.getUserMedia(constraints) 
//	    .then((stream) => {self._media_onopen(self, stream)});
	navigator.mediaDevices.getUserMedia({audio: {echoCancellation: false}})
	    .then((stream) => {self._media_onopen(self, stream)});
    }
    
    _media_onopen(self, stream) {
	console.log('media opened. stream='+stream);
	
	if(isSafari) {
	    self.audio.muted = true;
	    self.audio.srcObject = stream;
	    
	    btnStartRecording.disabled = false;
	    btnStartRecording.style.border = '1px solid red';
	    btnStartRecording.style.fontSize = '150%';

	    alert('Please click startRecording button again. First time we tried to access your microphone. Now we will record it.');
	    return;
	}


	self.audio.muted = true;
	self.audio.srcObject = stream;

	var options = {
	    type: 'audio',
	    mimeType: 'audio/wav',
	    numberOfAudioChannels: isEdge ? 1 : 2,
	    checkForInactiveTracks: true,
	    bufferSize: 16384
	};
	
	if(isSafari || isEdge) {
	    options.recorderType = StereoAudioRecorder;
	}

	if(navigator.platform && navigator.platform.toString().toLowerCase().indexOf('win') === -1) {
	    options.sampleRate = 48000; // or 44100 or remove this line for default
	}

	if(isSafari) {
	    options.sampleRate = 44100;
	    options.bufferSize = 4096;
	    options.numberOfAudioChannels = 2;
	}

	options.recorderType = RecordRTC.StereoAudioRecorder
	
        self._recorder = RecordRTC(stream, options);
	
        self._recorder.ondataavailable = ( (blob) => {
	    console.log('dataavailable:e='+blob);
            let fileReader = new FileReader();
            fileReader.onload = (event) => {self._ondata_event_handler(self, event.target.result);};
            fileReader.readAsArrayBuffer(blob);
        });
	
    }

}

