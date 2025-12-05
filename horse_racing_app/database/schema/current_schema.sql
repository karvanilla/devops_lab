BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO "alembic_version" VALUES('7f4bda760caf');
CREATE TABLE competitions (
	id INTEGER NOT NULL, 
	date DATE NOT NULL, 
	time TIME NOT NULL, 
	location VARCHAR(200) NOT NULL, 
	name VARCHAR(200), 
	PRIMARY KEY (id)
);
CREATE TABLE horse_medical_records (
	id INTEGER NOT NULL, 
	horse_id INTEGER NOT NULL, 
	checkup_date DATE NOT NULL, 
	veterinarian VARCHAR(100) NOT NULL, 
	diagnosis TEXT, 
	treatment TEXT, 
	next_checkup_date DATE, 
	is_healthy BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(horse_id) REFERENCES horses (id)
);
CREATE TABLE horses (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	gender VARCHAR(10) NOT NULL, 
	age INTEGER NOT NULL, 
	owner_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES owners (id)
);
CREATE TABLE jockeys (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	address VARCHAR(200) NOT NULL, 
	age INTEGER NOT NULL, 
	rating FLOAT NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO "jockeys" VALUES(1,'Test Jockey','Test Address',25,4.0);
CREATE TABLE owners (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	address VARCHAR(200) NOT NULL, 
	phone VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE results (
	id INTEGER NOT NULL, 
	competition_id INTEGER NOT NULL, 
	jockey_id INTEGER NOT NULL, 
	horse_id INTEGER NOT NULL, 
	position INTEGER NOT NULL, 
	time VARCHAR(20) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(competition_id) REFERENCES competitions (id), 
	FOREIGN KEY(jockey_id) REFERENCES jockeys (id), 
	FOREIGN KEY(horse_id) REFERENCES horses (id)
);
CREATE TABLE roles (
	id INTEGER NOT NULL, 
	name VARCHAR(50), 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO "roles" VALUES(1,'admin');
INSERT INTO "roles" VALUES(2,'member');
CREATE TABLE roles_users (
	user_id INTEGER NOT NULL, 
	role_id INTEGER NOT NULL, 
	PRIMARY KEY (user_id, role_id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(role_id) REFERENCES roles (id)
);
INSERT INTO "roles_users" VALUES(2,2);
INSERT INTO "roles_users" VALUES(1,1);
CREATE TABLE users (
	id INTEGER NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username)
);
INSERT INTO "users" VALUES(1,'admin','pbkdf2:sha256:600000$UZEwKifvSJF6uFaj$8fec3c727109c8a443f078ff87ded98454a0ad3cd350fcb2cdd92b1b1d3d6a91');
INSERT INTO "users" VALUES(2,'member','pbkdf2:sha256:600000$2FNKqhLpyvkKyrfd$b12e312aed5d168e9b5f6123f23f1cc404d85800bd3663f0a8118414ce431c39');
COMMIT;
