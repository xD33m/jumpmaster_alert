import React, { useEffect, useRef, useState } from "react";
import styles from "components/terminal/Terminal.module.scss";
import { PushSpinner } from "react-spinners-kit";
import TerminalMessage from "./TerminalMessage";

const Terminal = ({ logs, jumpDetectionRunning, charDetectionRunning, setLogs }) => {
  const messagesEndRef = useRef(null);

  const [timer, setTimer] = useState(0);
  const [currentJumpStatus, setCurrentJumpStatus] = useState(jumpDetectionRunning);
  const [currentCharStatus, setCurrentCharStatus] = useState(charDetectionRunning);
  const [currentInterval, setCurrentInterval] = useState();
  const [loading, setLoading] = useState(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (jumpDetectionRunning !== currentJumpStatus) {
      setCurrentJumpStatus(jumpDetectionRunning);
      if (jumpDetectionRunning) {
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
  }, [logs, jumpDetectionRunning, currentInterval]);

  const updateLogs = (count) => {
    const [time] = new Date().toTimeString().split(" ");
    const fullLog = { time, log: `Looking for jumpmster... (${count}/120)` };
    const lastLog = logs[logs.length - 1];
    if (count > 1 && lastLog.log.includes("jumpmster")) {
      logs.pop();
    }
    if (count !== 0) {
      setLogs((prevLogs) => [...prevLogs, fullLog]);
    }
  };

  useEffect(() => {
    updateLogs(timer);
  }, [timer]);

  useEffect(() => {
    if (charDetectionRunning !== currentCharStatus) {
      setCurrentCharStatus(charDetectionRunning);
      const [time] = new Date().toTimeString().split(" ");
      let fullLog = "";
      if (charDetectionRunning) {
        setLoading(true);
        fullLog = {
          time,
          log: (
            <span className={`${styles.terminalMessage}`}>
              Looking for champion selection...
              <PushSpinner size={10} color="#686769" loading={false} />
            </span>
          ),
        };
      } else {
        setLoading(false);
        fullLog = {
          time,
          log: "Champion selection found !",
        };
      }
      setLogs((prevLogs) => [...prevLogs, fullLog]);
    }
  }, [charDetectionRunning]);

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
