import React, { useEffect, useState } from "react";
import { io } from "socket.io-client";

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
      setLogs((prevLogs) => [...prevLogs, log].slice(-5));
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

      <div className={styles.app}>
        <div className={styles["app-header"]}>
          <div className={styles.col}>
            <img
              src={logo}
              className={`${styles["app-logo"]} ${socketStatus && styles["app-logo-animation"]} ${
                status === "On" && styles.red
              }`}
              alt="logo"
            />
            <button
              type="button"
              className={styles.button}
              aria-label="Increment value"
              onClick={startAndStop}
            >
              {status === "On" ? "Stop" : "Start"}
            </button>
          </div>
          <div className={styles.col}>
            <Terminal logs={logs} />
          </div>
        </div>
      </div>
    </>
  );
}

export default App;

const Terminal = ({ logs }) => {
  return (
    <div className={styles.terminal}>
      {logs.map((log, i) => (
        <p>{log}</p>
      ))}
    </div>
  );
};
