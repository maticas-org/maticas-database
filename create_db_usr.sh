sudo apt install postgresql
sudo systemctl start postgresql 
sudo systemctl enable postgresql 

#sudo -i -u postgres
sudo -u postgres psql
create user dave with encrypted password '0000';
grant all privileges on database maticas to dave;

ALTER USER dave CREATEDB;

create database maticas;
create database maticas_users;


