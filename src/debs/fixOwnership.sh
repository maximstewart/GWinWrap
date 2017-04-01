find . -type f -exec chmod 644 {} +
find . -type d -exec chmod 755 {} +

chown -R root:root ./*/

