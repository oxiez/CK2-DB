



DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS Marriage;
DROP TABLE IF EXISTS Trait;
DROP TABLE IF EXISTS TraitLookup;
DROP TABLE IF EXISTS Dynasty;
DROP TABLE IF EXISTS Title;
DROP TABLE IF EXISTS Rulers;
DROP TABLE IF EXISTS Claim;
DROP TABLE IF EXISTS Province;
DROP TABLE IF EXISTS Barony;
DROP TABLE IF EXISTS Religion;
DROP TABLE IF EXISTS Culture;
DROP TABLE IF EXISTS Religion;
DROP TABLE IF EXISTS Culture;
DROP TABLE IF EXISTS BloodLines;
DROP TABLE IF EXISTS BloodLineMembers;


CREATE TABLE Person(
	personID INT PRIMARY KEY, 
	birthName VARCHAR(63), 
	dynastyID INT, 
	isMale BOOLEAN, 
	birthday DATE, 
	deathday DATE, 
	fatherID INT,  
	real_fatherID INT, 
	motherID INT,  
	religionID INT, 
	cultureID INT, 
	fertility FLOAT, 
	health FLOAT, 
	wealth FLOAT, 
	prestige FLOAT, 
	piety FLOAT,
	hostID INT,   
	employerID INT, 
	martial INT, 
	diplomacy INT, 
	stewardship INT, 
	intrigue INT, 
	learning INT
);

CREATE TABLE Marriage(
	personID INT,
	spouseID INT,
	PRIMARY KEY(personID, spouseID)
);

CREATE TABLE Trait(
	personID INT, 
	traitID INT,
	PRIMARY KEY(personID,traitID)
);

CREATE TABLE TraitLookup(
	traitID INT PRIMARY KEY, 
	traitName VARCHAR(63) 
);

CREATE TABLE Dynasty(
	dynastyID INT PRIMARY KEY, 
	dynastyName VARCHAR(63),
	cultureID INT,
	religionID INT
);

CREATE TABLE Title(
	id VARCHAR(63) PRIMARY KEY, 
	holderid INT,
	name VARCHAR(63), 
	level CHAR(1), 
	deFactoLeige VARCHAR(63), 
	deJureLeige VARCHAR(63)
);
CREATE TABLE Rulers(
	personID INT, 
	titleID VARCHAR(63),
	PRIMARY KEY(personID,titleID)
);

CREATE TABLE Claim(
	personID INT, 
	titleID VARCHAR(63),
	pressed BOOLEAN,
	weak BOOLEAN,
	PRIMARY KEY(personID,titleID)
);

CREATE TABLE Province(
	provinceID INT PRIMARY KEY, 
	name VARCHAR(63), 
	countyID VARCHAR(63), 
	culture VARCHAR(63), 
	religion VARCHAR(63)
);

CREATE TABLE Barony(
	name VARCHAR(63) PRIMARY KEY,
	province INT,  
	type VARCHAR(63)
);

CREATE TABLE Religion(
	religionID INT PRIMARY KEY, 
	religionName VARCHAR(63), 
	heresy BOOLEAN,  
	parent VARCHAR(63),
	religionGroup VARCHAR(63)
	
);

CREATE TABLE Culture(
	cultureID INT PRIMARY KEY, 
	cultureName VARCHAR(63), 
	cultureGroup VARCHAR(63)
);

CREATE TABLE BloodLineMembers(
	personID INT,
	bloodLineID INT,
	PRIMARY KEY(personID, bloodLineID)
);

CREATE TABLE BloodLines(
	bloodlineID INT PRIMARY KEY,
	bloodlineName VARCHAR(63),
	founderID INT
);
