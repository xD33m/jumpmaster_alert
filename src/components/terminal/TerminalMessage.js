import React from "react";
import styles from "components/terminal/Terminal.module.scss";

const TerminalMessage = ({ message }) => {
  return (
    <div className={`${styles.instruction}`}>
      <span className={`${styles.user}`}>{`[${message.time}] apex_alert@info: `}</span>
      <span className={`${styles.command}`}>{message.log}</span>
    </div>
  );
};

export default TerminalMessage;
