import React from "react";
import styles from "components/settingsPanel/SettingsPanel.module.scss";
import Toggle from "../toggle/Toggle";
import ThemeToggle from "../theme/ThemeToggle";
import SettingsHeading from "./SettingsHeading";

const SettingsPanel = ({ setTheme, darkTheme, startAndStop, status, socketStatus }) => {
  return (
    <>
      <SettingsHeading darkTheme={darkTheme} status={status} socketStatus={socketStatus} />
      <div className={styles.toggleSection}>
        <hr />
        <p className={styles.sectionTitle}>General</p>
        <Toggle label="Toggle Jumpmaster Alert" id="startStop" onClick={startAndStop} />
        <hr />
        <p className={styles.sectionTitle}>Settings</p>
        <Toggle
          label="Toggle"
          id="1"
          onClick={() => {
            console.log(1);
          }}
        />
        <Toggle label="Sound Alert" id="2" onClick={() => {}} />
        <Toggle label="Discord DM" id="3" onClick={() => {}} />
        <ThemeToggle setTheme={setTheme} />
      </div>
    </>
  );
};

export default SettingsPanel;
