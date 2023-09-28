# ll-scripts
To deploy the ll-scripts's changes, you must run the following commant at the root directory of the service (ex: /ll-transaction):
```shell script
git submodule update --init && cd .ebfiles/scripts && git pull origin master && cd .. && git add scripts/ && cd ..
```
