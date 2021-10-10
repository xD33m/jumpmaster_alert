import React from "react";
import styles from "components/terminal/Terminal.module.scss";
import { PushSpinner } from "react-spinners-kit";

const TerminalMessage = ({ log }) => {
  const { message, loading, time } = log;
  return (
    <div className={`${styles.instruction}`}>
      <span className={`${styles.terminalMessage}`}>
        <span className={`${styles.user}`}>{`[${time}] apex_alert@info: `}</span>
        <span className={`${styles.command}`}>{message}</span>
        {loading && <PushSpinner size={10} color="#686769" />}
      </span>
    </div>
  );
};

export default TerminalMessage;
