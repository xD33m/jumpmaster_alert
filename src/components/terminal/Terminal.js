import React, { useEffect, useRef } from "react";
import styles from "components/terminal/Terminal.module.scss";
import TerminalMessage from "./TerminalMessage";

const Terminal = ({ logs }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [logs]);

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
