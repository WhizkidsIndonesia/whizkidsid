#!/bin/sh
echo Backup DB from remote machine..
ssh root@do-whizkidsid 'pg_dump -U postgres -p 5438 -h localhost -d postgres > ~/latest-backup.db && zip latest-backup.db.zip latest-backup.db'
echo Copying to /var/tmp..
scp root@do-whizkidsid:~/latest-backup.db.zip /var/tmp
echo Restoring backup..
unzip -o /var/tmp/latest-backup.db.zip -d /var/tmp
dropdb  -U postgres -p 5438 -h localhost postgres
createdb  -U postgres -p 5438 -h localhost postgres
psql  -U postgres -p 5438 -h localhost -d postgres -f /var/tmp/latest-backup.db
echo Done.
