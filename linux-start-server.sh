#!/bin/sh

export JAVA_HOME=/home/demobin/jdk1.8.0_60
export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$CLASSPATH

java -version >/dev/null 2>&1
if [ $? != 0 ];then
    echo "No Java Environment!"
    exit 1
fi

DIR=/home/demobin/$1
JAR_NAME=$1
JAR_FILE=$DIR/$JAR_NAME*.jar
JAVA_OPTS="-Xms128m -Xmx1024m -XX:PermSize=128M -XX:MaxNewSize=256m -XX:MaxPermSize=512m -Dfile.encoding=UTF-8"
PID_FILE=$DIR/pid
LOG_NAME=$1
LOG_FILE="$DIR/log/$LOG_NAME.log"

echo "1 : $1"
echo "2 : $2"
echo "dir : $DIR"
echo "jar_name : $JAR_NAME"
echo "jar_file : $JAR_FILE"
echo "pid_file : $PID_FILE"
echo "log_file : $LOG_FILE"

function checkrun {
    if [[ -f $PID_FILE ]]; then
        PID=$(cat $PID_FILE)
        ps -ef | awk '{ print $2 }' | grep -e "^${PID}$"
        if [ $? -eq 0 ]; then
            RETVAL=1
        else
            RETVAL=0
        fi
    else
        RETVAL=0
        return $RETVAL
    fi
}

function status {
checkrun
    if [ $RETVAL -eq 1 ]; then
        echo "[INFO] $JAR_NAME is running..."
    else
        echo "[INFO] $JAR_NAME is stopped."
    fi
}

function stop {
    checkrun
    if [ $RETVAL -eq 1 ]; then
        if [[ -f $PID_FILE ]]; then
            PID=$(cat $PID_FILE)
            kill -15 $PID 1>/dev/null 2>&1
            if [ $? -eq 0 ]; then
              time=0
                ps -ef | awk '{ print $2 }' | grep -e "^${PID}$"
                while [[ $? -eq 0 ]];
                do
                    sleep 1
                    let "time+=1"
                    echo "[INFO]$time second $JAR_NAME is stopping"
                    ps -ef | awk '{ print $2 }' | grep -e "^${PID}$"
               done
                echo "[INFO][OK] $JAR_NAME is stopped."
                rm -rf $PID_FILE
            fi
        fi
    else
        echo "[WARN] $JAR_NAME has stopped."
    fi

}

function start {
    checkrun
    if [ $RETVAL -eq 0 ]; then
        echo "-- Starting "$JAR_NAME"..."
        nohup java  $JAVA_OPTS -jar ${JAR_FILE} --logging.file=$LOG_FILE >/dev/null 2>&1 &
        echo $! > $PID_FILE
        echo "[INFO][OK] "$JAR_NAME" Started."
        sleep 2
        checklog yes
    else
        echo "[ERR] "$JAR_NAME" already running."
    fi
}

function relink {
    target=$(find $DIR -regex '^.*-[0-9]*\.jar$' -type f | sort | tail -n 1)
    rm -rf $JAR_FILE 2> /dev/null
    ln -s $target $JAR_FILE
    echo "[INFO][OK] Relinked."
}

function autoremove {
    count=$(find $DIR -regex '^.*-[0-9]*\.jar$' | wc -l)

    if [ "$count" -gt 1 ]
    then
        find $IDR -regex '^.*-[0-9]*\.jar$' -type f | sort | sed -e '$ d' | xargs rm -rf 2>/dev/null
        echo "[INFO][OK] Autoremoved."
    fi
}


checklog(){
  tail -n 50 $LOG_FILE
}


log(){
  status
  if [ $RETVAL -eq 0 ]; then
    echo "[WARN] $JAR_NAME is stopped"
  fi
  checklog yes
}

function help {
    echo "Parameter: start | stop | restart | status | log"
}

case $2 in
    stop )
        stop
        ;;
    start )
        start
        ;;
    restart )
        stop
       start
        ;;
    relink )
        relink
        ;;
    autoremove )
        autoremove
        ;;
    status )
        status
        ;;
    log )
        log
        ;;
    all )
        stop
        relink
        start
#        autoremove
        ;;
    * )
        help
esac

exit 0
