import React, { useEffect, useState } from "react";
import io from "socket.io-client";

import Titlebar from "components/titlebar/Titlebar";

import logo from "logo.svg";
import styles from "components/App.module.scss";
import Terminal from "./terminal/Terminal";
import ThemeToggle from "./theme/ThemeToggle";

const { ipcRenderer } = window.require("electron");
const port = ipcRenderer.sendSync("get-port-number");

function App() {
  const [status, setStatus] = useState("Off");
  const [socketStatus, setSocketStatus] = useState(false);
  const [logs, setLogs] = useState([]);
  const [socket, setSocket] = useState(null);
  const [darkTheme, setTheme] = useState(false);

  useEffect(() => {
    const s = io(`http://localhost:${port}`);
    setSocket(s);

    s.on("connect", () => {
      setSocketStatus(true);
      console.log("Connected to socket");
    });

    s.on("disconnect", () => {
      setSocketStatus(false);
      console.log("Disconnected to socket");
    });

    s.on("status", (message) => {
      setStatus(message.status);
      console.log("status", message.status);
    });

    s.on("logs", (log) => {
      const [time] = new Date().toTimeString().split(" ");
      const fullLog = { time, log };
      setLogs((prevLogs) => [...prevLogs, fullLog]);
    });

    return () => {
      s.close();
    };
  }, []);

  const startAndStop = () => {
    if (status === "On") {
      socket.emit("message", { data: "Stop Jumpmaster Alert", status: "Off" });
      setStatus("Off");
    } else {
      socket.emit("message", { data: "Start Jumpmaster Alert", status: "On" });
      setStatus("On");
    }
  };
  return (
    <div className={`${styles.main} ${darkTheme ? styles.dark : styles.light}`}>
      <Titlebar darkTheme={darkTheme} />

      <div className={styles["app-header"]}>
        <div className={`${styles.col} ${styles.leftSide}`}>
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
        </div>
        <div className={styles.col}>
          <Terminal logs={logs} />
        </div>
      </div>
    </div>
  );
}

export default App;

const Toggle = ({ label, id, onClick }) => {
  return (
    <div className={styles.toggleButton}>
      <input className={styles.hide} id={id} type="checkbox" onClick={onClick} />
      <label htmlFor={id} className={styles.toggle} />
      <span className={styles.label}>{label}</span>
    </div>
  );
};
