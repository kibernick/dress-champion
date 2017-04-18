# DressChampion

*To promote something is to champion it.*

## Setup databases

```bash
$ mysql -uroot
CREATE USER 'dresschampuser'@'localhost' IDENTIFIED BY {PASSWORD};
CREATE DATABASE dresschamp;
GRANT ALL PRIVILEGES ON dresschamp.* To 'dresschampuser'@'localhost';
CREATE DATABASE dresschamp_test;
GRANT ALL PRIVILEGES ON dresschamp_test.* To 'dresschampuser'@'localhost';
FLUSH PRIVILEGES;
```
