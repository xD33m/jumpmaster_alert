import React from "react";
import styles from "components/terminal/Terminal.module.scss";
import { ClapSpinner } from "react-spinners-kit";

const TerminalMessage = ({ log }) => {
  const { message, loading, time } = log;
  return (
    <div className={`${styles.instruction}`}>
      <span className={`${styles.terminalMessage}`}>
        <span className={`${styles.user}`}>{`[${time}] apex_alert@info: `}</span>
        {loading && (
          <div className={`${styles.loadingSpinner}`}>
            <ClapSpinner size={8} frontColor="#0872c4" backColor="#686769" />
          </div>
        )}
        <span className={`${styles.command}`}>{message}</span>
      </span>
    </div>
  );
};

export default TerminalMessage;
