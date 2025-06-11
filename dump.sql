create table Askos_lingua
(
    id   integer     not null
        primary key autoincrement,
    nome varchar(50) not null
        unique
);

create table Askos_staff
(
    cod_fiscale varchar(16)  not null
        primary key,
    nome        varchar(50)  not null,
    cognome     varchar(50)  not null,
    telefono    varchar(20)  not null,
    email       varchar(254) not null,
    ruolo       varchar(10)  not null
);

create table Askos_staff_lingue
(
    id        integer     not null
        primary key autoincrement,
    staff_id  varchar(16) not null
        references Askos_staff
            deferrable initially deferred,
    lingua_id bigint      not null
        references Askos_lingua
            deferrable initially deferred
);

create index Askos_staff_lingue_lingua_id_e7b166fd
    on Askos_staff_lingue (lingua_id);

create index Askos_staff_lingue_staff_id_6640b678
    on Askos_staff_lingue (staff_id);

create unique index Askos_staff_lingue_staff_id_lingua_id_0bea4269_uniq
    on Askos_staff_lingue (staff_id, lingua_id);

create table Askos_tour
(
    id        integer      not null
        primary key autoincrement,
    nome      varchar(100) not null,
    data      date         not null,
    durata    varchar(50)  not null,
    prezzo    decimal      not null,
    lingua_id bigint
        references Askos_lingua
            deferrable initially deferred
);

create index Askos_tour_lingua_id_243f1b18
    on Askos_tour (lingua_id);

create table Askos_tour_driver
(
    id       integer     not null
        primary key autoincrement,
    tour_id  bigint      not null
        references Askos_tour
            deferrable initially deferred,
    staff_id varchar(16) not null
        references Askos_staff
            deferrable initially deferred
);

create index Askos_tour_driver_staff_id_ed0a0820
    on Askos_tour_driver (staff_id);

create index Askos_tour_driver_tour_id_43611453
    on Askos_tour_driver (tour_id);

create unique index Askos_tour_driver_tour_id_staff_id_135ea14e_uniq
    on Askos_tour_driver (tour_id, staff_id);

create table Askos_tour_guide
(
    id       integer     not null
        primary key autoincrement,
    tour_id  bigint      not null
        references Askos_tour
            deferrable initially deferred,
    staff_id varchar(16) not null
        references Askos_staff
            deferrable initially deferred
);

create index Askos_tour_guide_staff_id_49fb5557
    on Askos_tour_guide (staff_id);

create index Askos_tour_guide_tour_id_021c91e6
    on Askos_tour_guide (tour_id);

create unique index Askos_tour_guide_tour_id_staff_id_cbec900e_uniq
    on Askos_tour_guide (tour_id, staff_id);

create table auth_group
(
    id   integer      not null
        primary key autoincrement,
    name varchar(150) not null
        unique
);

create table auth_user
(
    id           integer      not null
        primary key autoincrement,
    password     varchar(128) not null,
    last_login   datetime,
    is_superuser bool         not null,
    username     varchar(150) not null
        unique,
    last_name    varchar(150) not null,
    email        varchar(254) not null,
    is_staff     bool         not null,
    is_active    bool         not null,
    date_joined  datetime     not null,
    first_name   varchar(150) not null
);

create table Askos_cliente
(
    user_id             integer     not null
        primary key
        references auth_user
            deferrable initially deferred,
    cod_fiscale         varchar(16) not null
        unique,
    telefono            varchar(20) not null,
    lingua_preferita_id bigint
        references Askos_lingua
            deferrable initially deferred
);

create index Askos_cliente_lingua_preferita_id_47d0c304
    on Askos_cliente (lingua_preferita_id);

create table Askos_prenotazione
(
    id                integer          not null
        primary key autoincrement,
    data_prenotazione date             not null,
    num_partecipanti  integer unsigned not null,
    cliente_id        integer          not null
        references Askos_cliente
            deferrable initially deferred,
    tour_id           bigint           not null
        references Askos_tour
            deferrable initially deferred,
    check ("num_partecipanti" >= 0)
);

create index Askos_prenotazione_cliente_id_950c6cd7
    on Askos_prenotazione (cliente_id);

