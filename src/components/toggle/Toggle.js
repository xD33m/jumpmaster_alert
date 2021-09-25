import React from "react";
import styles from "components/toggle/Toggle.module.scss";

const Toggle = ({ label, id, onClick }) => {
  return (
    <div className={styles.toggleButton}>
      <input className={styles.hide} id={id} type="checkbox" onClick={onClick} />
      <label htmlFor={id} className={styles.toggle} />
      <span className={styles.label}>{label}</span>
    </div>
  );
};

export default Toggle;
