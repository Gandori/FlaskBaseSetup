import { create_sidebar_content } from "./sidebar.js";
import { send_message, create_msg, set_notification_sound } from "./chat.js";

var send = true;
window.onload = () => {

    get_data();
    setInterval(get_data,2000);

    //chat
    var chat_btn = document.getElementById("chat_btn");
    if(chat_btn){chat_btn.addEventListener('click', send_message);};
    addEventListener('keydown', input =>{
        if(document.activeElement.tagName == 'INPUT')
        {
            if(input.key != 'Enter'){return;};
            send_message(send)
        }
    })
};

var old_data;
var old_chat_data = [];
function get_data()
{
    $.ajax(
    {
        type:'GET',
        url:window.location.href.split('home')[0] + 'home/get_data',
        success:function(res)
        {
            var data = JSON.parse(res);
            var sidebar_data = data[0];
            var chat_data = data[1];

            if(JSON.stringify(old_data) != JSON.stringify(data))
            {
                old_data = data;

                //sidebar
                if(document.getElementById('sidebar'))
                {
                    var sidebar = document.getElementById('sidebar');
                    while(sidebar.firstChild){sidebar.firstChild.remove();};
                    sidebar_data.forEach(element => {
                        sidebar.append(create_sidebar_content(element));
                    });
                }

                //chat
                if(document.getElementById('chat_content'))
                {
                    var old_chat = JSON.stringify(old_chat_data);
                    var new_chat = JSON.stringify(chat_data)

                    if(old_chat == new_chat){return;};

                    for(let i = 0; i < chat_data.length; i++)
                    {
                        if(JSON.stringify(chat_data[i]) !== JSON.stringify(old_chat_data[i]))
                        {
                            old_chat_data.push(chat_data[i]);

                            var chat_content = document.getElementById('chat_content');
                            chat_content.append(create_msg(chat_data[i]));
                            chat_content.scrollBy(chat.scrollTop, chat.scrollHeight); 
                        }
                    }
                }
                set_notification_sound(true)
            }
        }
    });
}