create index Askos_prenotazione_tour_id_adbff5f3
    on Askos_prenotazione (tour_id);

create table Askos_recensione
(
    id         integer          not null
        primary key autoincrement,
    voto       integer unsigned not null,
    commento   text             not null,
    data       datetime         not null,
    cliente_id integer          not null
        references Askos_cliente
            deferrable initially deferred,
    tour_id    bigint           not null
        references Askos_tour
            deferrable initially deferred,
    check ("voto" >= 0)
);

create index Askos_recensione_cliente_id_b469149d
    on Askos_recensione (cliente_id);

create unique index Askos_recensione_cliente_id_tour_id_1c889db4_uniq
    on Askos_recensione (cliente_id, tour_id);

create index Askos_recensione_tour_id_3eb84238
    on Askos_recensione (tour_id);

create table auth_user_groups
(
    id       integer not null
        primary key autoincrement,
    user_id  integer not null
        references auth_user
            deferrable initially deferred,
    group_id integer not null
        references auth_group
            deferrable initially deferred
);

create index auth_user_groups_group_id_97559544
    on auth_user_groups (group_id);

create index auth_user_groups_user_id_6a12ed8b
    on auth_user_groups (user_id);

create unique index auth_user_groups_user_id_group_id_94350c0c_uniq
    on auth_user_groups (user_id, group_id);

create table django_content_type
(
    id        integer      not null
        primary key autoincrement,
    app_label varchar(100) not null,
    model     varchar(100) not null
);

create table auth_permission
(
    id              integer      not null
        primary key autoincrement,
    content_type_id integer      not null
        references django_content_type
            deferrable initially deferred,
    codename        varchar(100) not null,
    name            varchar(255) not null
);

create table auth_group_permissions
(
    id            integer not null
        primary key autoincrement,
    group_id      integer not null
        references auth_group
            deferrable initially deferred,
    permission_id integer not null
        references auth_permission
            deferrable initially deferred
);

create index auth_group_permissions_group_id_b120cbf9
    on auth_group_permissions (group_id);

create unique index auth_group_permissions_group_id_permission_id_0cd325b0_uniq
    on auth_group_permissions (group_id, permission_id);

create index auth_group_permissions_permission_id_84c5c92e
    on auth_group_permissions (permission_id);

create index auth_permission_content_type_id_2f476e4b
    on auth_permission (content_type_id);

create unique index auth_permission_content_type_id_codename_01ab375a_uniq
    on auth_permission (content_type_id, codename);

create table auth_user_user_permissions
(
    id            integer not null
        primary key autoincrement,
    user_id       integer not null
        references auth_user
            deferrable initially deferred,
    permission_id integer not null
        references auth_permission
            deferrable initially deferred
);

create index auth_user_user_permissions_permission_id_1fbb5f2c
    on auth_user_user_permissions (permission_id);

create index auth_user_user_permissions_user_id_a95ead1b
    on auth_user_user_permissions (user_id);

create unique index auth_user_user_permissions_user_id_permission_id_14a6b632_uniq
    on auth_user_user_permissions (user_id, permission_id);

create table django_admin_log
(
    id              integer           not null
        primary key autoincrement,
    object_id       text,
    object_repr     varchar(200)      not null,
    action_flag     smallint unsigned not null,
    change_message  text              not null,
    content_type_id integer
        references django_content_type
            deferrable initially deferred,
    user_id         integer           not null
        references auth_user
            deferrable initially deferred,
    action_time     datetime          not null,
    check ("action_flag" >= 0)
);

create index django_admin_log_content_type_id_c4bce8eb
    on django_admin_log (content_type_id);

create index django_admin_log_user_id_c564eba6
    on django_admin_log (user_id);

create unique index django_content_type_app_label_model_76bd3d3b_uniq
    on django_content_type (app_label, model);

create table django_migrations
(
    id      integer      not null
        primary key autoincrement,
    app     varchar(255) not null,
    name    varchar(255) not null,
    applied datetime     not null
);

create table django_session
(
    session_key  varchar(40) not null
        primary key,
    session_data text        not null,
    expire_date  datetime    not null
);

create index django_session_expire_date_a5c62663
    on django_session (expire_date);


