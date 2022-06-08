create table if not exists users (
    name Text,
    password Text,
    status Text,
    img text
);
create table if not exists chats (
    id text,
    user1 Text,
    user2 Text,
    msg Text
);
create table if not exists currentchatpartner (
    user1 Text,
    user2 Text
);
create table if not exists admin (
    user Text,
    password Text
);
insert into admin values(
    'admin',
    'admin'
)