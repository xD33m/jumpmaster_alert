import React, { useEffect, useRef, useState } from "react";
import styles from "components/terminal/Terminal.module.scss";
import TerminalMessage from "./TerminalMessage";

const Terminal = ({ logs, detectionRunning, setLogs }) => {
  const messagesEndRef = useRef(null);

  const [timer, setTimer] = useState(0);
  const [currentStatus, setCurrentStatus] = useState(detectionRunning);
  const [currentInterval, setCurrentInterval] = useState();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (detectionRunning !== currentStatus) {
      setCurrentStatus(detectionRunning);
      if (detectionRunning) {
        if (!currentInterval) {
          const interval = setInterval(() => setTimer((prevVal) => prevVal + 1), 1000);
          setCurrentInterval(interval);
        }
      } else {
        clearInterval(currentInterval);
        setCurrentInterval(null);
        setTimer(0);
      }
    }
    scrollToBottom();
  }, [logs, detectionRunning, currentInterval]);

  const updateLogs = (count) => {
    const [time] = new Date().toTimeString().split(" ");
    const fullLog = { time, log: `Looking for jumpmster... (${count}/120)` };
    const lastLog = logs[logs.length - 1];
    if (count > 1 && lastLog.log.includes("Looking")) {
      logs.pop();
    }
    if (count !== 0) {
      setLogs((prevLogs) => [...prevLogs, fullLog]);
    }
  };

  useEffect(() => {
    updateLogs(timer);
  }, [timer]);

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
          <TerminalMessage message={log} key={`message-${i}`} />
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};

export default Terminal;
