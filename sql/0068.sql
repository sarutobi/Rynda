begin;

alter table "Location" rename longtitude to longitude;

update config set value='0.68' where key='db_version';
commit;
