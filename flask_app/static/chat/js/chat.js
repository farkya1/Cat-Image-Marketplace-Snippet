var socket;
$(document).ready(function(){
    
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        socket.emit('joined', {});
    });
    
    socket.on('status', function(data) {     
        let tag  = document.createElement("p");
        let text = document.createTextNode(data.msg);
        let element = document.getElementById("chat");
        tag.appendChild(text);
        tag.style.cssText = data.style;
        element.appendChild(tag);
        $('#chat').scrollTop($('#chat')[0].scrollHeight);

    });
});
function sendMessage(event){

    var messageSent = document.getElementsByName("messageSent")[0].value;
    socket.emit('message', messageSent);
    document.getElementsByName("messageSent")[0].value =  document.getElementsByName("messageSent")[0].ariaPlaceholder;

}

function leaving(event){
    socket.emit('leaving');
    window.location.href = "/home";

}