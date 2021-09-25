import React, { useState } from "react";
import styles from "../App.module.scss";

export default function ThemeMode({ setTheme }) {
  const [themeState, setThemeState] = useState(false);

  const updateTheme = () => {
    setThemeState(!themeState);
    setTheme(!themeState);
  };

  return <Toggle label="Toggle" id="4" onClick={() => updateTheme()} />;
}

const Toggle = ({ label, id, onClick }) => {
  return (
    <div className={styles.toggleButton}>
      <input className={styles.hide} id={id} type="checkbox" onClick={onClick} />
      <label htmlFor={id} className={styles.toggle} />
      <span className={styles.label}>{label}</span>
    </div>
  );
};
