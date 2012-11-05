begin;
--Add a color for message types
alter table message_type add column color character varying(7);
--Add an icon for message type
alter table message_type add column icon character varying(200);

--Message table changes
alter table "Message" add column contact character varying(200);
alter table "Message" add column contact_mail character varying(200); 
alter table "Message" add column contact_phone character varying(200); 
alter table "Message" add column source character varying(255);
alter table "Message" add column expired_date timestamp without time zone;
alter table "Message" add column edit_key character varying(40);

update "config" set value='67' where key='db_version';
commit;
