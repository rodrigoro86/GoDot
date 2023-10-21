extends Node2D


var socket = WebSocketPeer.new()
var json = JSON.new()

func process_websocket():
	var state = socket.get_ready_state()
	if state == WebSocketPeer.STATE_OPEN:
		while socket.get_available_packet_count():
			print("Packet: ", socket.get_packet().get_string_from_utf8())
	elif state == WebSocketPeer.STATE_CLOSING:
		# Keep polling to achieve proper close.
		pass
	elif state == WebSocketPeer.STATE_CLOSED:
		var code = socket.get_close_code()
		var reason = socket.get_close_reason()
		print("WebSocket closed with code: %d, reason %s. Clean: %s" % [code, reason, code != -1])
		set_process(false) # Stop processing.

func send_data():
	var data = {
		"key1": "Teste"
	}
	socket.send_text(JSON.stringify(data))
	

func _ready():
	socket.connect_to_url("ws://127.0.0.1:8000/ws_text")
	
	
func _process(delta):
	socket.poll()
	process_websocket()
	send_data()
	
