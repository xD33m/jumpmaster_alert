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

  const [count, setCount] = useState(0);

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
        {logs.map((log, i) => (
          <TerminalMessage log={log} key={`message-${i}`} />
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default Terminal;
