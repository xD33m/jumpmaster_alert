import React from "react";
import styles from "components/settingsPanel/SettingsPanel.module.scss";
import logo from "./logo.svg";

const SettingsHeading = ({ darkTheme, status, socketStatus }) => {
  return (
    <div className={styles.headingSection}>
      <img
        src={logo}
        className={`${styles["app-logo"]} ${socketStatus && styles["app-logo-animation"]} ${
          status === "On" && styles.red
        } ${darkTheme && status === "Off" && styles.white}`}
        alt="logo"
      />
      <p>Apex Jumpmaster Alert</p>
    </div>
  );
};

export default SettingsHeading;
