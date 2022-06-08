var notification_sound = false
export var set_notification_sound = bool => (notification_sound = bool);

export function send_message(send)
{
    if(send == false){return;};
    if(!document.getElementById("chat_input")){return;};

    var chat_input = document.getElementById("chat_input");
    var message = chat_input.value;

    if(!message){return;};
    send = false;

    $.ajax(
    {
        url: `${window.location.href.split('home')[0]}home/send_message`,
        type:"POST",
        data:{"message":message},
        success:function(res)
        {
            document.getElementById("chat_input").value = "";
            send = true
        }
    });
}

export function create_msg(data)
{
    var msg_direction = data[0];
    var msg = data[1];
    var blue = "#1d2742";
    var red = "#4f212a";

    const msg_container = document.createElement("div");
    msg_container.setAttribute("id", "msg_container");
    msg_container.setAttribute("class", "text");

    const label = document.createElement("label");
    label.setAttribute("id", "msg");
    label.setAttribute("class", "text");
    label.innerHTML = msg;
    msg_container.append(label);

    if(msg_direction == "right"){
        msg_container.style.marginLeft = "40%";
        msg_container.style.backgroundColor = blue;
    }
    else
    {
        msg_container.style.marginRight = "40%";
        msg_container.style.backgroundColor = red;
    }

    if(msg_direction == "left"){sound();};
    return msg_container;
};

function sound()
{
    if(notification_sound == false){return;};
    notification_sound = false;
    var sound = "static/assets/notification_sound.mp3"
    var play = new Audio(sound).play();
};