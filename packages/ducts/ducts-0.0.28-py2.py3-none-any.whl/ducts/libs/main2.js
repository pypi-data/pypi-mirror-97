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
	    (event) => {this._ws_onopen(this, event)};
	this._ws.onmessage = 
	    (event) => {this._ws_onmessage(this, event)};

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

    }
    
    _start_recording(self, timeslice) {
	if (timeslice > 0) {
	    //console.log("start_recording method called. timeslice="+timeslice);
	    self._recorder.start(timeslice);
	} else {
	    //console.log("start_recording method called. without timeslice:"+timeslice);
	    self._recorder.start();
	}
    }

    _stop_recording(self) {
	//console.log("stop_recording method called.");
	self._recorder.stop();
    }

    _open_user_media(self, constraints) {
	navigator.mediaDevices.getUserMedia(constraints) 
	    .then((stream) => {self._media_onopen(self, stream)});
    }
    
    _media_onopen(self, stream) {
	console.log('media opened. stream='+stream);
        self._recorder = new MediaRecorder(stream);
        self._recorder.addEventListener('dataavailable', (blob) => {
	    console.log('dataavailable:e='+blob);
            let fileReader = new FileReader();
            fileReader.onload = (event) => {self._ondata_event_handler(self, event);};
            fileReader.readAsArrayBuffer(blob.data);
        });

	self._recorder.addEventListener('onerror', (e) => {
	    if(self._recorder_error_handler != null) {
		self._recorder_error_handler(e)
	    }
	});

	self._recorder.addEventListener('start', (e) => {
	    if(self._recorder_event_handler != null) {
		self._recorder_event_handler('start', e)
	    }
	});
	
	self._recorder.addEventListener('stop', (e) => {
	    if(self._recorder_event_handler != null) {
		self._recorder_event_handler('stop', e)
	    }
	});
	
    }

}

