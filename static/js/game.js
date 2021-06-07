const roomName = JSON.parse(document.getElementById('room-name').textContent);

    const lobbySocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/game/'
        + roomName
        + '/'
    );

    let answers;

    lobbySocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data['message']['event'] === 'exit') {
            document.querySelector('#creator_left').innerHTML = 'Sorry the creator of the room have left the game. You can leave now.';
        } else if (data['message']['event'] === 'change_question') {
            let question_json = JSON.parse(data['message']['data']);
            answers = question_json[0]['answer'];
            document.querySelector('#question').innerHTML = question_json[0]['title'];
            document.querySelector('#first').innerHTML = question_json[0]['answer'][0]['answer_text'];
            document.querySelector('#second').innerHTML = question_json[0]['answer'][1]['answer_text'];
            document.querySelector('#third').innerHTML = question_json[0]['answer'][2]['answer_text'];
            document.querySelector('#fourth').innerHTML = question_json[0]['answer'][3]['answer_text'];
            enableQuestions();
            resetStyle();
        } else if (data['message']['event'] === 'show_results') {
            let results_json = JSON.parse(data['message']['data']);
            document.querySelector('#question').innerHTML = 'WYNIKI: ';
            document.querySelector('#first').innerHTML = '';
            document.querySelector('#second').innerHTML = '';
            document.querySelector('#third').innerHTML = '';
            document.querySelector('#fourth').innerHTML = '';
            document.querySelector('#right_answer').innerHTML = '';

            let ul = document.createElement('ul');
            document.getElementById('results').appendChild(ul);
            results_json.forEach(function (item) {
                    let li = document.createElement('li');
                    ul.appendChild(li);
                    li.innerHTML += item.username + ' PUNKTY: ' + item.points;
            });
            document.querySelector('#next').onclick = false;
        }
    };

    lobbySocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#next').onclick = function(e) {
        lobbySocket.send(JSON.stringify({
            'message': {
                'event': 'next_question',
                'data': '',
            }
        }));
    };

    function disableQuestions() {
        document.querySelectorAll('.answer').forEach(el => {el.onclick = false;})
    }

    function enableQuestions() {
        document.querySelectorAll('.answer').forEach((el, i) => {el.onclick = () => checkAnswer(i, el);})
    }

    function checkAnswer(i, p) {
        if (answers[i]['is_right']) {
            p.style.color = 'green';
            lobbySocket.send(JSON.stringify({
                'message': {
                    'event': 'add_point',
                    'data': '',
                }
            }));
        } else {
            p.style.color = 'red';
        }

        for (let j = 0; j < 4; j++) {
            if (answers[j]['is_right']) {
                document.querySelector('#right_answer').innerHTML = 'Prawidłowa odpowiedź: ' + answers[j]['answer_text'];
            }
        }

        disableQuestions();
    }

    function resetStyle() {
        document.querySelectorAll('.answer').forEach(el => {el.style.color = 'black';})
        document.querySelector('#right_answer').innerHTML = '';
    }
