import React from "react";
import styles from "../App.module.scss";

const TerminalMessage = ({ message }) => {
  return (
    <div className={`${styles.instruction}`}>
      <span className={`${styles.user}`}>{`[${message.time}] apex_alert@log: `}</span>
      <span className={`${styles.command}`}>{message.log}</span>
    </div>
  );
};

export default TerminalMessage;
