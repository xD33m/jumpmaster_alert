import React, { useEffect, useRef, useState } from "react";
import styles from "components/terminal/Terminal.module.scss";
import { PushSpinner } from "react-spinners-kit";
import TerminalMessage from "./TerminalMessage";
import { useInterval } from "utils/hooks";

const Terminal = ({
  logs,
  setLogs,
  jumpDetectionRunning,
  setJumpDetectionRunning,
  removeAllLoadingStates,
}) => {
  const messagesEndRef = useRef(null);

  // const [timer, setTimer] = useState(0);
  const [count, setCount] = useState(0);
  // const [currentJumpStatus, setCurrentJumpStatus] = useState(jumpDetectionRunning);
  // const [currentCharStatus, setCurrentCharStatus] = useState(charDetectionRunning);
  // const [currentInterval, setCurrentInterval] = useState();
  // const [loading, setLoading] = useState(false);

  useInterval(
    () => {
      const [time] = new Date().toTimeString().split(" ");
      const fullLog = {
        time,
        message: `Looking for jumpmaster... (${count}/120)`,
        loading: true,
        type: "jumpmaster",
      };
      const lastLog = logs[logs.length - 1];

      // Increase Counter
      setCount((prevCount) => prevCount + 1);

      if (lastLog.message.includes("jumpmaster")) {
        // Replace last log with new counter
        setLogs((prevLogs) => {
          return [...prevLogs.filter((log) => log !== lastLog), fullLog];
        });
      } else {
        // if something went inbetween the last log and the current log
        removeAllLoadingStates();
        // Print on new line
        setLogs((prevLogs) => {
          return [...prevLogs, fullLog];
        });
      }

      if (count === 120) {
        // just to be sure
        setJumpDetectionRunning(false);
        setCount(0);
      }
    },
    jumpDetectionRunning ? 1000 : null
  );

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [logs]);

  useEffect(() => {
    if (!jumpDetectionRunning) {
      setCount(0);
    }
  }, [jumpDetectionRunning]);

  // useEffect(() => {
  //   // if type = jumpmasterDetection && laoding = true
  //   if (jumpDetectionRunning !== currentJumpStatus) {
  //     setCurrentJumpStatus(jumpDetectionRunning);
  //     if (jumpDetectionRunning) {
  //       if (!currentInterval) {
  //         const interval = setInterval(() => setTimer((prevVal) => prevVal + 1), 1000);
  //         setCurrentInterval(interval);
  //       }
  //     } else {
  //       clearInterval(currentInterval);
  //       setCurrentInterval(null);
  //       setTimer(0);
  //     }
  //   }
  //   scrollToBottom();
  // }, [logs, jumpDetectionRunning, currentInterval]);

  // const updateLogs = (count) => {
  //   const [time] = new Date().toTimeString().split(" ");
  //   const fullLog = {
  //     time,
  //     message: `Looking for jumpmaster... (${count}/120)`,
  //     loading: true,
  //     type: "jumpmaster",
  //   };
  //   const lastLog = logs[logs.length - 1];
  //   if (count > 1 && lastLog.message.includes("jumpmaster")) {
  //     logs.pop();
  //   }
  //   if (count !== 0) {
  //     setLogs((prevLogs) => [...prevLogs, fullLog]);
  //   }
  // };

  // useEffect(() => {
  //   if (jumpDetectionRunning) {
  //     updateLogs(timer);
  //   }
  // }, [timer]);

  // useEffect(() => {
  //   if (charDetectionRunning !== currentCharStatus) {
  //     setCurrentCharStatus(charDetectionRunning);
  //     const [time] = new Date().toTimeString().split(" ");
  //     let fullLog = "";
  //     if (charDetectionRunning) {
  //       setLoading(true);
  //       fullLog = {
  //         time,
  //         log: (
  //           <span className={`${styles.terminalMessage}`}>
  //             Looking for champion selection...
  //             <PushSpinner size={10} color="#686769" loading={false} />
  //           </span>
  //         ),
  //       };
  //     } else {
  //       setLoading(false);
  //       fullLog = {
  //         time,
  //         log: "Champion selection found !",
  //       };
  //     }
  //     setLogs((prevLogs) => [...prevLogs, fullLog]);
  //   }
  // }, [charDetectionRunning]);

  return (
    <div className={`${styles["cv-code"]}`}>
      <div className={`${styles["cv-code-header"]}`}>
        <div className={`${styles["cv-code-buttons"]}`}>
          <span className={`${styles["fake-button"]}`} data-close />
          <span className={`${styles["fake-button"]}`} data-minify />
          <span className={`${styles["fake-button"]}`} data-expand />
        </div>
        <span className={`${styles["cv-code-title"]}`}>apex_alert@terminal: ~</span>
      </div>
      <div className={`${styles.content} ${styles.scrollbar}`}>
        {console.log(`logs`, logs)}
        {logs.map((log, i) => (
          <TerminalMessage log={log} key={`message-${i}`} />
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default Terminal;
