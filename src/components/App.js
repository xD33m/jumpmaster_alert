import React, { useEffect, useState } from "react";
import io from "socket.io-client";

import styles from "components/App.module.scss";
import Titlebar from "components/titlebar/Titlebar";
import Terminal from "./terminal/Terminal";
import SettingsPanel from "./settingsPanel/SettingsPanel";

const { ipcRenderer } = window.require("electron");
const port = ipcRenderer.sendSync("get-port-number");

function App() {
  const [darkTheme, setTheme] = useState(false);
  const [logs, setLogs] = useState([]);
  const [socketStatus, setSocketStatus] = useState(false);
  const [status, setStatus] = useState(false);
  const [soundActivated, setSoundActivated] = useState(false);
  const [dicordDM, setDiscordDM] = useState(false);
  const [socket, setSocket] = useState();

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
    if (status === true) {
      socket.emit("toggle", { type: "startAndStop", status: false });
      setStatus(false);
    } else {
      socket.emit("toggle", { type: "startAndStop", status: true });
      setStatus(true);
    }
  };

  const soundToggle = () => {
    if (soundActivated === true) {
      socket.emit("toggle", { type: "sound", status: false });
      setSoundActivated(false);
    } else {
      socket.emit("toggle", { type: "sound", status: true });
      setSoundActivated(true);
    }
  };

  const discordDMToggle = () => {
    if (dicordDM === true) {
      socket.emit("toggle", { type: "discordDM", status: false });
      setDiscordDM(false);
    } else {
      socket.emit("toggle", { type: "discordDM", status: true });
      setDiscordDM(true);
    }
  };

  return (
    <div className={`${styles.main} ${darkTheme ? styles.dark : styles.light}`}>
      <Titlebar darkTheme={darkTheme} />

      <div className={styles["app-header"]}>
        <div className={styles.col}>
          <SettingsPanel
            setTheme={setTheme}
            darkTheme={darkTheme}
            socketStatus={socketStatus}
            status={status}
            startAndStop={startAndStop}
            soundToggle={soundToggle}
            discordDMToggle={discordDMToggle}
          />
        </div>
        <div className={styles.col}>
          <Terminal logs={logs} setLogs={setLogs} />
        </div>
      </div>
    </div>
  );
}

export default App;
