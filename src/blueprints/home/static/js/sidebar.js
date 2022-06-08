export function create_sidebar_content(data)
{
    var username = data[0];
    var status = data[1];
    var img = data[2];

    var sidebar_content = create_div('sidebar_content');
    sidebar_content.append(create_sidebar_img(img, username));

    var sidebar_content_container = create_div('sidebar_content_container');
    sidebar_content_container.append(create_label('username',username));
    sidebar_content_container.append(create_label('userstatus',status));
    sidebar_content.append(sidebar_content_container);

    return sidebar_content;
};

function create_div(id)
{
    var div = document.createElement('div');
    div.setAttribute('id', id);
    return div;
};

function create_sidebar_img(url, username)
{
    var img = document.createElement('img');
    img.setAttribute('id', 'sidebar_img');
    img.addEventListener('click', () => {click_on_img(img, username)})

    if(url == 'None'){img.setAttribute('src', 'static/assets/imagefail.png');}
    else{img.setAttribute('src', `./../static/${url}`);}
    return img;
};

function click_on_img(img_element, username)
{
    if(document.getElementById('dropdown_info'))
    {
        document.getElementById('dropdown_info').remove();
    }
    var div = create_div('dropdown_info');
    img_element.parentElement.append(div);

    var img_url = img_element.getAttribute('src');

    var a = document.createElement('a');
    a.setAttribute('id', 'sidebar_img');
    a.style.margin = 'auto';
    a.style.background = `url(${img_url})`;
    a.style.backgroundSize = '100% 100%';
    a.setAttribute('href', `${window.location.href.split('home')[0]}home/profile?user=${username}`);
    div.append(a);
    
    var label = create_label('',username);
    div.append(label);

    var a = document.createElement('a');;
    a.setAttribute('class', 'btn');
    a.style.fontSize = 'calc(var(--font_size) - 5px)';
    a.innerHTML = 'Nachricht';
    a.style.textDecoration = 'none';
    a.setAttribute('href', `${window.location.href.split('home')[0]}home/chat?user=${username}`);
    div.append(a);
};

function create_label(id, txt)
{
    var label = document.createElement('label');
    label.setAttribute('id',id);
    if(txt == 'offline'){label.style.color = 'red';};
    if(txt == 'online'){label.style.color = 'green';};
    label.innerHTML = txt;
    return label;
};