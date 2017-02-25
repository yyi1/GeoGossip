/**
 * Created by baishi on 11/19/16.
 */
var group_id = null;
var group_name = null;
var user_id = null;
var username = null;

$(document).ready(function () {
    var myApp = new Framework7();
    var $$ = Dom7;
    var messageLayout = $('#message_layout');
    group_id = $('#group_id').val();
    group_name = $('#group-name').html();
    user_id = $('#user_id').val();
    username = $('#username').val();
    // Init Messages
    var myMessages = myApp.messages('.messages', {
        autoLayout:true
    });
    // Init Messagebar
    var myMessagebar = myApp.messagebar('.messagebar');

    var socket = new WebSocket("wss://" + window.location.host + "/" + group_id + "/");

    socket.onmessage = function (e) {
        var data = JSON.parse(e.data);
        var datetime = new Date(data['time']);
        switch (data['type']) {
            case 'online':
                messageLayout.append(
                    '<div class="messages-date">' +
                    data['username'] +
                    ' has joined this group.<span>\t\t' +
                    datetime.getFullYear() +
                    '.' +
                    datetime.getMonth() +
                    '.' +
                    datetime.getDate() +
                    '\t' +
                    datetime.getHours() +
                    ':' +
                    datetime.getMinutes() +
                    '</span></div>'
                );
                break;
            case 'offline':
                messageLayout.append(
                    '<div class="messages-date">' +
                    data['username'] +
                    ' has left this group.<span>\t\t' +
                    datetime.getFullYear() +
                    '.' +
                    datetime.getMonth() +
                    '.' +
                    datetime.getDate() +
                    '\t' +
                    datetime.getHours() +
                    ':' +
                    datetime.getMinutes() +
                    '</span></div>'
                );
                break;
            case 'message':
                myMessages.appendMessage({
                  text: data['content'],
                  type: (data['user_id'] == user_id) ? 'sent' : 'received',
                  avatar: '/geogossip/avatar/' + data['user_id'],
                  name: data['username']
                }, true);
                break;
            case 'alert':
                alert(data['content']);
                break;
            default:
                console.log('Unknown socket message type: ' + data['type']);
        }
    };

    socket.onclose = function () {
        alert('You are disconnected, please login again!');
    };

    // Handle message
    $$('#send').click(function () {
        var messageText = myMessagebar.value().trim();
    // Exit if empy message
        if (messageText.length === 0) {
            alert('Cannot send empty content');
            return;
        }

        socket.send(messageText);

        // Empty messagebar
        myMessagebar.clear();
    });
});
