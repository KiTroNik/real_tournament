const roomName = JSON.parse(document.getElementById('room-name').textContent);

    const lobbySocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/lobby/'
        + roomName
        + '/'
    );

    lobbySocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data['message'] === 'exit') {
            document.querySelector('#number_of_players').innerHTML = 'Twórca pokoju wyszedł z gry. Stwórz własną lub dołącz do istniejącej';
        } else if (data['message'] === 'start_game') {
            window.location.replace('http://127.0.0.1:8000/game/' + roomName);
            document.querySelector('#number_of_players').innerHTML = 'kurwaa jebana';
        }//} else {
        //    document.querySelector('#number_of_players').innerHTML = data['message'];
       // }
    };

    lobbySocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#start_game').onkeyup = function(e) {
        if (e.keyCode === 13) {
                document.querySelector('#start_game').click();
        }
    };

    document.querySelector('#start_game').onclick = function(e) {
        lobbySocket.send(JSON.stringify({
            'message': {
                'event': 'start',
            }
        }));
    };