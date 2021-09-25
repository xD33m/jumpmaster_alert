import React, { useEffect, useRef, useState } from "react";
import io from "socket.io-client";

import Titlebar from "components/titlebar/Titlebar";

import logo from "logo.svg";
import styles from "components/App.module.scss";

const { ipcRenderer } = window.require("electron");
const port = ipcRenderer.sendSync("get-port-number");

function App() {
  const [status, setStatus] = useState("Off");
  const [socketStatus, setSocketStatus] = useState(false);
  const [logs, setLogs] = useState([]);
  const [socket, setSocket] = useState(null);

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
      setLogs((prevLogs) => [...prevLogs, log]);
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
    <>
      <Titlebar />

      <div className={styles["app-header"]}>
        <div className={`${styles.col} ${styles.leftSide}`}>
          <div className={styles.headingSection}>
            <img
              src={logo}
              className={`${styles["app-logo"]} ${socketStatus && styles["app-logo-animation"]} ${
                status === "On" && styles.red
              }`}
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
            <Toggle label="Toggle" id="2" onClick={() => {}} />
            <Toggle label="Toggle" id="3" onClick={() => {}} />
            <Toggle label="Toggle" id="4" onClick={() => {}} />
          </div>
        </div>
        <div className={styles.col}>
          <Terminal logs={logs} />
        </div>
      </div>
    </>
  );
}

export default App;

const TerminalMessage = ({ message }) => {
  return (
    <div className={`${styles.instruction}`}>
      <span className={`${styles.user}`}>apex_alert@log: </span>
      <span className={`${styles.command}`}>{message}</span>
    </div>
  );
};

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

const Toggle = ({ label, id, onClick }) => {
  return (
    <div className={styles.toggleButton}>
      <input className={styles.hide} id={id} type="checkbox" onClick={onClick} />
      <label htmlFor={id} className={styles.toggle} />
      <span className={styles.label}>{label}</span>
    </div>
  );
};
